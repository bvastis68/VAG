---
name: "knowledge-ops"
description: "Decide where a piece of information belongs, keep one canonical home per fact, and stop the practice accumulating five versions of the same document. Use when saving, organising, syncing, or hunting for practice knowledge across Drive, email, trackers, and memory."
---

# Knowledge Ops

One canonical home per fact. Everything else points at it. The failure mode this
prevents is five versions of the same tracker, three of them wrong.

Defer to `firm-context`. Use `practice-memory` for session-level working state.

## When to use

- Saving something and not knowing where it goes
- Looking for a document and finding three versions of it
- Onboarding a new process and deciding where its truth lives
- Cleaning up after a busy period

## The layers

| Layer | Holds | Canonical for |
|---|---|---|
| Firm systems | Client records, holdings, KYC, compliance files | Everything client-specific. Always. |
| Google Drive | Trackers, one-pagers, decks, client letters, research | Documents and deliverables |
| `firm-context` skill | Permanent practice facts: taxonomy, policy, house view, style | How the practice operates |
| `practice-memory` | Decisions, preferences, working state, handoffs | Why something was decided |
| Session context | The current conversation | Nothing. Session context is not storage. |

## Steps

### 1. Classify

Ask what kind of fact this is before deciding where it goes.

- Client-specific: firm systems. Nothing else. Never a local file, never memory.
- A deliverable or a tracker: Drive, with a date in the filename.
- How the practice operates: `firm-context`. Update the skill, do not write a
  note about it.
- Why a decision was made: `practice-memory`.
- Research output: Drive, with sources and date attached.

### 2. Deduplicate

Search before creating. If it already exists, update it. If a newer version
exists elsewhere, the older one gets marked superseded, not deleted.

Trackers are rebuilt whole, never edited in fragments. This is the
`bd-pipeline-review` rule and it applies everywhere.

### 3. Store

Write to exactly one canonical location. Everything else links to it.

### 4. Index

If the thing lives in a set, update the set's index. An unindexed document is a
lost document.

## Output format

```
KNOWLEDGE OPERATION

Item: [what]
Classification: [which layer, and why]
Canonical location: [exactly where]
Duplicates found: [what else exists, and what happens to it]
Index updated: [yes / no / not applicable]
Redactions applied: [what was stripped before storing]
```

## Rules

- Client personal information never leaves firm systems. Not into Drive notes,
  not into memory, not into a skill file, not into a repository. This is not a
  preference.
- Redact before storing. Names, account numbers, holdings, figures.
- Never create a second copy of a fact that lives somewhere authoritative. Link
  to it.
- Filenames are lowercase, hyphenated, and dated.
- Every stored research document carries its sources and the date it was
  gathered.
- A document with no owner and no date is treated as unverified.
- Never commit practice knowledge, client information, or voice samples into a
  git repository.
- Short sentences. No emojis. No em dashes.
