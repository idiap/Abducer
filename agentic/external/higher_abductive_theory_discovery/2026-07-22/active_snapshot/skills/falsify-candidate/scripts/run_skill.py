#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()
command = [sys.executable, "-m", "tdr.api.cli", "run-skill", "falsify-candidate", "--input", args.input, "--pretty"]
try:
    raise SystemExit(subprocess.call(command))
except FileNotFoundError:
    print(json.dumps({"status": "blocked", "artifacts": [], "claims": [], "uncertainties": [{"reason": "tdr runtime unavailable"}], "next": [{"action": "install higher-abductive-theory-discovery"}], "provenance": {}}))
    raise SystemExit(2)
