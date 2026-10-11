"""Run with: python3 -m unittest discover -s tests"""
import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "senior-stats" / "scripts"))
from stats import gather, report  # noqa: E402

TODAY = dt.date(2026, 10, 11)
DECK = """---
tags: [flashcards]
---
#flashcards/commands/docker

# Docker commands

Show the last 10 minutes of a container's logs::`docker logs --since 10m <c>`

Follow a container's logs live::`docker logs -f <c>`
<!--SR:!2026-10-09,3,250-->

What does `2>&1` do?
?
Sends stderr to wherever stdout goes.
<!--SR:!2026-10-20,9,270-->

Which flag filters `docker logs` by time?
A) --tail  B) --since
?
**B) --since**

```bash
echo "not::a card inside a code block"
```
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def quest(status, priority, seen, created):
    return f"---\nstatus: {status}\npriority: {priority}\nseen: {seen}\ncreated: {created}\nprogress: 2/6\ntags: [sidequest]\n---\n# q\n"


class StatsTest(unittest.TestCase):
    def setUp(self):
        self.hub = Path(tempfile.mkdtemp()) / "Senior"
        write(self.hub / "Side Quests" / "Conntrack.md", quest("open", "high", 2, "2026-10-01"))
        write(self.hub / "Side Quests" / "Systemd timers.md", quest("open", "medium", 1, "2026-10-10"))
        write(self.hub / "Side Quests" / "MSE vs WebRTC.md", quest("learning", "medium", 1, "2026-10-05"))
        write(self.hub / "Side Quests" / "H264 levels.md", quest("done", "low", 1, "2026-09-01"))
        write(self.hub / "Flashcards" / "Commands" / "Docker.md", DECK)
        for day in ("2026-10-09", "2026-10-10", "2026-10-11"):
            write(self.hub / "Sessions" / f"{day} home - work.md", f"---\ndate: {day}\ntags: [senior-session]\n---\n")
        write(self.hub / "Profile.md", "## Known concepts\n<!-- - example - date -->\n- conntrack\n- RMS vs dBFS\n"
                                       "## Known commands\n- `docker logs --since`\n## Learning now\n- WebRTC\n")
        self.stats = gather(self.hub, TODAY)

    def test_side_quests(self):
        q = self.stats["side_quests"]
        self.assertEqual(q["by_status"], {"open": 2, "learning": 1, "done": 1})
        self.assertEqual(q["up_next"][0]["title"], "Conntrack")
        self.assertEqual(q["up_next"][0]["waiting_days"], 10)

    def test_flashcards_due_and_new(self):
        f = self.stats["flashcards"]
        self.assertEqual((f["total"], f["due"], f["new"]), (4, 1, 2))
        self.assertEqual(f["decks"][0]["deck"], "Commands/Docker")

    def test_sessions_streak(self):
        self.assertEqual(self.stats["sessions"], {"total": 3, "days_in_last_7": 3, "streak_days": 3})

    def test_mastered_ignores_comments_and_other_sections(self):
        self.assertEqual(self.stats["mastered"], {"concepts": 2, "commands": 1})

    def test_report_renders(self):
        text = report(self.stats)
        self.assertIn("4 cards, 1 due now, 2 never reviewed", text)
        self.assertIn("streak 3 day(s)", text)


if __name__ == "__main__":
    unittest.main()
