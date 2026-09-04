import concurrent.futures
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import check_i18n
import next_job
from translation_checks import validate_pairs


class InterfaceEvaluationTests(unittest.TestCase):
    def test_concurrent_evaluations_do_not_collide(self):
        literals = ['{"worker":%d,"text":"value %d"}' % (i, i) for i in range(32)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(check_i18n.evaluate, literals))
        for i, (value, error) in enumerate(results):
            self.assertIsNone(error)
            self.assertEqual({"worker": i, "text": "value %d" % i}, value)
        self.assertEqual([], list(TOOLS.glob("*.i18n-eval.js")))


class QueueDependencyTests(unittest.TestCase):
    def queue_with(self, terms, lives, entries, interface=0):
        counts = {("terms", "el"): terms, ("lives", "el"): lives}
        with mock.patch.object(next_job, "LANGS", ["el"]), \
                mock.patch.object(next_job, "written",
                                  side_effect=lambda kind, lang: counts[(kind, lang)]), \
                mock.patch.object(next_job, "entries_published",
                                  return_value={"el": (entries, 1456)}), \
                mock.patch.object(next_job, "interface_remaining",
                                  return_value={"el": (interface, 342)}):
            return [job["kind"] for job in next_job.queue()]

    def test_vocabulary_gates_all_later_work(self):
        self.assertEqual(["terms"], self.queue_with(10631, 0, 0))

    def test_lives_gate_entries(self):
        self.assertEqual({"interface", "lives"},
                         set(self.queue_with(10632, 1455, 0)))

    def test_entries_eligible_only_after_lives(self):
        self.assertIn("entries", self.queue_with(10632, 1456, 0))

    def test_entry_job_uses_the_info_loop_kind(self):
        command = next_job.command({"kind": "entries", "lang": "el"})
        self.assertIn("tools/loop.py info el", command)
        self.assertNotIn("tools/loop.py entries", command)


class ClaimTests(unittest.TestCase):
    def test_pick_hard_stops_when_claim_cannot_be_published(self):
        job = {"lang": "el", "kind": "terms", "name": "Greek"}
        with mock.patch.object(next_job, "synchronized_claims", return_value={}), \
                mock.patch.object(next_job, "save_claim",
                                  side_effect=next_job.ClaimError("rejected")):
            with self.assertRaises(next_job.ClaimError):
                next_job.pick("A", [job])

    def test_pick_returns_job_only_after_confirmed_claim(self):
        job = {"lang": "el", "kind": "terms", "name": "Greek"}
        with mock.patch.object(next_job, "synchronized_claims", return_value={}), \
                mock.patch.object(next_job, "save_claim", return_value=True) as save:
            self.assertEqual((job, True), next_job.pick("A", [job]))
            save.assert_called_once()


class TranslationChecksTests(unittest.TestCase):
    def test_deterministic_translation_guards(self):
        errors = validate_pairs("el", [
            ("blank", "Source", " "),
            ("placeholder", "Source", "TODO"),
            ("fallback", "English source", "English source"),
            ("script", "Source", "Latin only"),
            ("reference", "John 3:16, 4th century", "Ἰωάννης 3:17, αἰών"),
            ("short", "A " * 50, "κ"),
            ("duplicate-a", "A sufficiently long first English source sentence", "ἡ αὐτὴ μακρὰ μετάφραση"),
            ("duplicate-b", "A different and sufficiently long English sentence", "ἡ αὐτὴ μακρὰ μετάφραση"),
        ])
        joined = "\n".join(errors)
        for expected in ("blank", "placeholder", "fallback", "native-script",
                         "numbers/dates/references", "truncated", "duplicate"):
            self.assertIn(expected, joined)


if __name__ == "__main__":
    unittest.main()
