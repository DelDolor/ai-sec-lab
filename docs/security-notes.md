# Security Notes for Contributors

**This is a public repository.** These rules are hard requirements, not suggestions.

---

## What Must Never Be Committed

| Category | Examples |
|---|---|
| Secrets and credentials | API keys, tokens, passwords, JWT secrets, private keys |
| Network details | IP addresses, hostnames, internal DNS names, VPN configs |
| Personal information | Names, emails, phone numbers, usernames tied to real people |
| Real documents | PDFs, Word files, text files with actual content |
| Real logs | Application logs, SIEM events, audit trails from a real system |
| Home lab details | Device names, network topology, router config, MAC addresses |

---

## Where Configuration Lives

- **`.env.example`** — placeholder values only (e.g., `changeme`, `localhost`, `local-user`)
- **`.env`** — real values; gitignored; never commit this file
- **`observability/examples/*.jsonl`** — synthetic events only; no real hostnames, IPs, or user data

---

## Before Every Commit

Run these checks before staging files:

```bash
# Review what you are about to commit
git status
git diff --staged

# Check for accidentally staged sensitive files
git diff --staged --name-only | grep -E '\.(env|pem|key|log|pdf|jsonl)$'

# Check for secrets in staged content (requires gitleaks installed separately)
gitleaks detect --staged

# Alternative: trufflehog
trufflehog git file://. --since-commit HEAD --only-verified
```

> Neither `gitleaks` nor `trufflehog` is installed automatically. Install one locally before pushing to a remote.

---

## Synthetic Data Rules

When adding example logs, events, or test fixtures:

- Use `local-user` for any user identifier
- Use `example-session-id` for session identifiers
- Use `localhost` for hostnames
- Use `doc-example-001` style identifiers for document IDs
- Use RFC 3339 timestamps with a fixed date (e.g., `2026-01-01T00:00:00Z`)
- Never use real IP addresses — use `127.0.0.1` or `192.0.2.x` (TEST-NET per RFC 5737)

---

## PDF and Document Files

- `data/documents/`, `data/poisoned-docs/`, and `data/uploads/` are gitignored
- Never add real PDFs to `tests/fixtures/` without explicit review
- Synthetic test fixtures in `tests/fixtures/` must contain only generated or clearly fictional content

---

## If You Accidentally Commit a Secret

1. Do **not** push.
2. Remove the secret from the file.
3. Use `git reset HEAD~1` to undo the commit (before push).
4. If already pushed: rotate the secret immediately, then use `git filter-repo` or contact GitHub support to remove it from history.
5. Assume the secret is compromised regardless of how quickly it was removed.
