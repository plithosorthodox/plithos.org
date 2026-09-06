#!/usr/bin/env python3
"""Checks for the claim mechanism, which decides who may take a language.

Run it: python3 tools/next_job_selftest.py
"""
import datetime
import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("next_job", ROOT / "tools" / "next_job.py")
nj = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nj)


def hours_ago(n):
    return (nj.now() - datetime.timedelta(hours=n)).replace(microsecond=0).isoformat()


class FreshnessTests(unittest.TestCase):
    """A claim speaks for a lane that is still working, not still talking.

    The heartbeat fires only when a lane asks the queue, and a lane deep in a
    batch loop does not ask for hours. On 5 September four lanes were within an
    hour of being declared gone while committing work every few minutes.
    """

    def setUp(self):
        self.original = dict(nj._LAST_WORK)
        self.addCleanup(lambda: (nj._LAST_WORK.clear(), nj._LAST_WORK.update(self.original)))

    def claim(self, age_hours, lang="zh", kind="lives"):
        return {"lang": lang, "kind": kind, "name": nj.NAME[lang], "since": hours_ago(age_hours)}

    def set_work(self, when, lang="zh", kind="lives"):
        nj._LAST_WORK[(nj.KINDS[kind][0], lang)] = when

    def test_a_recent_claim_is_fresh_whatever_the_branch_shows(self):
        self.set_work(None)
        self.assertTrue(nj.fresh(self.claim(1)))

    def test_an_old_claim_whose_work_is_landing_is_fresh(self):
        self.set_work(nj.now() - datetime.timedelta(minutes=3))
        self.assertTrue(nj.fresh(self.claim(nj.STALE_HOURS + 6)))

    def test_an_old_claim_with_no_work_for_half_a_day_is_stale(self):
        self.set_work(nj.now() - datetime.timedelta(hours=nj.STALE_HOURS + 1))
        self.assertFalse(nj.fresh(self.claim(nj.STALE_HOURS + 1)))

    def test_a_claim_whose_language_was_never_written_is_stale_when_old(self):
        self.set_work(None)
        self.assertFalse(nj.fresh(self.claim(nj.STALE_HOURS + 1)))

    def test_a_kind_with_no_directory_falls_back_to_the_claim_alone(self):
        self.assertIsNone(nj.last_work("interface", "zh"))
        self.assertFalse(nj.fresh({"lang": "zh", "kind": "interface",
                                   "name": "Chinese", "since": hours_ago(nj.STALE_HOURS + 1)}))

    def test_the_branch_is_consulted_once_per_language(self):
        calls = []
        nj._LAST_WORK.clear()
        original = nj._git
        nj._git = lambda args, **kw: (calls.append(args), "")[1]
        try:
            nj.last_work("lives", "zh")
            first = len(calls)
            nj.last_work("lives", "zh")
            self.assertEqual(first, len(calls))
        finally:
            nj._git = original


class SharingTests(unittest.TestCase):
    """A spare lane joins a language rather than standing idle.

    On 6 September Chinese finished and lane B had nothing to take: four jobs,
    five lanes. The two lanes on one language are given opposite ends of the
    remaining list so they never hold the same saint.
    """

    def claim(self, lang="arc", kind="lives", from_end=False, age_hours=0.1):
        c = {"lang": lang, "kind": kind, "name": nj.NAME[lang],
             "since": hours_ago(age_hours)}
        if from_end:
            c["from_end"] = True
        return c

    def test_a_second_lane_may_share_but_only_from_the_far_end(self):
        existing = {"E": self.claim()}
        self.assertFalse(self.refused(existing, self.claim(from_end=True)))
        self.assertTrue(self.refused(existing, self.claim()))

    def test_a_third_lane_is_refused(self):
        existing = {"E": self.claim(), "B": self.claim(from_end=True)}
        self.assertTrue(self.refused(existing, self.claim(from_end=True)))
        self.assertTrue(self.refused(existing, self.claim()))

    def test_a_job_held_only_by_a_gone_lane_is_taken_outright(self):
        stale = self.claim(age_hours=nj.STALE_HOURS + 1)
        nj._LAST_WORK[(nj.KINDS["lives"][0], "arc")] = None
        self.addCleanup(nj._LAST_WORK.pop, (nj.KINDS["lives"][0], "arc"), None)
        self.assertFalse(self.refused({"E": stale}, self.claim()))

    def refused(self, existing, wanted):
        """Mirror save_claim's admission rule against a fixed claims table."""
        slot = "B" if "B" not in existing else "Z"
        others = [c for s, c in existing.items()
                  if s != slot and nj.fresh(c)
                  and (c.get("lang"), c.get("kind")) == (wanted.get("lang"), wanted.get("kind"))]
        return bool(others and not (wanted.get("from_end")
                                    and not any(c.get("from_end") for c in others)))

    def test_the_floor_keeps_the_two_ends_apart(self):
        self.assertGreaterEqual(nj.SHARE_FLOOR, 40)


if __name__ == "__main__":
    unittest.main(verbosity=2)
