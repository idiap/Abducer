---
name: review
description: Review source code and return structured findings.
allowed-tools: Read, Grep, Glob
---

Read `references/oracle.md`, inspect the requested files, and return a JSON
array of findings. Each finding has `path`, `severity`, and `summary`.
