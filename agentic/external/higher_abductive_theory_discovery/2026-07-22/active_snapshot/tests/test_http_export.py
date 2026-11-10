from http.server import ThreadingHTTPServer
import json
import tempfile
from threading import Thread
import unittest
from urllib.request import urlopen

from tdr.api.http import make_handler
from tdr.export import export_candidate
from tdr.orchestration import DiscoveryEngine


class HttpExportTests(unittest.TestCase):
    def test_loopback_health_and_skill_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(DiscoveryEngine(directory)))
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                host, port = server.server_address
                with urlopen(f"http://{host}:{port}/health", timeout=3) as response:
                    self.assertEqual(json.load(response), {"status": "ok"})
                with urlopen(f"http://{host}:{port}/skills", timeout=3) as response:
                    self.assertEqual(len(json.load(response)), 17)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)

    def test_latex_export_escapes_candidate_text(self):
        output = export_candidate({"candidate_id": "c_1", "title": "A & B", "formal_move": "x_{1} % y"}, "latex")
        self.assertIn(r"A \& B", output)
        self.assertIn(r"x\_\{1\} \% y", output)
        self.assertTrue(output.endswith("\\end{document}"))


if __name__ == "__main__":
    unittest.main()
