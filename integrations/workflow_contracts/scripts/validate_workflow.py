#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Validate workflow descriptors without executing bindings or fetching schemas."""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError as exc:
    raise SystemExit('Use Python with PyYAML>=6 and jsonschema>=4.18 installed: ' + str(exc)) from exc

SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'references/workflow.schema.json'


class DescriptorError(ValueError):
    """An invalid descriptor or unsupported schema dependency."""


class StrictLoader(yaml.SafeLoader):
    """Accept JSON-compatible YAML with unique string keys and no aliases."""


StrictLoader.yaml_implicit_resolvers = deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)
for key, resolvers in StrictLoader.yaml_implicit_resolvers.items():
    StrictLoader.yaml_implicit_resolvers[key] = [
        item for item in resolvers
        if item[0] not in ('tag:yaml.org,2002:bool', 'tag:yaml.org,2002:timestamp')
    ]
StrictLoader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|false)$'), list('tf'))


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise DescriptorError('YAML mapping keys must be strings')
        if key in result:
            raise DescriptorError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(path):
    source = Path(path).read_text(encoding='utf-8')
    for token in yaml.scan(source):
        if isinstance(token, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken, yaml.tokens.TagToken)):
            raise DescriptorError('YAML aliases, anchors, and explicit tags are unsupported')
    result = yaml.load(source, Loader=StrictLoader)
    json.dumps(result, allow_nan=False)
    return result


def local_path(base, reference, root):
    uri = urlsplit(reference)
    if uri.scheme or uri.netloc or uri.query or Path(unquote(uri.path)).is_absolute():
        raise DescriptorError(f'only local relative schema/source references are allowed: {reference}')
    path = (base / unquote(uri.path)).resolve()
    if not path.is_relative_to(root):
        raise DescriptorError(f'reference escapes repository root: {reference}')
    return path, uri.fragment


class Schemas:
    """Resolve local payload schemas; reject all network retrieval."""

    def __init__(self, root):
        self.root = root
        self.resources = {}
        self.references = []
        self.registry = Registry()

    def read(self, path):
        uri = path.as_uri()
        if uri in self.resources:
            return
        raw = json.loads(path.read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(raw)
        if isinstance(raw, dict) and raw.get('$schema', 'https://json-schema.org/draft/2020-12/schema') != 'https://json-schema.org/draft/2020-12/schema':
            raise DescriptorError(f'payload schema must use JSON Schema 2020-12: {path}')
        self.resources[uri] = None

        def rewrite(value, top=False):
            if isinstance(value, list):
                return [rewrite(item) for item in value]
            if not isinstance(value, dict):
                return value
            if '$dynamicRef' in value or ('$id' in value and not top):
                raise DescriptorError('nested $id and $dynamicRef are unsupported; use local $ref')
            result = {}
            for key, item in value.items():
                if key == '$id':
                    continue
                if key == '$ref':
                    if item.startswith('#'):
                        resolved = uri + item
                    else:
                        target, fragment = local_path(path.parent, item, self.root)
                        self.read(target)
                        resolved = target.as_uri() + ('#' + fragment if fragment else '')
                    self.references.append(resolved)
                    result[key] = resolved
                else:
                    result[key] = rewrite(item)
            return result

        normalized = rewrite(raw, top=True)
        self.resources[uri] = normalized

    def type_schema(self, definition, base):
        raw = definition['schema']
        if isinstance(raw, str):
            path, fragment = local_path(base, raw, self.root)
            self.read(path)
            reference = path.as_uri() + ('#' + fragment if fragment else '')
            self.references.append(reference)
            return {'$ref': reference}
        Draft202012Validator.check_schema(raw)
        if isinstance(raw, dict) and raw.get('$schema', 'https://json-schema.org/draft/2020-12/schema') != 'https://json-schema.org/draft/2020-12/schema':
            raise DescriptorError('inline payload schemas must use JSON Schema 2020-12')

        def no_refs(value):
            if isinstance(value, dict):
                if any(k in value for k in ('$ref', '$dynamicRef', '$id')):
                    raise DescriptorError('inline payload schemas cannot contain references; use a schema file')
                for item in value.values():
                    no_refs(item)
            elif isinstance(value, list):
                for item in value:
                    no_refs(item)
        no_refs(raw)
        return raw

    def finish(self):
        self.registry = Registry().with_resources(
            (uri, Resource.from_contents(value, default_specification=DRAFT202012))
            for uri, value in self.resources.items()
        )
        for reference in self.references:
            self.registry.resolver().lookup(reference)

    def expand(self, schema):
        seen = set()
        while isinstance(schema, dict) and '$ref' in schema:
            reference = schema['$ref']
            if reference in seen:
                raise DescriptorError('recursive schema cannot be expanded at this reference')
            seen.add(reference)
            if len(schema) != 1:
                raise DescriptorError('static field inspection requires $ref without sibling assertions')
            schema = self.registry.resolver().lookup(reference).contents
        return schema


@dataclass
class Slot:
    schema: object
    name: str | None = None
    optional: bool = False


class Semantics:
    def __init__(self, data, base, root):
        self.data = data
        self.errors = []
        self.schemas = Schemas(root)
        self.types = {name: self.schemas.type_schema(value, base) for name, value in data['types'].items()}
        self.schemas.finish()
        self.operations = data['operations']

    def error(self, location, message):
        self.errors.append(f'{location}: {message}')

    def slot(self, name):
        if name not in self.types:
            raise DescriptorError(f'unknown type {name}')
        return Slot(self.types[name], name)

    def ports(self, ports):
        return {key: Slot(self.slot(port['type']).schema, port['type'], not port.get('required', True)) for key, port in ports.items()}

    def resolve(self, reference, scope, present=frozenset()):
        prefixes = [key for key in scope if reference == key or reference.startswith(key + '.')]
        if not prefixes:
            raise DescriptorError(f'unavailable or forward reference {reference}')
        prefix = max(prefixes, key=len)
        initial = scope[prefix]
        schema, optional = initial.schema, initial.optional
        suffix = reference[len(prefix):].lstrip('.')
        for field in suffix.split('.') if suffix else []:
            schema = self.schemas.expand(schema)
            if not isinstance(schema, dict) or schema.get('type') not in ('object', ['object']):
                raise DescriptorError(f'field access requires a guaranteed object parent in {reference}')
            if field not in schema.get('properties', {}):
                raise DescriptorError(f'field {field} is not statically declared in {reference}')
            optional = optional or field not in schema.get('required', [])
            schema = schema['properties'][field]
        if reference in present:
            optional = False
        return Slot(schema, initial.name if not suffix else None, optional)

    def compatible(self, actual, expected):
        if actual.name and expected.name:
            return actual.name == expected.name
        actual_schema = self.schemas.expand(actual.schema)
        expected_schema = self.schemas.expand(expected.schema)
        if actual_schema == expected_schema or expected_schema is True or actual_schema is False:
            return True
        # Only prove the primitive widening below. Complex schemas require the same named type.
        if isinstance(actual_schema, dict) and isinstance(expected_schema, dict):
            if set(expected_schema) <= {'type', 'description', 'title'}:
                accepted = expected_schema.get('type')
                found = actual_schema.get('type')
                return found == accepted or (found == 'integer' and accepted == 'number')
        return False

    def expression(self, expression, scope, expected=None, condition=False, present=frozenset(), optional=False):
        if 'ref' in expression:
            slot = self.resolve(expression['ref'], scope, present)
            if slot.optional and not optional:
                raise DescriptorError(f'possibly absent reference {expression["ref"]}; guard with exists')
        elif 'literal' in expression:
            value = expression['literal']
            if expected:
                issues = list(Draft202012Validator(expected.schema, registry=self.schemas.registry).iter_errors(value))
                if issues:
                    raise DescriptorError(f'literal does not satisfy {expected.name or expected.schema}: {issues[0].message}')
                return expected
            slot = Slot({'const': value, 'type': ('null' if value is None else 'boolean' if isinstance(value, bool) else 'integer' if isinstance(value, int) else 'number' if isinstance(value, float) else 'string' if isinstance(value, str) else 'array' if isinstance(value, list) else 'object')})
        else:
            operator, arguments = next(iter(expression.items()))
            if operator in ('all', 'any'):
                for item in arguments:
                    self.expression(item, scope, condition=True, present=present)
            elif operator == 'not':
                self.expression(arguments, scope, condition=True, present=present)
            elif operator == 'exists':
                if 'ref' not in arguments:
                    raise DescriptorError('exists requires a reference')
                self.resolve(arguments['ref'], scope, present)
            elif operator == 'eq':
                left, right = arguments
                if 'literal' in left and 'literal' not in right:
                    left, right = right, left
                left_slot = self.expression(left, scope, present=present)
                if 'literal' in left:
                    left_slot = Slot({'type': left_slot.schema['type']})
                self.expression(right, scope, expected=left_slot, present=present)
            slot = Slot({'type': 'boolean'})
        if condition and not self.compatible(slot, Slot({'type': 'boolean'})):
            raise DescriptorError('condition must be boolean')
        if expected and not self.compatible(slot, expected):
            raise DescriptorError(f'type mismatch: {slot.name or slot.schema} -> {expected.name or expected.schema}')
        return slot

    @staticmethod
    def guards(expression):
        if 'exists' in expression and 'ref' in expression['exists']:
            return {expression['exists']['ref']}
        if 'all' in expression:
            return set().union(*(Semantics.guards(item) for item in expression['all']))
        return set()

    def exports(self, node, scope, location):
        result = {}
        for name, port in node.get('outputs', {}).items():
            expected = self.slot(port['type'])
            self.expression(port['value'], scope, expected=expected)
            result[name] = expected
        return result

    def node(self, node, inherited, location):
        scope = dict(inherited)
        kind = node['kind']
        if kind in ('call', 'handoff'):
            name = node['operation']
            if name not in self.operations:
                raise DescriptorError(f'{location}: unknown operation {name}')
            operation = self.operations[name]
            required = {name for name, port in operation['inputs'].items() if port.get('required', True)}
            supplied = set(node['arguments'])
            if required - supplied or supplied - set(operation['inputs']):
                raise DescriptorError(f'{location}: arguments missing={sorted(required - supplied)} unknown={sorted(supplied - set(operation["inputs"]))}')
            for argument, expression in node['arguments'].items():
                port = operation['inputs'][argument]
                self.expression(expression, scope, expected=self.slot(port['type']), optional=not port.get('required', True))
            if kind == 'handoff' and operation['execution'].get('binding', {}).get('kind') != 'workflow':
                raise DescriptorError('handoff requires a workflow binding')
            return self.ports(operation['outputs']), scope
        if kind == 'gate':
            self.expression(node['condition'], scope, condition=True)
            for reference in self.guards(node['condition']):
                slot = self.resolve(reference, scope)
                scope[reference] = Slot(slot.schema, slot.name, False)
            return {}, scope
        if kind == 'sequence':
            ids = set()
            for index, child in enumerate(node['steps']):
                step_id = child.get('id')
                if not step_id or step_id in ids:
                    raise DescriptorError(f'{location}: sequence children require unique ids')
                ids.add(step_id)
                child_outputs, child_scope = self.node(child, scope, f'{location}.steps[{index}]')
                if child['kind'] == 'gate':
                    scope = child_scope
                for name, slot in child_outputs.items():
                    scope[f'steps.{step_id}.outputs.{name}'] = slot
        elif kind == 'parallel':
            for name, child in node['branches'].items():
                branch_outputs, _ = self.node(child, inherited, f'{location}.branches.{name}')
                for port, slot in branch_outputs.items():
                    scope[f'branches.{name}.outputs.{port}'] = slot
        elif kind == 'switch':
            cases = node['cases']
            if len({case['id'] for case in cases}) != len(cases):
                raise DescriptorError('switch case ids must be unique')
            variants = []
            for case in cases:
                self.expression(case['when'], scope, condition=True)
                branch_scope = dict(scope)
                for reference in self.guards(case['when']):
                    slot = self.resolve(reference, scope)
                    branch_scope[reference] = Slot(slot.schema, slot.name, False)
                variants.append(self.node(case['body'], branch_scope, f'{location}.cases.{case["id"]}')[0])
            variants.append(self.node(node['default'], scope, f'{location}.default')[0])
            first = variants[0]
            if any(set(other) != set(first) or any(other[k].name != first[k].name or other[k].optional != first[k].optional for k in first) for other in variants[1:]):
                raise DescriptorError('switch branches must expose identical output names, types and optionality')
            for name, slot in first.items():
                scope[f'selected.outputs.{name}'] = slot
        elif kind == 'loop':
            state = self.slot(node['state_type'])
            self.expression(node['initial'], scope, expected=state)
            scope['loop.state'] = state
            body, _ = self.node(node['body'], scope, location + '.body')
            scope.update({f'body.outputs.{name}': slot for name, slot in body.items()})
            self.expression(node['next_state'], scope, expected=state)
            self.expression(node['until'], scope, condition=True)
        elif kind == 'map':
            item = self.slot(node['item_type'])
            items = self.expression(node['items'], scope)
            expanded = self.schemas.expand(items.schema)
            if not isinstance(expanded, dict) or expanded.get('type') != 'array' or 'items' not in expanded:
                raise DescriptorError('map.items must have a statically declared array items schema')
            if not self.compatible(Slot(expanded['items']), item):
                raise DescriptorError('map item_type does not match array items')
            scope['map.item'] = item
            body, _ = self.node(node['body'], scope, location + '.body')
            for name, slot in body.items():
                if slot.optional:
                    raise DescriptorError('map body outputs must be required')
                scope[f'items.outputs.{name}'] = Slot({'type': 'array', 'items': slot.schema})
        return self.exports(node, scope, location), scope

    def check_policy(self):
        policy = self.data['policy']
        allowed = set(policy['authority']['allowed'])
        forbidden = set(policy['authority']['forbidden'])
        if allowed & forbidden:
            self.error('policy.authority', 'an action cannot be both allowed and forbidden')
        for name, operation in self.operations.items():
            if operation['execution']['mode'] == 'specification_only':
                if self.data['lifecycle'] != 'draft':
                    self.error(f'operations.{name}', 'specification-only operations require draft lifecycle')
                if self.data['provenance']['coverage'] == 'complete':
                    self.error(f'operations.{name}', 'specification-only operations require an explicit coverage gap')
            for port in (*operation['inputs'].values(), *operation['outputs'].values()):
                self.slot(port['type'])
            if 'authority' in operation:
                own = operation['authority']
                if not set(own['allowed']) <= allowed or set(own['allowed']) & (forbidden | set(own['forbidden'])):
                    self.error(f'operations.{name}.authority', 'operation exceeds workflow authority')
            if 'effects' in operation:
                own = operation['effects']
                for field in ('network', 'external_write'):
                    if not set(own.get(field, [])) <= set(policy['effects'].get(field, [])):
                        self.error(f'operations.{name}.effects', f'{field} exceeds workflow effects')
                for field in ('read', 'write'):
                    if not set(own['filesystem'][field]) <= set(policy['effects']['filesystem'][field]):
                        self.error(f'operations.{name}.effects', f'filesystem {field} exceeds workflow effects')

    def validate(self):
        self.check_policy()
        scope = {f'inputs.{name}': slot for name, slot in self.ports(self.data['inputs']).items()}
        for condition in self.data['activation']['prerequisites']:
            self.expression(condition, scope, condition=True)
        flow_outputs, final_scope = self.node(self.data['flow'], scope, 'flow')
        final_scope.update({f'flow.outputs.{name}': slot for name, slot in flow_outputs.items()})
        for name, port in self.data['outputs'].items():
            self.expression(port['value'], final_scope, expected=self.slot(port['type']))
        return self.errors


def validate(path, repository_root=None, require_declared_bindings=False):
    path = Path(path).resolve()
    errors = []
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(schema)
        data = load_yaml(path)
        for error in Draft202012Validator(schema).iter_errors(data):
            errors.append(f'{".".join(map(str, error.absolute_path)) or "$"}: {error.message}')
        if not errors:
            root = Path(repository_root).resolve() if repository_root else path.parent
            if not path.is_relative_to(root):
                raise DescriptorError('workflow file is outside repository root')
            errors.extend(Semantics(data, path.parent, root).validate())
            if require_declared_bindings:
                for name, operation in data['operations'].items():
                    if operation['execution']['mode'] == 'specification_only':
                        errors.append(f'operations.{name}: binding is not declared')
            if repository_root:
                for source in data['provenance']['sources']:
                    target, fragment = local_path(root, source['path'], root)
                    if fragment:
                        raise DescriptorError('put source selectors in selector, not path fragments')
                    if not target.is_file():
                        errors.append(f'provenance: source file not found: {source["path"]}')
                    elif 'digest' in source and source['digest'] != 'sha256:' + hashlib.sha256(target.read_bytes()).hexdigest():
                        errors.append(f'provenance: source digest mismatch: {source["path"]}')
    except (OSError, ValueError, TypeError, yaml.YAMLError, RecursionError) as exc:
        errors.append(str(exc))
    except Exception as exc:
        # Schema-library resolution errors have library-specific exception classes.
        errors.append(f'{type(exc).__name__}: {exc}')
    return {'path': str(path), 'valid': not errors, 'errors': errors,
            'runtime_bindings_verified': False, 'source_semantics_verified': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workflows', nargs='*', type=Path)
    parser.add_argument('--repository-root', type=Path)
    parser.add_argument('--require-declared-bindings', action='store_true')
    parser.add_argument('--schema-only', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if not args.workflows and not args.schema_only:
        parser.error('provide workflow paths or --schema-only')
    if args.schema_only:
        try:
            schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
            Draft202012Validator.check_schema(schema)
            registry = Registry().with_resource(schema['$id'], Resource.from_contents(schema))
            def visit(value):
                if isinstance(value, dict):
                    if '$ref' in value:
                        registry.resolver(schema['$id']).lookup(value['$ref'])
                    for child in value.values():
                        visit(child)
                elif isinstance(value, list):
                    for child in value:
                        visit(child)
            visit(schema)
            result = {'schema': str(SCHEMA_PATH), 'valid': True, 'errors': []}
        except Exception as exc:
            result = {'schema': str(SCHEMA_PATH), 'valid': False, 'errors': [str(exc)]}
        print(json.dumps(result, indent=2) if args.json else f'schema: {"PASS" if result["valid"] else "FAIL"} {result["errors"]}')
        if not result['valid']:
            return 1
    results = [validate(path, args.repository_root, args.require_declared_bindings) for path in args.workflows]
    if results:
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for result in results:
                print(f'{"PASS" if result["valid"] else "FAIL"} {result["path"]}')
                for error in result['errors']:
                    print('  ' + error)
            print('Checks describe contracts only; runtime bindings and source fidelity require repository verification.')
    return int(any(not result['valid'] for result in results))


if __name__ == '__main__':
    sys.exit(main())
