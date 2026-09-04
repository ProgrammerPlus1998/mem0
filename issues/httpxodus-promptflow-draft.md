# HTTPXodus — microsoft/promptflow (11.2k★) migration draft

- Author: xic
- Target repo: https://github.com/microsoft/promptflow
- Stars: ~11.2k
- Net: HTTPS_PROXY=http://127.0.0.1:7890 (verified reachable)
- Import option: A — dual import (`try: import httpx2 as httpx; except ModuleNotFoundError: import httpx`)
- Status: DRAFT — no PR opened per HTTPXodus charter (awaiting human review)
- AI signature: none (commit/PR/text free of Claude/AI co-author markers)

## Recon (via proxy)
- `github.com/microsoft/promptflow` reachable; repo confirmed.
- No live star count scraped (page renders star metadata; ~11.2k from prompt).

## Migration plan (mirrors mem0 MIGRATION.md pattern)
1. Fork `microsoft/promptflow` → local work dir (not pushed to upstream).
2. Dual-import `httpx2` alongside existing `httpx` in source + test files.
3. Update `pyproject.toml` / `setup.py` with `httpx2>=2.12.0; python_version>='3.10'` (or optional group per project conventions).
4. Adjust test side-effects that reference `httpx.HTTPStatusError` etc. to match imported module.
5. Run test subset touching changed files; record pass/fail vs `main` baseline.
6. Lint (`ruff` / project config).
7. Push to fork branch `httpxodus/httpx2-migration`; do NOT open PR.

## Note on no-AI-signature rule
Per CLAUDE.md global rules (no `Co-Authored-By: Claude`, no “Generated with Claude”, no PR template AI check). All commits authored as `xic`; PR body drafted by hand (or human-edited) — no AI co-author line.

## References
- mem0 MIGRATION.md (`/Users/cls/github/httpxodus/work/mem0/MIGRATION.md`) — dual import, test updates, no PR, 99 migration-touching tests pass pattern.
- HTTPXodus charter: PR remains draft until maintainer `accepted` label + CLA signed.
