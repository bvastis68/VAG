# Phone updates (call_me)

To phone Billy with a status update: `./call_me "short message"` (needs BLAND_API_KEY).

- Only calls +14165680554. Hard-coded; there is no way to target another number.
- Max 5 calls/day (Toronto time). Every call and its cost is logged to `calls.log`.
- NEVER put client names, account numbers, holdings, or dollar amounts in a call.
  The script refuses messages that look like client data; client names to block go
  in `call_me.blocklist` (one per line, gitignored).
- Use `./call_me --dry-run "..."` to check a message without dialing.
- Calls cost money. Only call for updates Billy asked to be phoned about.
