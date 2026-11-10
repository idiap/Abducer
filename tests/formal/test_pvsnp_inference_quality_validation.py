# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "agentic/scripts/validate_pvsnp_inference_quality.py"
FIXTURES = ROOT / "agentic/fixtures/pvsnp_inference_quality"


def run_validator(*paths: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *map(str, paths)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


class PvsnpInferenceQualityValidationTests(unittest.TestCase):
    def test_valid_transfer_packet_passes(self) -> None:
        result = run_validator(FIXTURES / "valid_transfer_packet.json")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_packets_fail(self) -> None:
        for path in FIXTURES.glob("invalid_*_packet.json"):
            result = run_validator(path)
            self.assertNotEqual(result.returncode, 0, path.name)

    def test_validator_self_check_exercises_invalid_fixtures(self) -> None:
        result = run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("validated", result.stdout)


if __name__ == "__main__":
    unittest.main()
