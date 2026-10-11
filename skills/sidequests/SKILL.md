---
name: sidequests
description: >
  List open side quests from the patient-senior learning hub and work through
  one: teach it professor-style, tick its checklist, write the lesson into the
  note, run a teach-back, create flashcards and mark it done. Use for
  /sidequests, /sidequests <title>, "what side quests do I have", "teach me a side quest".
argument-hint: "[title or number]"
---

# /sidequests

Notes live in `<hub>/Side Quests/` (hub path from the session's patient-senior block or
`~/.config/patient-senior/config.json`).

## Without an argument: the list

Read every note's frontmatter and show a compact table of quests with `status` `open` or `learning`,
sorted by priority (high, medium, low), then `seen` (descending), then `created` (oldest first):

| # | Side quest | Size | Priority | Seen | Progress | Project |

Mention the count of `done` quests, and ask which one to take on now (number or title).
Remind them the same view lives in Obsidian: `Senior HQ` -> Side Quests.

## With a choice: learn it

1. Set `status: learning` in the note.
2. Work through the **Learning checklist** in order. For each item:
   - Teach it with the full professor sequence (why it exists, mental model, analogy, where it appeared in
     the user's real work - quote the "Where we met it" section - general principle, misconception, a
     check question). Wait for the user's answer to the check question and respond to it.
   - Hands-on items: explain and run the command (or have the user run it), with the full command
     breakdown from the patient-senior rules.
   - Tick the box (`- [ ]` -> `- [x]`) and update `progress: k/N` in the frontmatter.
   - Append the essence of the lesson to the note's `## Notes` section in the user-facing professor voice:
     short paragraphs, a diagram or table where it helps, the commands used with their breakdown.
3. **Teach-back.** Ask the user to explain the topic in their own words (3-5 sentences). Paste their answer
   verbatim under `## Your teach-back`, then give specific feedback: what is right, what is missing or
   wrong, one sentence on how a senior would phrase it. If something important is wrong, re-teach that
   part and ask once more.
4. **Flashcards.** Load the `flashcards` skill and create 3-6 cards for the topic; tick that item.
5. **Done.** Tick `Mark done`, set `status: done` and add `completed: <today>`. Add the concept to
   `<hub>/Profile.md` under "Known concepts" only if the teach-back passed.
6. Close with one line: what they can now do that they could not before.

The user can stop at any point; leave `status: learning` and the ticked progress so they can resume later.
