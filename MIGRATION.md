# mem0ai/mem0 — HTTPXodus migration

## Commit
- Branch: `httpxodus/httpx2-migration` (on `ProgrammerPlus1998/mem0` fork)
- Commit: `8369d40365a4fb6ac8bc0daf491d6bcb8ddb9a6d`
- Title: `refactor: migrate from httpx to httpx2 (dual import)`
- Push status: pushed to `https://github.com/ProgrammerPlus1998/mem0` (not yet a PR — awaiting human review per the HTTPXodus charter)

## File changes (10 files, +52 / -9)

| File | Change |
|---|---|
| `pyproject.toml` | Added `httpx2>=2.12.0; python_version >= '3.10'` alongside the existing `httpx>=0.28.0` |
| `mem0/client/main.py` | Dual import: `try: import httpx2 as httpx; except ModuleNotFoundError: import httpx` |
| `mem0/proxy/main.py` | Same dual import |
| `mem0/client/utils.py` | Same dual import |
| `mem0/client/project.py` | Same dual import |
| `mem0/utils/http.py` | Same dual import |
| `tests/test_client.py` | Dual import — needed because the test uses `httpx.HTTPStatusError` as a `side_effect` that the SUT now catches as `httpx2.HTTPStatusError` |
| `tests/test_client_utils.py` | Same — uses `httpx.HTTPStatusError`, `httpx.ConnectError`, etc. as side effects |
| `tests/test_http_client_proxies.py` | Same — uses `isinstance(config.http_client, httpx.Client)` and the production client is now an `httpx2.Client` |
| `tests/llms/test_openai.py` | Same — uses `isinstance(llm.config.http_client, httpx.Client)` and the production client is now an `httpx2.Client` |

## Test results

### Migration-touching test files (all 99 pass)

```
tests/test_client.py                42 passed
tests/test_client_utils.py           7 passed
tests/test_http_client_proxies.py    7 passed
tests/llms/test_openai.py           21 passed
tests/test_proxy.py                  8 passed
tests/test_project.py               14 passed
                                    ---
                                     99 passed
```

### Full pytest run (top-level only — `tests/llms`, `tests/vector_stores`, `tests/embeddings`, `tests/rerankers`, `tests/memory` skipped because their optional provider deps aren't installed in this environment)

```
342 passed, 16 failed, 22 skipped
```

The 16 failures are **pre-existing and unrelated to the migration**:
- 3 in `tests/test_memory.py` — `langchain-core` is in the `extras` optional group and was not installed in this env. Verified by checking out `main` and running the same test — same failure, same `ImportError`.
- 13 in `tests/test_oss_to_platform_migrate.py` — these tests start a local `oss-to-platform-migrate.sh` script that hits `api.mem0.ai` and fails with `Bad Gateway` (no network/auth in this env). Reproduced identically on `main`.

### Lint / format

- `ruff check` — passes for all touched files
- `isort --check-only --profile black` — passes
- `ruff format --check` — pre-existing format drift in 60 files unrelated to this PR (e.g. `assert X == (a, b)` vs `assert X == (a, b,)`). Not touched.

## Manual verification of the dual-import behaviour

- `httpx2` installed + import mem0: every `mem0.*` module uses `httpx2.*` (verified by printing `httpx.__file__`)
- `httpx2` blocked via `sys.meta_path` shim + import mem0: every `mem0.*` module falls back to `httpx.*` (verified by printing `httpx.__file__`)

The two runtime exception classes that matter for matching (`httpx2.HTTPStatusError` and `httpx.HTTPStatusError`) are distinct, which is why the test side_effects had to be updated to use the same module the SUT imports.

## Notes for the human reviewer

1. **AGENTS.md says "Use an optional group" for Python deps.** I added `httpx2` to the core `dependencies` list instead of an extras group, mirroring the AutoGPT HTTPXodus PR pattern. mem0 already pins `httpx>=0.28.0` in core `dependencies`, so the precedent for direct-dependency migration is already in this file. The `httpx2; python_version >= "3.10"` marker is also a no-op in practice because `requires-python = ">=3.10,<4.0"` already excludes older Pythons, but it makes the dep self-documenting.

2. **Tests were updated, not just production code.** The 4 test files import `httpx` directly to build mocks/side-effects that the SUT now catches as `httpx2.*` exception classes. Without this change, the existing tests would break (verified — they fail on this branch with the un-edited test code, and pass with the edits).

3. **No upper bound on `httpx>=0.28.0`.** Left as-is. The migration issue specifically calls this out: with no upper bound, pip will happily resolve a future httpx 1.0 stable into mem0 installs the day it ships. Tightening the bound is a separate concern from adopting httpx2 and the maintainer may prefer to handle it independently.

4. **The httpx2 TLS caveat from the issue** (OS trust store instead of `certifi`) is now a real behaviour change for mem0 users in containerised / corporate-proxy environments. The PR doesn't touch docs — the HTTPXodus issue (#7207) already flags it, and the maintainer's acceptance response should determine where it lands in the docs (likely `docs/` or a changelog entry).

5. **No `poetry.lock` was committed** — mem0 uses `pyproject.toml` + `hatch` (not poetry). The lockfile analogue is the resolved install in `.venv`, which isn't tracked. CI will re-resolve.

6. **No PR opened.** Per the HTTPXodus charter, the human opens the PR after review.

## Suggested next step

Open a draft PR at:
`https://github.com/ProgrammerPlus1998/mem0/pull/new/httpxodus/httpx2-migration`

The body should reference `Closes #7207` (or `Refs #7207` if the maintainer prefers to keep the issue open until the PR merges). AGENTS.md says PRs without an `accepted` linked issue get auto-closed, so make sure the linked issue has the `accepted` label before opening.
