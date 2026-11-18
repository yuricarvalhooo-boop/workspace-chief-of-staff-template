import datetime
import unittest

from scripts import search


class SearchRankingTests(unittest.TestCase):
    def test_maintained_sources_rank_before_session_evidence(self):
        decision = search.source_priority("knowledge/decisions/DEC-001-x.md", None, {}, None, None, False)
        project = search.source_priority("knowledge/projects/projeto-x.md", None, {}, "projeto-x", None, False)
        roadmap = search.source_priority("knowledge/roadmap/projeto-x.md", None, {}, "projeto-x", None, False)
        checkpoint = search.source_priority("knowledge/conversations/projeto-x/2026-10-19-x.md", None, {}, None, None, False)
        meeting = search.source_priority("meetings/2026-10-01-x.md", None, {}, None, None, False)

        self.assertEqual(decision, 0)
        self.assertEqual(project, 0)
        self.assertEqual(roadmap, 0)
        self.assertLess(decision, checkpoint)
        self.assertEqual(checkpoint, meeting)

    def test_historical_status_and_archive_rank_last(self):
        historical_note = search.source_priority("knowledge/projects/x.md", None, {"status": "historico"}, None, None, False)
        archive = search.source_priority("archive/x.source.txt", {"historical": True}, {}, None, None, True)

        self.assertEqual(historical_note, 6)
        self.assertEqual(archive, 7)

    def test_superseded_statuses_are_detected(self):
        for status in ("substituída", "substituida", "Superada", "obsoleta"):
            self.assertTrue(search.superseded({"status": status}), status)
        self.assertFalse(search.superseded({"status": "aceita"}))
        self.assertFalse(search.superseded({}))

    def test_expired_only_after_the_date(self):
        today = datetime.date(2026, 10, 19)

        self.assertTrue(search.expired({"expires": "2026-10-18"}, today))
        self.assertFalse(search.expired({"expires": "2026-10-19"}, today))
        self.assertFalse(search.expired({"expires": "data-invalida"}, today))
        self.assertFalse(search.expired({}, today))


if __name__ == "__main__":
    unittest.main()
