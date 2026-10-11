#!/usr/bin/env python3
"""Learning statistics for a patient-senior hub (an Obsidian folder).

    stats.py [hub_path] [--json] [--today YYYY-MM-DD]

hub_path defaults to "hub" in ~/.config/patient-senior/config.json.
Counts side quests by status, flashcards per deck (with due and never-reviewed
cards from Spaced Repetition's <!--SR:...--> comments), sessions and streak,
and mastered items listed in Profile.md. Read-only.
"""
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

CONFIG = Path(os.environ.get("PATIENT_SENIOR_CONFIG", "~/.config/patient-senior/config.json")).expanduser()
SR_DATE = re.compile(r"!(\d{4}-\d{2}-\d{2})")
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[end + 4:]


def notes(folder):
    return sorted(p for p in folder.glob("**/*.md") if p.is_file()) if folder.is_dir() else []


def parse_date(value):
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def side_quests(hub, today):
    quests = []
    for path in notes(hub / "Side Quests"):
        meta, _ = frontmatter(path.read_text(errors="replace"))
        created = parse_date(meta.get("created", ""))
        quests.append({"title": path.stem, "status": meta.get("status", "open"),
                       "priority": meta.get("priority", "medium"), "seen": int(meta.get("seen") or 1),
                       "progress": meta.get("progress", ""),
                       "waiting_days": (today - created).days if created else None})
    by_status = {s: sum(q["status"] == s for q in quests) for s in ("open", "learning", "done")}
    up_next = sorted((q for q in quests if q["status"] != "done"),
                     key=lambda q: (PRIORITY_RANK.get(q["priority"], 1), -q["seen"], -(q["waiting_days"] or 0)))
    return {"total": len(quests), "by_status": by_status, "up_next": up_next[:5]}


def cards_in(text):
    """Return one list of scheduled dates per card (empty list = never reviewed)."""
    _, body = frontmatter(text)
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    cards = []
    for block in re.split(r"\n\s*\n", body):
        lines = [l for l in block.splitlines() if l.strip()]
        multi = any(l.strip() in ("?", "??") for l in lines)
        if multi:
            cards.append(SR_DATE.findall(block))
            continue
        for i, line in enumerate(lines):
            if "::" in line and not line.lstrip().startswith(("#", ">", "<!--")):
                dates = SR_DATE.findall(line)
                follow = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if not dates and follow.startswith("<!--SR:"):
                    dates = SR_DATE.findall(follow)  # schedule written on the line after the card
                cards.append(dates)
    return cards


def flashcards(hub, today):
    decks, total, due, new = [], 0, 0, 0
    for path in notes(hub / "Flashcards"):
        cards = cards_in(path.read_text(errors="replace"))
        if not cards:
            continue
        d_due = sum(any(parse_date(x) and parse_date(x) <= today for x in dates) for dates in cards)
        d_new = sum(not dates for dates in cards)
        decks.append({"deck": str(path.relative_to(hub / "Flashcards").with_suffix("")),
                      "cards": len(cards), "due": d_due, "new": d_new})
        total, due, new = total + len(cards), due + d_due, new + d_new
    return {"total": total, "due": due, "new": new, "decks": sorted(decks, key=lambda d: -d["cards"])}


def sessions(hub, today):
    days = set()
    count = 0
    for path in notes(hub / "Sessions"):
        meta, _ = frontmatter(path.read_text(errors="replace"))
        day = parse_date(meta.get("date", "")) or parse_date(path.stem)
        count += 1
        if day:
            days.add(day)
    streak, day = 0, today
    if day not in days:
        day -= dt.timedelta(days=1)
    while day in days:
        streak, day = streak + 1, day - dt.timedelta(days=1)
    last7 = sum(1 for d in days if 0 <= (today - d).days < 7)
    return {"total": count, "days_in_last_7": last7, "streak_days": streak}


def mastered(hub):
    profile = hub / "Profile.md"
    if not profile.is_file():
        return {"concepts": 0, "commands": 0}
    text = re.sub(r"<!--.*?-->", "", profile.read_text(errors="replace"), flags=re.S)
    counts, section = {"concepts": 0, "commands": 0}, None
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line.lower()
            if "concept" in heading:
                section = "concepts"
            elif "command" in heading:
                section = "commands"
            else:
                section = None
        elif section and re.match(r"\s*- \S", line):
            counts[section] += 1
    return counts


def gather(hub, today):
    return {"hub": str(hub), "date": today.isoformat(), "side_quests": side_quests(hub, today),
            "flashcards": flashcards(hub, today), "sessions": sessions(hub, today), "mastered": mastered(hub)}


def report(s):
    q, f, se, m = s["side_quests"], s["flashcards"], s["sessions"], s["mastered"]
    out = [f"Senior HQ - {s['date']}", "",
           f"Side quests   {q['total']} total: {q['by_status']['open']} open, "
           f"{q['by_status']['learning']} learning, {q['by_status']['done']} done"]
    for item in q["up_next"]:
        wait = f", waiting {item['waiting_days']}d" if item["waiting_days"] is not None else ""
        prog = f", {item['progress']}" if item["progress"] and item["status"] == "learning" else ""
        out.append(f"  - {item['title']} ({item['priority']}, seen {item['seen']}x{prog}{wait})")
    out += ["", f"Flashcards    {f['total']} cards, {f['due']} due now, {f['new']} never reviewed"]
    out += [f"  - {d['deck']}: {d['cards']} cards ({d['due']} due, {d['new']} new)" for d in f["decks"][:8]]
    out += ["", f"Sessions      {se['total']} total, {se['days_in_last_7']} of the last 7 days, "
                f"streak {se['streak_days']} day(s)",
            f"Mastered      {m['concepts']} concepts, {m['commands']} commands (from Profile.md)"]
    return "\n".join(out)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    today = dt.date.today()
    if "--today" in argv:
        today = dt.date.fromisoformat(argv[argv.index("--today") + 1])
        args = [a for a in args if a != argv[argv.index("--today") + 1]]
    hub = Path(args[0]).expanduser() if args else None
    if hub is None:
        try:
            hub = Path(json.loads(CONFIG.read_text())["hub"]).expanduser()
        except (OSError, ValueError, KeyError):
            sys.exit("No hub configured - run /senior-setup or pass the hub path.")
    if not hub.is_dir():
        sys.exit(f"Hub folder not found: {hub}")
    stats = gather(hub, today)
    print(json.dumps(stats, indent=2) if "--json" in argv else report(stats))


if __name__ == "__main__":
    main(sys.argv[1:])
