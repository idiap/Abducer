import tempfile
import unittest

from tdr.orchestration import DiscoveryEngine
from tdr.provenance import ArtifactStore, Repository


class PersistenceE2ETests(unittest.TestCase):
    def test_content_addressed_store_deduplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ArtifactStore(directory)
            first = store.put_json({"a": 1})
            second = store.put_json({"a": 1})
            self.assertEqual(first, second)
            self.assertEqual(store.get_json(first), {"a": 1})

    def test_repository_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Repository(directory)
            repo.save_record({"record_id": "x", "schema_version": "1.0", "lifecycle": "staged", "value": 3}, "example")
            self.assertEqual(repo.get_record("x")["value"], 3)

    def test_demo_reaches_synthesis_and_replays(self):
        with tempfile.TemporaryDirectory() as directory:
            engine = DiscoveryEngine(directory)
            outcome = engine.run_demo()
            self.assertEqual(outcome["phase"], "SYNTHESIZED")
            self.assertEqual(outcome["candidate_count"], 4)
            replay = engine.replay(outcome["run_id"])
            self.assertTrue(replay["verified"])


if __name__ == "__main__":
    unittest.main()

