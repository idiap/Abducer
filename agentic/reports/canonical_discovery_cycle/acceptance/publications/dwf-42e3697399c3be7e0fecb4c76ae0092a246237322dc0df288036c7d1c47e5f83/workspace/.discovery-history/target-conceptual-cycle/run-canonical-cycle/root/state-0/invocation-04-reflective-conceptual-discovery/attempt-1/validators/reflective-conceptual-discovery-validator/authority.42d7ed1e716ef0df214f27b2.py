"""Isolated exact, symbolic, finite, numeric, sweep, and Lean probe adapters."""

from __future__ import annotations

import ast
import importlib.util
import itertools
import math
import random
import shutil
import statistics
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

from agentic.discovery.budgets import BudgetExceeded, ResourceGovernor


class AdapterSpecError(ValueError):
    """Raised before execution when a probe adapter contract is incomplete."""


_BINARY = {
    ast.Add: lambda left, right: left + right,
    ast.Sub: lambda left, right: left - right,
    ast.Mult: lambda left, right: left * right,
    ast.Div: lambda left, right: left / right,
    ast.FloorDiv: lambda left, right: left // right,
    ast.Mod: lambda left, right: left % right,
    ast.Pow: lambda left, right: left**right,
}
_UNARY = {ast.UAdd: lambda value: value, ast.USub: lambda value: -value, ast.Not: lambda value: not value}
_COMPARE = {
    ast.Eq: lambda left, right: left == right,
    ast.NotEq: lambda left, right: left != right,
    ast.Lt: lambda left, right: left < right,
    ast.LtE: lambda left, right: left <= right,
    ast.Gt: lambda left, right: left > right,
    ast.GtE: lambda left, right: left >= right,
}
_FUNCTIONS = {
    "abs": abs,
    "sqrt": math.sqrt,
    "exp": math.exp,
    "log": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "floor": math.floor,
    "ceil": math.ceil,
    "min": min,
    "max": max,
}


def _number(value: int | float, *, exact: bool) -> int | float | Fraction:
    if isinstance(value, bool):
        raise AdapterSpecError("booleans are not numeric constants")
    if exact:
        if isinstance(value, int):
            return Fraction(value, 1)
        # Decimal source spelling is preserved by the AST only approximately;
        # parsing its repr produces the intended finite decimal rational.
        return Fraction(str(value))
    return value


def safe_expression(expression: str, names: Mapping[str, Any] | None = None, *, exact: bool = False) -> Any:
    """Evaluate the deliberately small pure expression language used by probes."""

    if not isinstance(expression, str) or not expression.strip():
        raise AdapterSpecError("expression must be a non-empty string")
    environment = dict(names or {})
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise AdapterSpecError(f"invalid expression: {exc.msg}") from exc

    def visit(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, bool)):
            return node.value if isinstance(node.value, bool) else _number(node.value, exact=exact)
        if isinstance(node, ast.Name):
            if node.id not in environment:
                raise AdapterSpecError(f"unbound variable {node.id!r}")
            value = environment[node.id]
            return Fraction(str(value)) if exact and isinstance(value, (int, float, str)) else value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow):
                if not isinstance(right, (int, Fraction)) or int(right) != right or abs(int(right)) > 64:
                    raise AdapterSpecError("power exponent must be a bounded integer")
                right = int(right)
            try:
                return _BINARY[type(node.op)](left, right)
            except (ArithmeticError, ValueError, TypeError) as exc:
                raise AdapterSpecError(f"expression arithmetic failed: {exc}") from exc
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
            return _UNARY[type(node.op)](visit(node.operand))
        if isinstance(node, ast.BoolOp) and isinstance(node.op, (ast.And, ast.Or)):
            values = [bool(visit(child)) for child in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.Compare):
            left = visit(node.left)
            for operator, comparator in zip(node.ops, node.comparators, strict=True):
                right = visit(comparator)
                comparator_fn = _COMPARE.get(type(operator))
                if comparator_fn is None:
                    raise AdapterSpecError(f"comparison {type(operator).__name__} is forbidden")
                if not comparator_fn(left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if exact or node.func.id not in _FUNCTIONS or node.keywords:
                raise AdapterSpecError(f"function {node.func.id!r} is forbidden")
            return _FUNCTIONS[node.func.id](*[visit(argument) for argument in node.args])
        raise AdapterSpecError(f"expression node {type(node).__name__} is forbidden")

    return visit(tree)


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def exact_adapter(model: Mapping[str, Any], governor: ResourceGovernor) -> dict[str, Any]:
    """Check a rational equality or bounded integer predicate exactly."""

    operation = model.get("operation", "equality")
    governor.checkpoint()
    if operation == "equality":
        left_expression = model.get("left", model.get("expression"))
        right_expression = model.get("right", model.get("expected"))
        left = safe_expression(left_expression, exact=True)
        right = safe_expression(right_expression, exact=True)
        if not isinstance(left, Fraction) or not isinstance(right, Fraction):
            raise AdapterSpecError("exact equality must produce rational values")
        equal = left == right
        witness = {"left": _fraction_text(left), "right": _fraction_text(right), "difference": _fraction_text(left - right)}
        return {
            "status": "succeeded" if equal else "counterexample",
            "epistemic_outcome": "supports_within_scope" if equal else "falsifies_claim",
            "result": {"claim_holds": equal, "exact_values": witness},
            "certificate": {
                "kind": "normalized_rational_equality",
                "expression": f"({left_expression}) == ({right_expression})",
                **witness,
                "verification": "Fraction numerator and denominator normalized by gcd",
            },
            "uncertainty_analysis": {"kind": "none_exact_arithmetic", "roundoff": 0},
            "completeness": {"complete": True, "scope": "declared rational expression"},
        }
    if operation == "integer_predicate":
        variables = model.get("variables", {})
        predicate = model.get("predicate")
        if not isinstance(variables, Mapping) or not predicate:
            raise AdapterSpecError("integer_predicate requires variables and predicate")
        value = safe_expression(str(predicate), variables, exact=True)
        if not isinstance(value, bool):
            raise AdapterSpecError("integer predicate must evaluate to boolean")
        return {
            "status": "succeeded" if value else "counterexample",
            "epistemic_outcome": "supports_within_scope" if value else "falsifies_claim",
            "result": {"claim_holds": value, "assignment": dict(variables)},
            "certificate": {"kind": "exact_integer_predicate", "predicate": predicate, "assignment": dict(variables), "value": value},
            "uncertainty_analysis": {"kind": "none_exact_arithmetic", "roundoff": 0},
            "completeness": {"complete": True, "scope": "declared assignment"},
        }
    raise AdapterSpecError(f"unknown exact operation: {operation!r}")


def sympy_adapter(model: Mapping[str, Any], governor: ResourceGovernor) -> dict[str, Any]:
    """Use a real SymPy simplifier when that capability is installed."""

    if importlib.util.find_spec("sympy") is None:
        return {
            "status": "capability_unavailable",
            "epistemic_outcome": "not_evaluated",
            "result": {"available": False, "capability": "sympy"},
            "certificate": None,
            "uncertainty_analysis": None,
            "completeness": None,
        }
    import sympy  # type: ignore[import-not-found]

    governor.checkpoint()
    left_text = model.get("left")
    right_text = model.get("right", "0")
    if not isinstance(left_text, str) or not isinstance(right_text, str):
        raise AdapterSpecError("sympy adapter requires string left and right expressions")
    symbols = {name: sympy.Symbol(name) for name in model.get("symbols", [])}
    try:
        left = sympy.sympify(left_text, locals=symbols, evaluate=True)
        right = sympy.sympify(right_text, locals=symbols, evaluate=True)
        normal = sympy.cancel(sympy.together(left - right))
        equal = normal == 0
    except Exception as exc:
        return {
            "status": "solver_failure",
            "epistemic_outcome": "not_evaluated",
            "result": {"available": True, "error": f"{type(exc).__name__}: {exc}"},
            "certificate": None,
            "uncertainty_analysis": None,
            "completeness": None,
        }
    return {
        "status": "succeeded" if equal else "counterexample",
        "epistemic_outcome": "supports_within_scope" if equal else "falsifies_claim",
        "result": {"claim_holds": equal, "normal_form": str(normal), "sympy_version": sympy.__version__},
        "certificate": {
            "kind": "sympy_exact_normal_form",
            "left": left_text,
            "right": right_text,
            "normal_form": str(normal),
            "sympy_version": sympy.__version__,
        },
        "uncertainty_analysis": {"kind": "symbolic_exact_no_numeric_roundoff"},
        "completeness": {"complete": True, "scope": "algebraic simplification in declared SymPy domain"},
    }


def finite_model_adapter(model: Mapping[str, Any], governor: ResourceGovernor) -> dict[str, Any]:
    """Exhaust a finite Cartesian model and emit witness/completeness metadata."""

    variables = model.get("variables")
    predicate = model.get("predicate")
    quantifier = model.get("quantifier", "forall")
    if not isinstance(variables, Mapping) or not variables or not isinstance(predicate, str):
        raise AdapterSpecError("finite_model requires variables and predicate")
    if quantifier not in {"forall", "exists"}:
        raise AdapterSpecError("finite quantifier must be forall or exists")
    names = sorted(variables)
    domains: list[list[Any]] = []
    for name in names:
        values = variables[name]
        if not isinstance(values, list) or not values:
            raise AdapterSpecError(f"finite domain {name!r} must be a non-empty list")
        domains.append(values)
    state_count = math.prod(len(domain) for domain in domains)
    max_states = int(model.get("max_states", state_count))
    if max_states < 1:
        raise AdapterSpecError("max_states must be positive")
    explored = 0
    witness = None
    counterexample = None
    for values in itertools.product(*domains):
        governor.checkpoint()
        if explored >= max_states:
            break
        assignment = dict(zip(names, values, strict=True))
        outcome = safe_expression(predicate, assignment, exact=True)
        if not isinstance(outcome, bool):
            raise AdapterSpecError("finite predicate must return boolean")
        explored += 1
        if outcome and witness is None:
            witness = assignment
        if not outcome and counterexample is None:
            counterexample = assignment
        if quantifier == "forall" and counterexample is not None:
            break
        if quantifier == "exists" and witness is not None:
            break
    decisive_early = (quantifier == "forall" and counterexample is not None) or (quantifier == "exists" and witness is not None)
    complete = explored == state_count or decisive_early
    if not complete:
        return {
            "status": "resource_exhausted",
            "epistemic_outcome": "inconclusive",
            "result": {"claim_holds": None, "explored": explored, "state_count": state_count},
            "certificate": None,
            "uncertainty_analysis": {"kind": "none_deterministic_but_incomplete"},
            "completeness": {"complete": False, "explored": explored, "state_count": state_count, "max_states": max_states},
        }
    holds = counterexample is None if quantifier == "forall" else witness is not None
    certificate = {
        "kind": "finite_model_exhaustion",
        "quantifier": quantifier,
        "predicate": predicate,
        "domains": {name: list(variables[name]) for name in names},
        "witness": witness,
        "counterexample": counterexample,
        "explored": explored,
        "state_count": state_count,
        "decisive_early_witness": decisive_early,
    }
    return {
        "status": "succeeded" if holds else "counterexample",
        "epistemic_outcome": "supports_within_scope" if holds else "falsifies_claim",
        "result": {"claim_holds": holds, "witness": witness, "counterexample": counterexample},
        "certificate": certificate,
        "uncertainty_analysis": {"kind": "none_finite_deterministic"},
        "completeness": {"complete": True, "explored": explored, "state_count": state_count, "scope": "declared finite domains"},
    }


def _grid(model: Mapping[str, Any]) -> list[dict[str, float]]:
    base = model.get("parameters", {})
    sweep = model.get("sweep", {})
    if not isinstance(base, Mapping) or not isinstance(sweep, Mapping):
        raise AdapterSpecError("numeric parameters and sweep must be objects")
    names = sorted(sweep)
    values: list[list[float]] = []
    for name in names:
        raw = sweep[name]
        if isinstance(raw, list):
            sequence = raw
        elif isinstance(raw, Mapping):
            start, stop, count = float(raw["start"]), float(raw["stop"]), int(raw["count"])
            if count < 1:
                raise AdapterSpecError("sweep count must be positive")
            sequence = [start] if count == 1 else [start + (stop - start) * index / (count - 1) for index in range(count)]
        else:
            raise AdapterSpecError(f"invalid sweep definition for {name!r}")
        if not sequence:
            raise AdapterSpecError(f"sweep {name!r} cannot be empty")
        values.append([float(value) for value in sequence])
    if not names:
        return [{str(key): float(value) for key, value in base.items()}]
    points = []
    for row in itertools.product(*values):
        point = {str(key): float(value) for key, value in base.items()}
        point.update(dict(zip(names, row, strict=True)))
        points.append(point)
    max_points = int(model.get("max_points", 100_000))
    if len(points) > max_points:
        raise AdapterSpecError(f"sweep has {len(points)} points, exceeding preregistered max_points={max_points}")
    return points


def _decision(values: list[float], rule: Mapping[str, Any], uncertainty: Mapping[str, Any] | None = None) -> bool:
    if not values:
        raise AdapterSpecError("decision rule cannot consume zero values")
    aggregation = rule.get("aggregation", "all")
    comparator = rule.get("comparator")
    threshold = rule.get("threshold")
    if aggregation == "mean":
        operands = [statistics.fmean(values)]
    else:
        operands = values
    if comparator in {"ci_above", "ci_below"}:
        if uncertainty is None or "lower" not in uncertainty or "upper" not in uncertainty:
            raise AdapterSpecError("CI decision requires preregistered uncertainty interval")
        if comparator == "ci_above":
            return float(uncertainty["lower"]) > float(threshold)
        return float(uncertainty["upper"]) < float(threshold)
    compare = {
        "<": lambda value: value < float(threshold),
        "<=": lambda value: value <= float(threshold),
        ">": lambda value: value > float(threshold),
        ">=": lambda value: value >= float(threshold),
        "==": lambda value: math.isclose(value, float(threshold), rel_tol=float(rule.get("relative_tolerance", 1e-12)), abs_tol=float(rule.get("absolute_tolerance", 1e-12))),
    }.get(str(comparator))
    if compare is None:
        raise AdapterSpecError("unsupported numeric comparator")
    outcomes = [compare(value) for value in operands]
    return any(outcomes) if aggregation == "any" else all(outcomes)


def _stochastic_samples(model: Mapping[str, Any], preregistration: Mapping[str, Any], seed_policy: Mapping[str, Any]) -> tuple[list[float], dict[str, Any]]:
    sample_size = int(preregistration.get("sample_size", 0))
    estimand = preregistration.get("estimand")
    uncertainty_method = preregistration.get("uncertainty_method")
    if sample_size < 1 or not estimand or not uncertainty_method:
        raise AdapterSpecError("stochastic probe requires estimand, positive sample_size, and uncertainty_method")
    if not preregistration.get("stopping_rule"):
        raise AdapterSpecError("stochastic probe requires an ex-ante stopping rule")
    policy = seed_policy.get("policy")
    if policy == "fixed_master_seed":
        if "master_seed" not in seed_policy:
            raise AdapterSpecError("fixed_master_seed requires master_seed")
        rng = random.Random(int(seed_policy["master_seed"]))
    elif policy == "enumerated_seeds":
        seeds = seed_policy.get("seeds")
        if not isinstance(seeds, list) or not seeds:
            raise AdapterSpecError("enumerated_seeds requires a non-empty seed list")
        rng = random.Random(str(tuple(int(seed) for seed in seeds)))
    else:
        raise AdapterSpecError("stochastic probe requires a deterministic seed policy")
    distribution = model.get("distribution", {})
    kind = distribution.get("kind")
    samples: list[float] = []
    for _ in range(sample_size):
        if kind == "bernoulli":
            probability = float(distribution["probability"])
            if not 0 <= probability <= 1:
                raise AdapterSpecError("Bernoulli probability must be within [0,1]")
            samples.append(float(rng.random() < probability))
        elif kind == "uniform":
            samples.append(rng.uniform(float(distribution["low"]), float(distribution["high"])))
        elif kind == "normal":
            sigma = float(distribution["sigma"])
            if sigma < 0:
                raise AdapterSpecError("normal sigma cannot be negative")
            samples.append(rng.gauss(float(distribution["mean"]), sigma))
        else:
            raise AdapterSpecError("unsupported preregistered distribution")
    estimate = statistics.fmean(samples)
    if uncertainty_method == "normal_95":
        standard_error = statistics.stdev(samples) / math.sqrt(sample_size) if sample_size > 1 else 0.0
        interval = {"method": "normal_95", "estimate": estimate, "standard_error": standard_error, "lower": estimate - 1.96 * standard_error, "upper": estimate + 1.96 * standard_error}
    elif uncertainty_method == "wilson_95" and kind == "bernoulli":
        z = 1.96
        denominator = 1 + z * z / sample_size
        centre = (estimate + z * z / (2 * sample_size)) / denominator
        half = z * math.sqrt(estimate * (1 - estimate) / sample_size + z * z / (4 * sample_size**2)) / denominator
        interval = {"method": "wilson_95", "estimate": estimate, "lower": max(0.0, centre - half), "upper": min(1.0, centre + half)}
    else:
        raise AdapterSpecError("uncertainty method is unsupported for the declared distribution")
    return samples, interval


def numeric_adapter(
    model: Mapping[str, Any],
    preregistration: Mapping[str, Any],
    seed_policy: Mapping[str, Any],
    governor: ResourceGovernor,
) -> dict[str, Any]:
    """Execute deterministic parameter sweeps or preregistered stochastic samples."""

    stochastic = bool(seed_policy.get("stochastic"))
    decision_rule = preregistration.get("decision_rule")
    if not isinstance(decision_rule, Mapping):
        raise AdapterSpecError("numeric probe requires a structured decision_rule")
    if stochastic:
        governor.checkpoint()
        samples, interval = _stochastic_samples(model, preregistration, seed_policy)
        holds = _decision(samples, decision_rule, interval)
        return {
            "status": "succeeded" if holds else "counterexample",
            "epistemic_outcome": "supports_within_scope" if holds else "falsifies_claim",
            "result": {"claim_holds": holds, "estimate": interval["estimate"], "sample_count": len(samples), "sample_digest_material": samples},
            "certificate": {"kind": "seeded_stochastic_replay", "seed_policy": dict(seed_policy), "sample_count": len(samples), "decision_rule": dict(decision_rule)},
            "uncertainty_analysis": interval,
            "completeness": {"complete": True, "scope": "preregistered finite sample plan", "stopping_rule": preregistration["stopping_rule"]},
        }
    expression = model.get("expression")
    if not isinstance(expression, str):
        raise AdapterSpecError("deterministic numeric probe requires expression")
    points = _grid(model)
    values: list[float] = []
    rows: list[dict[str, Any]] = []
    for point in points:
        governor.checkpoint()
        raw = safe_expression(expression, point, exact=False)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not math.isfinite(float(raw)):
            raise AdapterSpecError("numeric expression must produce a finite number")
        value = float(raw)
        values.append(value)
        rows.append({"parameters": point, "value": value})
    holds = _decision(values, decision_rule)
    return {
        "status": "succeeded" if holds else "counterexample",
        "epistemic_outcome": "supports_within_scope" if holds else "falsifies_claim",
        "result": {"claim_holds": holds, "samples": rows, "minimum": min(values), "maximum": max(values)},
        "certificate": {"kind": "deterministic_numeric_replay", "expression": expression, "decision_rule": dict(decision_rule), "points": len(points)},
        "uncertainty_analysis": {"kind": "floating_point", "absolute_tolerance": decision_rule.get("absolute_tolerance", 1e-12), "relative_tolerance": decision_rule.get("relative_tolerance", 1e-12), "does_not_establish_exact_equality": True},
        "completeness": {"complete": True, "scope": "declared finite parameter grid", "points": len(points)},
    }


def lean_adapter(model: Mapping[str, Any], governor: ResourceGovernor, work_directory: Path) -> dict[str, Any]:
    """Check an actual Lean source file when a Lean executable is available."""

    executable = shutil.which(str(model.get("executable", "lean")))
    if executable is None:
        return {
            "status": "capability_unavailable",
            "epistemic_outcome": "not_evaluated",
            "result": {"available": False, "capability": "lean"},
            "certificate": None,
            "uncertainty_analysis": None,
            "completeness": None,
        }
    source = model.get("source")
    proposition = model.get("proposition")
    if not isinstance(source, str) or not source.strip() or not isinstance(proposition, str) or not proposition.strip():
        raise AdapterSpecError("Lean adapter requires source and proposition")
    source_path = work_directory / "Probe.lean"
    source_path.write_text(source, encoding="utf-8")
    outcome = governor.run_process([executable, source_path.name], cwd=work_directory, role="solver")
    if outcome["status"] == "deadline_exhausted":
        status, epistemic = "deadline_exhausted", "not_evaluated"
    elif outcome["status"] != "succeeded":
        status, epistemic = "solver_failure", "not_evaluated"
    else:
        status, epistemic = "succeeded", "supports_within_scope"
    return {
        "status": status,
        "epistemic_outcome": epistemic,
        "result": {"available": True, "proposition": proposition, "process": outcome},
        "certificate": {"kind": "lean_kernel_checked", "source": source_path.name, "proposition": proposition, "executable": executable} if status == "succeeded" else None,
        "uncertainty_analysis": {"kind": "none_kernel_check"} if status == "succeeded" else None,
        "completeness": {"complete": status == "succeeded", "scope": "declared Lean proposition"},
    }


def execute_adapter(spec: Mapping[str, Any], governor: ResourceGovernor, work_directory: Path) -> dict[str, Any]:
    """Dispatch one validated experiment specification to an isolated adapter."""

    adapter = spec.get("adapter")
    model = spec.get("model", {})
    if not isinstance(model, Mapping):
        raise AdapterSpecError("model must be an object")
    try:
        if adapter == "exact":
            return exact_adapter(model, governor)
        if adapter == "sympy":
            return sympy_adapter(model, governor)
        if adapter == "finite_model":
            return finite_model_adapter(model, governor)
        if adapter in {"numeric", "sweep"}:
            return numeric_adapter(model, spec.get("preregistration", {}), spec.get("seed_policy", {}), governor)
        if adapter == "lean":
            return lean_adapter(model, governor, work_directory)
        if adapter == "hybrid":
            stages = model.get("stages")
            if not isinstance(stages, list) or len(stages) < 2:
                raise AdapterSpecError("hybrid adapter requires at least two stages")
            outputs = []
            for index, stage in enumerate(stages):
                if not isinstance(stage, Mapping) or stage.get("adapter") == "hybrid":
                    raise AdapterSpecError("hybrid stages must be non-hybrid adapter objects")
                child = dict(spec)
                child.update(stage)
                output = execute_adapter(child, governor, work_directory / f"stage-{index:02d}")
                outputs.append(output)
                if output["status"] not in {"succeeded", "counterexample"}:
                    break
            counterexample = any(row["status"] == "counterexample" for row in outputs)
            complete = len(outputs) == len(stages) and all(row["status"] in {"succeeded", "counterexample"} for row in outputs)
            if not complete:
                terminal = outputs[-1]
                status, epistemic = terminal["status"], "not_evaluated"
            else:
                status = "counterexample" if counterexample else "succeeded"
                epistemic = "falsifies_claim" if counterexample else "supports_within_scope"
            return {
                "status": status,
                "epistemic_outcome": epistemic,
                "result": {"stages": outputs, "all_stages_completed": complete},
                "certificate": {"kind": "hybrid_stage_chain", "stage_certificates": [row.get("certificate") for row in outputs]} if complete else None,
                "uncertainty_analysis": {"stage_uncertainties": [row.get("uncertainty_analysis") for row in outputs]},
                "completeness": {"complete": complete, "completed_stages": len(outputs), "planned_stages": len(stages)},
            }
    except BudgetExceeded as exc:
        return {
            "status": "deadline_exhausted" if exc.status == "deadline_exhausted" else "resource_exhausted",
            "epistemic_outcome": "not_evaluated",
            "result": {"budget_status": exc.status, "dimension": exc.dimension, "used": exc.used, "limit": exc.limit},
            "certificate": None,
            "uncertainty_analysis": None,
            "completeness": {"complete": False},
        }
    raise AdapterSpecError(f"unknown adapter: {adapter!r}")

