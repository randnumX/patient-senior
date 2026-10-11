---
type: llm
weight: 1
---

There are several reasonable approaches (for example cron, a systemd timer, or logrotate). The agent
presents at least two of them with their trade-offs, gives a recommendation with a reason, and asks the user
to choose before committing to one. Picking one approach and only giving its instructions, without asking,
does not pass.
