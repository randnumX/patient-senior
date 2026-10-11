---
name: recap
description: >
  End-of-session recap for patient-senior: write a session note to the Obsidian
  learning hub (goal, what was done and why, commands used, decisions the user
  made, concepts learned, side quests and cards created, next steps) and give a
  short spoken summary with recall questions. Use for /recap, "summarise the
  session", "what did we do today".
argument-hint: "[short session title]"
---

# /recap

1. **Gather** from this session: the goal, each chunk of work, every shell command run, every decision
   point and what the user chose, concepts taught, side quests saved (🧭) and cards created (🃏).
2. **Write** `<hub>/Sessions/<YYYY-MM-DD> <project> - <title>.md` from `<hub>/Templates/Session.md`
   (append ` (2)` if the name exists). Fill every section:
   - **Goal** - one sentence.
   - **What we did and why** - a numbered timeline; each item = action + reason + result.
   - **Commands used** - a table: command | what it does | deck it was added to.
   - **Decisions you made** - option chosen, the alternatives, the reason. These are the moments the user
     acted as the senior; make them visible.
   - **Concepts learned** - with links to concept decks.
   - **Side quests saved** - wiki-links to the notes (`[[Title]]`).
   - **Open threads / next steps.**
   - Frontmatter: `date`, `project`, `tags: [senior-session]`, `commands: <count>`, `cards: <count>`,
     `sidequests: <count>`.
3. **Say it** in chat in five lines or fewer: what was built, the one most important concept, the decisions
   the user made, where the note is.
4. **Close with three recall questions** (at least one "write the command"), without answers - answers
   come only if the user replies or runs `/quiz`.
