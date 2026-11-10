"""Minimal dependency-free JSON API. Bind to loopback by default."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
from typing import Any

from tdr.orchestration import DiscoveryEngine
from tdr.skills import list_skills


def make_handler(engine: DiscoveryEngine):
    class Handler(BaseHTTPRequestHandler):
        server_version = "TDR/0.1"

        def _send(self, status: int, value: Any) -> None:
            data = json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _body(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            value = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(value, dict):
                raise ValueError("request body must be an object")
            return value

        def do_GET(self) -> None:
            try:
                if self.path == "/health":
                    self._send(200, {"status": "ok"})
                elif self.path == "/skills":
                    self._send(200, list_skills())
                elif match := re.fullmatch(r"/runs/([^/]+)", self.path):
                    self._send(200, engine.inspect(match.group(1)))
                elif match := re.fullmatch(r"/contexts/([^/]+)/frontier", self.path):
                    records = engine.repository.list_records("portfolio")
                    self._send(200, {"context_id": match.group(1), "portfolios": records})
                else:
                    self._send(404, {"error": "not_found"})
            except (KeyError, ValueError) as error:
                self._send(400, {"error": type(error).__name__, "message": str(error)})

        def do_POST(self) -> None:
            try:
                body = self._body()
                if self.path == "/contexts":
                    state = engine.create_run()
                    result = engine.execute(state.run_id, "scope-research-context", body)
                    self._send(201, {"run_id": state.run_id, "result": result})
                elif self.path == "/runs":
                    state = engine.create_run(str(body.get("context_id", "pending-context")), body.get("budget"))
                    self._send(201, {"run_id": state.run_id, "phase": state.phase})
                elif match := re.fullmatch(r"/runs/([^/]+)/skills/([^/]+)", self.path):
                    self._send(200, engine.execute(match.group(1), match.group(2), body))
                elif match := re.fullmatch(r"/candidates/([^/]+)/validations", self.path):
                    candidate = engine.repository.get_record(match.group(1))
                    state = engine.create_run(str(body.get("context_id", "validation-only")))
                    skill_name = str(body.pop("skill", "falsify-candidate"))
                    self._send(200, engine.execute(state.run_id, skill_name, {**body, "candidate": candidate}))
                else:
                    self._send(404, {"error": "not_found"})
            except (KeyError, ValueError, json.JSONDecodeError) as error:
                self._send(400, {"error": type(error).__name__, "message": str(error)})

        def log_message(self, format: str, *args: Any) -> None:
            return

    return Handler


def serve(project: str, host: str = "127.0.0.1", port: int = 8765) -> None:
    engine = DiscoveryEngine(project)
    server = ThreadingHTTPServer((host, port), make_handler(engine))
    print(f"TDR API listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

