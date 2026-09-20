---
name: "practice-systems-audit"
description: "Inventory what is actually running in the practice: which tools, skills, workflows, and recurring tasks are live, broken, duplicated, or missing. Produces a keep, merge, cut, fix-next list. Use when the stack has accumulated and nobody is sure what is doing real work."
---

# Practice Systems Audit

Audit first. Evidence before opinion. The output is an inventory and a
keep, merge, cut, fix-next decision set, not a rebuild.

This is the E-Myth pass on the practice's own machinery: what jobs exist, who
holds each one, and which jobs nobody is holding.

Defer to `firm-context`.

## When to use

- The tool and subscription stack has grown and nobody knows what is used
- The same task is being done three different ways
- Something broke and it is unclear what depended on it
- Before building anything new, to check it does not already exist
- Quarterly hygiene

## Steps

### 1. Inventory the real surface

Read what is actually there before theorising about it. Group by surface.

- Skills and prompts in use
- Tools and subscriptions: ChatGPT, Claude, Genspark, Perplexity, PLAUD, and
  anything else being paid for
- Connected accounts and integrations
- Recurring tasks that a person performs manually on a schedule
- Documents that function as systems: trackers, templates, checklists

### 2. Classify each item

Do not blend these states. Most audit failures are a tool listed as live
because something references it.

- Live and verified in the last 30 days
- Configured but not verified recently
- Configured but broken
- Duplicated by something else on the list
- Paid for and unused
- Missing entirely: a job nobody holds

A reference in a skill file is not evidence a tool works. Evidence is a recent
successful use.

### 3. Find the overlaps

Where two things do the same job, name both, name what each does better, and
recommend one canonical lane.

### 4. Find the gaps

The more valuable half of the audit. Jobs that are getting done by Billy
personally because no system holds them. List them by hours consumed, not by
how interesting they are to fix.

### 5. Recommend

Keep, merge, cut, or fix next. One line each. Ranked by time recovered.

## Output format

```
SYSTEMS AUDIT
Date: [today]

Scoreboard
Live, unverified, broken, duplicated, unused, missing. Six numbers, one line.

Inventory
Table: Item | Surface | State | Last verified | What it does | Owner

Overlaps
Each overlap: the two items, what each does better, the recommended canonical
lane.

Gaps
Jobs nobody holds. Ranked by hours consumed per month. Who is absorbing each
one today.

Recommendations
Table: Item | Keep / Merge / Cut / Fix next | Why | First step | Owner

Cost
What is being paid for and not used. Monthly figure where known.

Unknowns
Anything that could not be verified. Never "None" unless it is true.
```

## Rules

- Start read-only. Do not change, merge, or cancel anything unless Billy asks in
  that turn.
- Never report a tool as live because a document mentions it. State the evidence.
- Never cancel, disconnect, or delete anything as part of an audit.
- Separate "not used" from "not verified". They lead to opposite decisions.
- Rank by time recovered, not by how broken something looks.
- Every recommendation names an owner: Billy, Sydney, or Jason. A recommendation
  with no owner is a gap, not a plan.
- Anything touching client data or firm systems is flagged for RBC DS review
  before it changes. Do not assume a tool is permitted.
- Never list credentials, tokens, or account identifiers in the output.
- Short sentences. Active voice. No emojis. No em dashes.
