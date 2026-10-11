---
name: flashcards
description: >
  Write flashcards and multiple-choice questions into the patient-senior
  learning hub in Obsidian Spaced Repetition format - command cards (task ->
  command) and concept cards. Used automatically after teaching, and manually
  via /flashcards [topic] to turn the session's learning into cards.
argument-hint: "[topic | session]"
---

# /flashcards

Decks live in the learning hub (`hub` from the session's patient-senior block or
`~/.config/patient-senior/config.json`):
- **Commands:** `<hub>/Flashcards/Commands/<Tool>.md` - one note per tool (`Docker.md`, `Git.md`, `SSH.md`, `Grep.md` ...).
- **Concepts:** `<hub>/Flashcards/Concepts/<Topic>.md` - one note per subject (`Networking.md`, `Audio.md`, `Docker.md` ...).

Without an argument, make cards from what was taught in this session that has no cards yet.

## Deck notes

The Spaced Repetition plugin builds decks from tags. A new deck note starts with:

```markdown
---
tags: [flashcards]
---
#flashcards/commands/docker

# Docker commands
```

Use `#flashcards/commands/<tool>` or `#flashcards/concepts/<topic>` (lower-case, hyphens for spaces). Append
new cards at the end, each separated from the next by one blank line.

## Card formats (Obsidian Spaced Repetition)

**Single-line** - front `::` back:

```
Show only the last 10 minutes of a container's logs::`docker logs --since 10m <container>`
```

**Multi-line** - front, a line containing only `?`, back. No blank lines inside a card:

```
What does `2>&1` do at the end of a command?
?
Sends stream 2 (stderr) to wherever stream 1 (stdout) is going, so a pipe or file receives errors too.
Without it, `| grep` never sees error messages.
```

**Multiple choice** - a multi-line card with the options on the front and the answer plus why on the back:

```
Which flag makes `docker logs` show only recent output by time?
A) --tail   B) --since   C) --follow   D) --until
?
**B) `--since`** - filters by time (`10m`, `2h`). `--tail` limits by line count, `--follow` streams new lines, `--until` sets an end time.
```

**Cloze** - hide the key part with `==highlight==`:

```
In `crop=w:h:x:y`, ==x and y== are the coordinates of the crop's top-left corner.
```

## Writing good cards

- **One fact per card.** Split anything with "and" into two cards.
- **Command cards go task -> command.** The front says what the user wants to achieve in plain words; the
  back gives the command and a one-line flag breakdown. Add the reverse (command -> meaning) only for
  commands whose syntax is the hard part.
- **Concept cards ask why/how, not definitions to memorise.** Prefer "Why does a new firewall rule not cut
  existing connections?" over "Define conntrack".
- Use the user's real context in examples (their containers, files and errors) - it makes recall stick.
- Prefer one multiple-choice card per concept, with plausible wrong options that reflect real misconceptions.
- **Never edit or delete `<!--SR:...-->` comments** - they hold the review schedule.
- Before adding, read the deck and skip cards that duplicate an existing one.

## Afterwards

Tell the user in one line per deck: `🃏 3 cards -> Commands/Docker`. If a side quest asked for flashcards,
tick that checklist item and update its `progress`.
