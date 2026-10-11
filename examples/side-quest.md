---
status: learning
project: home-monitoring
created: 2026-10-11
size: 20 min
priority: high
seen: 2
progress: 3/6
tags: [sidequest, networking, firewall]
---
# Why firewalls only block new connections (conntrack)

## Where we met it
- 2026-10-11 - Blocked the cameras' internet in the router's Parental Control, but the vendor app could
  still stream them until the cameras were power-cycled.
- 2026-10-11 - Seen again: Tailscale warned about firewall mode (iptables vs nftables) while setting up the VPN.

## Why it matters
Explains a whole class of "my firewall rule doesn't work" bugs, and how NAT routers and Linux firewalls
decide what to let through.

## Learning checklist
- [x] Understand the concept: what connection tracking is and why stateful firewalls need it
- [x] Answer: why does an already-open connection survive a new block rule?
- [x] Try it hands-on: `sudo conntrack -L | head` on a Linux box (command broken down)
- [ ] Teach it back in your own words
- [ ] Flashcards created
- [ ] Mark done

## Notes
A stateful firewall remembers every connection it has allowed in a table (Linux: `conntrack`). New packets
are checked against the rules; packets belonging to a connection already in the table are usually waved
through by an early "ESTABLISHED, RELATED -> accept" rule. A new block rule therefore stops *new*
connections but not the ones already open - until they close, time out, or the table entry is flushed.

```
sudo conntrack -L | head
│    │         │    └ head: first 10 lines only
│    │         └ -L: list tracked connections
│    └ conntrack: the tool for the kernel's connection-tracking table
└ sudo: the table belongs to the kernel, so root is needed
```

## Your teach-back
*(your own explanation goes here)*
