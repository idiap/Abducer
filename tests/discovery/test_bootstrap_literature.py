# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exercise acquisition through a bounded host channel and its raw-byte replay."""
import base64
import copy
import json
from urllib.parse import urlsplit

import pytest

from agentic.discovery.bootstrap_literature import (
    acquire_current_literature, public_query_routes, reopen_acquisition,
)
from agentic.discovery.contracts import ContractError, canonical_digest


ARXIV = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
<id>http://arxiv.org/abs/2609.12345v1</id><title>A bounded target analysis</title>
<author><name>Research Author</name></author><published>2026-09-01T00:00:00Z</published>
<summary>The bounded model has an obstruction under explicitly stated assumptions.</summary>
</entry></feed>'''
CROSSREF = json.dumps({"status": "ok", "message-type": "work-list", "message": {"items": [{
    "DOI": "10.1234/bounded", "title": ["A related construction"],
    "author": [{"given": "Research", "family": "Author"}],
    "published": {"date-parts": [[2025, 8, 3]]}, "type": "journal-article",
    "abstract": "<jats:p>The construction applies only to a finite approximation.</jats:p>",
}]}}).encode()


class Channel:
    """Model the host's single-stream protocol, recording actual requested URLs."""
    def __init__(self, *, fail=False):
        self.urls = []
        self.active = None
        self.fail = fail

    def __call__(self, operation, **arguments):
        if operation == "open":
            assert self.active is None
            url = arguments["url"]
            self.urls.append(url)
            self.active = ARXIV if urlsplit(url).hostname == "export.arxiv.org" else CROSSREF
            if self.fail and "barriers" in url:
                self.active = b'{"status":"failed"}'
            return {"token": "stream"}
        assert arguments["token"] == "stream" and self.active is not None
        if operation == "read":
            data, self.active = self.active[:arguments["size"]], self.active[arguments["size"]:]
            return {"data": base64.b64encode(data).decode()}
        assert operation == "close"
        self.active = None
        return {"closed": True}


def acquire(tmp_path, channel=None):
    channel = channel or Channel()
    root = tmp_path / "acquisition"
    result = acquire_current_literature(target_id="target-example", run_id="run-example",
        theory_state_digest=canonical_digest({"state": 0}), topic="target physics",
        root=root, public_fetch=channel)
    return root, result, channel


def reopen(root, result, **overrides):
    args = {"expected_digest": result["manifest"]["content_digest"],
            "target_id": "target-example", "run_id": "run-example",
            "theory_state_digest": canonical_digest({"state": 0})}
    args.update(overrides)
    return reopen_acquisition(root, **args)


def test_six_actual_queries_normalize_and_reopen_without_new_time(tmp_path):
    root, result, channel = acquire(tmp_path)
    assert len(channel.urls) == len(set(channel.urls)) == 6
    snapshot = result["snapshot"]
    assert snapshot["provenance_mode"] == "live"
    assert snapshot["validation_status"] == "validated"
    assert snapshot["result_count"] == 2  # Same Crossref work observed in five lanes.
    assert all(not source["decision_relevant"] for source in snapshot["sources"])
    assert all(source["correction_status"] == "unknown" for source in snapshot["sources"])
    assert reopen(root, result) == snapshot
    assert len(channel.urls) == 6
    with pytest.raises(FileExistsError):
        acquire(tmp_path)


def test_failure_keeps_diagnostic_receipts_but_cannot_be_reopened(tmp_path):
    channel = Channel(fail=True)
    with pytest.raises(ContractError, match="acquisition failed"):
        acquire(tmp_path, channel)
    root = tmp_path / "acquisition"
    snapshot = json.loads((root / "snapshot.json").read_text())
    assert any(row["status"] == "failed" for row in snapshot["lane_receipts"])
    assert (root / "negative_results_barriers/response.raw").is_file()
    manifest = json.loads((root / "acquisition.json").read_text())
    with pytest.raises(ContractError, match="incomplete"):
        reopen(root, {"manifest": manifest})
    assert channel.active is None


def test_reopen_rejects_raw_tampering_and_other_run(tmp_path):
    root, result, _ = acquire(tmp_path)
    with pytest.raises(ContractError, match="identity"):
        reopen(root, result, run_id="another-run")
    raw = root / result["manifest"]["captures"][0]["response"]["path"]
    raw.write_bytes(raw.read_bytes().replace(b"finite", b"global"))
    with pytest.raises(ContractError, match="digest changed"):
        reopen(root, result)


def test_public_queries_constrain_endpoint_method_and_parameters():
    routes = public_query_routes()
    assert {row["url"] for row in routes} == {
        "https://api.crossref.org/works", "https://export.arxiv.org/api/query"}
    assert all(row["method"] == "GET" and row["read_only"] for row in routes)
    for row in routes:
        assert row["query_schema"]["additionalProperties"] is False
        assert row["body_schema"] is None


def test_reopen_rejects_manifest_symlink_even_with_matching_content(tmp_path):
    root, result, _ = acquire(tmp_path)
    manifest = root / "acquisition.json"
    retained = tmp_path / "retained.json"
    manifest.rename(retained)
    manifest.symlink_to(retained)
    with pytest.raises(ContractError, match="symlink"):
        reopen(root, result)
