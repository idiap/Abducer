# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
import copy
import json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "agentic/spec/cohere_fast_artifacts.schema.json").read_text())
D = "sha256:" + "a" * 64


def packet():
    return {"artifact_type": "DomainEvidencePacket", "workflow_id": "cohere_fast", "domain_id": "ym", "run_id": "cf-0123456789abcdef01234567", "schema_version": "1.0", "claims": [{"claim": "bounded candidate", "status": "candidate", "ceiling": "candidate"}], "provenance": [{"archive_sha256": D, "member_path": "skills/programs/yang-mills/example", "member_sha256": D}], "integrity_status": "digest_verified", "proof_status": "candidate", "publication_status": "not_ready", "open_obligations": ["independent audit"]}


def test_domain_packet_retains_provenance_and_independent_status_dimensions():
    jsonschema.validate(packet(), SCHEMA)


def test_wrong_domain_or_unknown_status_fails_closed():
    bad = copy.deepcopy(packet()); bad["domain_id"] = "other"
    try: jsonschema.validate(bad, SCHEMA)
    except jsonschema.ValidationError: pass
    else: raise AssertionError("cross-domain packet accepted")
    bad = copy.deepcopy(packet()); bad["proof_status"] = "validated"
    try: jsonschema.validate(bad, SCHEMA)
    except jsonschema.ValidationError: pass
    else: raise AssertionError("unknown proof status accepted")
