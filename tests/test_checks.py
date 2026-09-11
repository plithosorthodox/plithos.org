"""The guards that outlived the translation.

Two of these tests were written while five lanes were writing at once and the
queue that fed them needed proving. The queue is gone; what it proved about
these two is not. `check_i18n.evaluate` shells out to node and once wrote its
scratch file to a fixed name, so two callers at the same moment read each
other's answer, and `validate_pairs` is the only thing standing between a
rendering and the file it is appended to.
"""
import concurrent.futures
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import check_i18n
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
