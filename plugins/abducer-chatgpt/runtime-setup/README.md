# Runtime setup

For operators of the Abducer host. Install all locked project and ChatGPT dependencies with `python runtime-setup/setup_runtime.py --environment /absolute/writable/abducer-env`. Use a dedicated environment outside the installed plugin and source tree. The uv executable is required. Repeat the command to audit/synchronize the same lock; it never starts research.

For automatic dependency setup before each service start, add `--source-root /absolute/abducer-source --launch bridge -- --host 127.0.0.1 --port 8766`. Use `--launch worker` for the worker, or `--launch server` for the standalone MCP service. A separately released integration can be selected with `--code-root /absolute/integration-release`. The launcher installs/checks dependencies, then runs the selected process in that environment.

The managed interpreter is bound to PATH, PYTHON and VIRTUAL_ENV, with user site packages disabled. Versioned receipts and startup checks cover the full marked dependency graph, including PDF ingestion. After deployment, run `python -m integrations.chatgpt.verify_environment --source-root /absolute/abducer-source` with the managed Python to exercise child interpreter resolution, numerical/symbolic operations and canonical PDF extraction.

Run the service/bridge and worker with that environment's Python. On startup they eagerly import the supported runtime libraries and load all canonical skill directories, workflow manifests and declared supporting sources. This requires the separately deployed canonical Abducer source snapshot; this client ZIP does not contain a scientific executor. Docker builds install the same dependency group.

Onboarding reads `get_capabilities.dependency_setup`; the Sites plugin exposes the same status through `get_profile` and `get_execution_capabilities`. Missing sources, identities and authored research inputs stay explicit. Preloading does not qualify additional executors or place all source text in model context.
