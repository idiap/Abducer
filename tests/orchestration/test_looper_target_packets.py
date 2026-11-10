# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class LooperTargetPacketTests(unittest.TestCase):
    def test_pvsnp_target_packet_validates(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/validate_target_packets.py", "agentic/examples/targets/p-vs-np-target.json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("validated target p-vs-np-target", result.stdout)

    def test_target_packet_rejects_unknown_statement(self) -> None:
        import tempfile

        packet = json.loads((ROOT / "agentic/examples/targets/p-vs-np-target.json").read_text(encoding="utf-8"))
        packet["main_claim_ids"] = ["st.not.present"]
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad-target.json"
            bad.write_text(json.dumps(packet), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "agentic/scripts/validate_target_packets.py"), str(bad)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("main_claim_id not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
