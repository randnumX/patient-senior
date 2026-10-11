---
name: sidequest
description: >
  Save a side quest - a topic worth learning later that would derail the
  current task - as a note in the patient-senior learning hub, with a tailored
  learning checklist. Used automatically by patient-senior mode and manually
  via /sidequest <topic>. Also handles "not a side quest" removals.
argument-hint: "<topic> | remove <title>"
---

# /sidequest

The learning hub path is in the session's "patient-senior is ON" block, or `hub` in
`~/.config/patient-senior/config.json`. Notes live in `<hub>/Side Quests/`; the template is
`<hub>/Templates/Side Quest.md`.

## When to capture one automatically

Capture when a topic is worth real learning time **and** would derail the current task:
- a concept we used without truly explaining it;
- an alternative we did not choose (record why we chose the other);
- a warning or error we decided to ignore;
- behaviour that surprised us;
- a "what is X?" from the user that needs more than two sentences.

Do **not** capture what can be explained inline in one or two sentences - explain it instead.

## Steps

1. **Deduplicate.** List `<hub>/Side Quests/` and read frontmatter/titles. If the topic already exists
   (same concept, even if worded differently):
   - increment `seen`;
   - append a dated bullet under "## Where we met it";
   - if `seen` is now 2 or more, raise `priority` one step (low -> medium -> high);
   - if `status` is `done`, mention that the user already learned it and offer a quick refresher instead.
2. **Otherwise create** `<hub>/Side Quests/<Title>.md` from the template. Title: a short question or noun
   phrase a learner would search for, e.g. `Why firewalls only block new connections (conntrack)`. Avoid
   `/ \ : * ? " < > |` in file names. Fill in:
   - `status: open`, `project:` (current repo or folder name), `created:` (today, YYYY-MM-DD),
     `size:` (`quick` = under 10 min, `20 min`, `deep dive`), `priority:` (`high` if it blocks the user's
     understanding of their own system, `medium` by default, `low` for curiosity), `seen: 1`,
     `progress: 0/N`, `tags: [sidequest, <topic tags>]`.
   - **Where we met it** - one concrete sentence: what we were doing, what happened.
   - **Why it matters** - one or two sentences linking it to real work.
   - **Learning checklist** - 4-6 tailored items. Always start with understanding the concept, include the
     specific questions to answer and one hands-on item (a command to run or code to read), and always end
     with `Teach it back in your own words`, `Flashcards created`, `Mark done`. Set `progress: 0/N`.
3. **Tell the user in one line**, then continue the original task:
   `🧭 Side quest saved: "<title>" (<size>, <priority>)` or `🧭 Side quest seen again: "<title>" (seen 3x, now high)`.

## remove

`/sidequest remove <title>` or the user saying "not a side quest": delete the note (explain the action), confirm in one line.
