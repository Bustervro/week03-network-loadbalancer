# Week 03 — QA Test Results

**Environment for observed results:** GitHub Codespaces, November 1, 2026 (Pacific Time), recorded in earlier terminal screenshots.

| Test | Observed result | Status |
|---|---|---|
| Initial 10 HTTP requests | backend1: 5, backend2: 5; all HTTP 200 | PASS |
| Stop backend1 and issue requests | Surviving backend2 responded HTTP 200 on observed requests | PASS (observed) |
| Restart backend1, issue 10 requests | Both backend IDs appeared; ten HTTP 200 responses | PASS |
| Host access `localhost:3000` | Connection refused | PASS (host port) |
| Load balancer `/healthz` | HTTP 200 from Nginx to backend | PASS |
| Browser opened forwarded 8080 | JSON `status:ok` response from backend2 | PASS (page loads) |
| Browser DevTools Network / Console | Main browser Console not independently verified; earlier missing `/favicon.ico` 404 logged | PARTIAL |
| Revised favicon response (`204`) | Code added but revised app not yet redeployed and verified | NOT RETESTED |
| GitHub Actions CI run | Included workflow; no result yet | NOT RUN |

## Limitations

- These were **observed demonstrations**, not proof of zero dropped requests for every kind of crash or timing.
- `localhost:3000` refusal demonstrates that host port was not listening. `docker compose ps` and the Compose file support the claim that backends have no published ports.
- Browser checks were partial and should not be marked fully passed until DevTools is inspected on the JSON application page.

## Additional reproducible test instructions

Run `docker compose up --build -d && bash test.sh`. The generated `qa-evidence.txt` and `qa-report.json` will document *that run's* actual results. Do not replace the earlier observed results unless the new run succeeds. Include relevant screenshots in the required video.
