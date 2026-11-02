# Week 03 — Docker Network Segmentation and Load Balancing

This is a **development demonstration** of two private Python backends behind an Nginx round-robin load balancer. A public Docker bridge reaches Nginx on port 8080; backend ports are *not* published on the host. The private Docker bridge is marked `internal: true`.

## Architecture diagram

```text
Browser / curl at localhost:8080
               |
  public_subnet 172.30.10.0/24
               |
       +---------------+
       | Nginx :80     |  <-- only published host port: 8080:80
       | Round-robin   |      connected to BOTH networks
       +---------------+
             /    \
  private_subnet 172.30.20.0/24 (internal: true)
           /          \
    backend1:3000    backend2:3000
     (private)        (private)
```

The `public_subnet` and `private_subnet` are Docker bridge networks, not a production cloud VPC. The subnet CIDRs are explicitly set; change them if they collide with your existing networks. This demo terminates plain HTTP on port 8080; production systems require HTTPS and additional hardening.

## Files

- `docker-compose.yml` — networks, Nginx, two isolated backends and health checks
- `nginx.conf` — round-robin upstream pool, retry/timeouts and logs
- `app.py`, `Dockerfile` — tiny Python JSON HTTP server, `/healthz` and a favicon 204 response
- `qa_test.py` / `test.sh` — repeatable automated checks; writes `qa-evidence.txt`, `qa-report.json`
- `qa-results.md` — *actual observed tests* and explicitly outstanding checks
- `ai-prompts.md` — AI disclosure and comparison with intentionally insecure example `audit/initial-compose.yml`
- `VIDEO_SCRIPT.md` — six-minute recording guide
- `../.github/workflows/qa.yml` — GitHub Actions CI to run Docker tests without Codespaces

## Run in Docker (locally or Codespaces)

From **this project's folder**:

```bash
docker compose up --build -d
docker compose ps
curl -i http://localhost:8080/healthz
bash test.sh
docker compose logs --tail=25 nginx
docker compose down
```

The script checks ten requests across both backends (5 + 5), stops `backend1` and verifies ten requests go to `backend2`, restarts the backend and verifies recovery, checks the host port boundary and health endpoint. It reports real failures instead of claiming success unconditionally. Logs and reports are generated in the working directory. It does **not** promise zero dropped requests for arbitrary timing or methods.

The Nginx upstream resolves Docker names at startup. If you **recreate** backend containers and change their internal IPs, run `docker compose restart nginx`. Restarting a stopped *existing* backend should keep its IP.

## Run checks without Codespaces (GitHub Actions)

Go to the repository **Actions → Docker QA → Run workflow**. The workflow runs `docker compose up --build -d`, executes `qa_test.py`, and saves a `qa-evidence` artifact. When it completes, inspect the workflow logs; a green check appears only if the automated checks pass. **Do not write “passed in GitHub Actions” until you see a green run.**

## AI use and security audit

I used ChatGPT to generate a starter project and explain deployment/testing. Exact short requests and the teacher-provided sample architecture prompt are recorded in [`ai-prompts.md`](ai-prompts.md). The `audit/initial-compose.yml` file is a **deliberately insecure comparison example**; I did not independently discover it as an accidental original error.

| Review item | Insecure audit example | Corrected project |
|---|---|---|
| Backend host ports | 3001:3000 and 3002:3000 published | No backend `ports` mappings |
| Backend networks | Public and private | Private only |
| Private bridge internal | Not configured | `internal: true` |
| Load balancing | Not validated | Nginx default round robin, retry on eligible failures |

## QA result summary (observed earlier in Codespaces)

| Test | Result | Evidence |
|---|---|---|
| 10 requests across two backends | **PASS — 5 backend1, 5 backend2**, all HTTP 200 | Terminal screenshots from Nov 1 Pacific |
| Stop backend1 | **PASS — observed requests from backend2**, HTTP 200 | Terminal screenshot |
| Restart backend1 | **PASS — both appeared again**, 10 responses HTTP 200 | Terminal screenshot |
| Host direct request `localhost:3000` | **PASS — connection refused** | Terminal screenshot; use `docker compose ps` to confirm mappings |
| `/healthz` via Nginx | **PASS — HTTP 200** | Terminal screenshot |
| Browser Network tab and Console | **PARTIAL — browser app responds, DevTools console not fully verified** | Needs manual browser check |

See [`qa-results.md`](qa-results.md) for details. Browser's earlier `/favicon.ico` 404 was a cosmetic missing-icon request; the **revised** backend now responds with 204, which still requires re-testing after deployment.

## Browser check (manual)

Open forwarded port 8080 in the browser (or `http://localhost:8080` locally). On the **JSON page** (not the Codespaces editor), open DevTools (F12) → Network → All → refresh. Check the main `/` request is HTTP 200, then check Console for unexpected errors. Update the status above and in `qa-results.md` with what you actually observe.

## Submission links

- **GitHub:** https://github.com/Bustervro/week03-network-loadbalancer
- **Live demo URL:** N/A — Docker/Codespaces development topology (not a persistent public deployment)
- **Video:** **ADD THE REAL UNLISTED/PUBLIC VIDEO URL AFTER RECORDING**

## Video timestamps (planned; adjust after recording)

- 0:00 — Diagram, public vs private networks, AI draft/config audit
- 1:30 — Running containers and ten-request balancing test
- 3:00 — Failover, restart and isolation checks
- 5:00 — Browser health check and takeaways

A video with both **webcam/face and screen** is required. The optional GitHub Actions test run does **not** replace the video.
