"""Shared advisory hook fixture; never executed during provider discovery."""

import json
import sys

json.load(sys.stdin)
