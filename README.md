# patient-senior

**The patient senior engineer you don't have.**

AI coding agents get the work done. They don't make *you* better at it.

- In **auto mode** the agent runs ten steps in a row. You get a result, but you can't explain how it got
  there - or what else it changed on the way.
- In **approval mode** it asks "run this?" but never says *why*. The reasoning stays in the model's head,
  and you approve commands you couldn't have written yourself.

patient-senior turns Claude Code into a pair programmer whose first job is your understanding. It is
always on, in auto mode and approval mode, every session.

## What changes

| Without | With patient-senior |
|---|---|
| Commands run with no explanation | Every action gets a **what / why / risk** pre-flight before it runs |
| `docker logs --since 10m frigate 2>&1 \| grep -i error` appears and works | The command is **broken down token by token**, with the general pattern, so you can write variations yourself |
| You never type the commands | **Recall challenges:** for commands you've met before, you write it first, then compare |
| The agent silently picks an approach | At real **decision points** you get the options, trade-offs and a recommendation - **you decide** |
| New concepts fly past | Taught like a great professor: why it exists, mental model, analogy, where it is in *your* code, principle, pitfall, check question |
| Interesting tangents derail the task - or get lost | Saved as **side quests** in Obsidian, with a learning checklist for later |
| You forget it all next week | **Flashcards and MCQs** written automatically for spaced repetition |
| "Senior" is a vague goal | A **senior lens** on the habits that matter: failure modes, blast radius, reversibility, tests, security |

## Example

```text
What: follow Frigate's log for errors from the last 10 minutes.
Why:  the camera dropped at 14:05; the log will say whether ffmpeg crashed or the network did.
Risk: read-only.

docker logs --since 10m frigate 2>&1 | grep -i error
│      │    │           │       │      │    └ -i: ignore case
│      │    │           │       │      └ grep: keep only matching lines
│      │    │           │       └ 2>&1: send stderr where stdout goes, so grep sees both
│      │    │           └ the container
│      │    └ --since 10m: only recent lines
│      └ logs: show a container's output
└ docker: the program

Pattern: docker logs [--since <time>] [--tail <n>] [-f] <container>

🃏 2 cards -> Commands/Docker
🧭 Side quest saved: "How Docker separates stdout and stderr" (quick, low)
```

## Install (Claude Code)

```bash
claude plugin marketplace add randnumX/patient-senior
claude plugin install patient-senior@patient-senior
```

Then start a new Claude Code session and run:

```text
/senior-setup
```

Setup picks the Obsidian vault folder that becomes your **learning hub**, copies in *Senior HQ* and writes
`~/.config/patient-senior/config.json`. From the next session on, the mode switches itself on.

Requirements: Claude Code, `python3` (for the start-of-session hook), Obsidian with the core **Bases**
plugin and the community **Spaced Repetition** plugin for reviewing cards.

## Commands

| Command | What it does |
|---|---|
| `/senior` | The mode itself. `light` / `full` / `deep` / `off` for this session, `status`, `default <level>` to persist |
| `/senior-setup` | Choose the vault folder, create Senior HQ, write the config |
| `/sidequest <topic>` | Park a topic for later (also happens automatically) |
| `/sidequests` | List open side quests, pick one, learn it with a checklist, teach-back and cards |
| `/flashcards [topic]` | Turn what you learned into Spaced Repetition cards and MCQs |
| `/quiz [topic]` | Interactive quiz: MCQs and write-the-command recall, one question at a time |
| `/recap` | Session note in Obsidian: what we did and why, commands, your decisions, concepts, next steps |
| `/senior-init` | Write the rules into AGENTS.md, Copilot, Cursor, Windsurf and Cline instruction files |

Plugin skills may also appear as `/patient-senior:<name>`.

**Pairs with [command-anatomy](https://github.com/randnumX/command-anatomy)** - install it too and every command
breakdown becomes a perfectly aligned anatomy tree (`/explain <command>` works on its own as well).

## Levels

| Level | For | Feels like |
|---|---|---|
| `light` | Familiar territory | One-line why per action; breakdowns only for flags you haven't seen |
| `full` (default) | Everyday work | Pre-flights, every command broken down, professor-style teaching for new concepts, debriefs |
| `deep` | Learning a new field on purpose | Everything, plus analogies, misconceptions, frequent recall challenges and teach-backs |

## Senior HQ - your learning hub in Obsidian

```text
<vault>/Senior/
├── Senior HQ.md          ← the root page: live tables of everything below
├── Side Quests.base      ← Open / In progress / By project / Done
├── Sessions.base         ← every /recap, newest first
├── Side Quests/          ← one note per side quest, with a checklist the agent ticks as you learn
├── Sessions/             ← one note per session
├── Flashcards/
│   ├── Commands/         ← one deck per tool: Docker.md, Git.md, SSH.md ...
│   └── Concepts/         ← one deck per subject
├── Profile.md            ← what you've demonstrably mastered (so it stops re-teaching it)
└── Templates/
```

A side quest looks like [examples/side-quest.md](examples/side-quest.md): where you met it, why it
matters, and a learning checklist that ends with **teaching it back in your own words**.

## How it works

- `rules/senior-core.md` holds the always-on rules (about 900 words).
- A `SessionStart` hook (`hooks/senior_activate.py`) injects them into every session, filled in with your
  hub path and level. A `SubagentStart` hook tells helper agents to return a teachable report of every
  action and command, since you never see their intermediate steps.
- Each `/command` is a skill in `skills/` - plain Markdown instructions you can read and change.

## Honest limitations

- Skills and rules are **instructions, not enforcement**. The model follows them closely, but it is not a
  guarantee. A future version may add a `PreToolUse` hook that blocks unexplained commands.
- Teaching costs tokens. `light` keeps it cheap; `off` pauses it.
- The learning hub assumes Obsidian. Without it, the mode still explains and teaches; only the notes and
  cards have nowhere to go.

## Roadmap

- Enforcement hook for unexplained commands
- Mastery statistics in Senior HQ
- Anki export for flashcards
- Other agents: Codex, Gemini CLI, Copilot agent mode
- APM package

## License

[MIT](LICENSE)
