# Week 03: Docker Network Segmentation and Load Balancing

A learning project that uses an Nginx reverse proxy to distribute HTTP requests between two Python web servers. **Only Nginx publishes a host port; the backends run on an internal Docker network.**

## Network diagram

```text
      Browser / curl
       localhost:8080
             |
  public_subnet (172.30.10.0/24)
             |
    +-----------------+
    |  Nginx          |  <-- attached to BOTH networks
    |  port 80        |
    |  round-robin LB |
    +-----------------+
         /       \
  private_subnet (172.30.20.0/24, internal)
       /             \
  backend1:3000   backend2:3000
  (private only)  (private only)
```

These are Docker bridge networks for a **local demo**; they do not automatically implement cloud VPC subnet security groups or internet-ready TLS. The sample CIDR ranges may need changing if they conflict with your local network.

## Files

- `docker-compose.yml`: public and private networks, Nginx, two Python backends.
- `nginx.conf`: round-robin upstream, timeouts, failover retries, logs.
- `app.py`: simple JSON response with unique backend ID and `/healthz`.
- `Dockerfile`: Python container build.
- `audit/initial-compose.yml`: intentionally insecure AI example for the configuration audit; **do not run it**.
- `ai-prompts.md`: actual AI requests, example audit, and your verification notes.
- `qa-results.md`: QA results table to complete using real output.
- `test.sh`: commands to exercise balancing, failover, and host isolation.

## Requirements

Install Docker Desktop (or Docker Engine with Docker Compose) and curl. GitHub alone will store the code but will not run this local Docker project.

## Start and inspect

```bash
docker compose up --build -d
docker compose ps
curl -i http://localhost:8080/healthz
```

Visit http://localhost:8080 and refresh. The response's `server` field tells you whether backend1 or backend2 served the request.

## Load distribution

```bash
for i in $(seq 1 10); do curl -s http://localhost:8080/; echo; done
```

Expect roughly five responses from each backend if both are healthy. Nginx's default upstream policy is round-robin.

## Failover and recovery

```bash
docker compose stop backend1
for i in $(seq 1 10); do curl -i http://localhost:8080/; done
docker compose start backend1
sleep 6
for i in $(seq 1 10); do curl -s http://localhost:8080/; echo; done
```

Look for only backend2 during the stopped phase, followed by both servers after recovery. Nginx retries eligible requests, reducing outages, but results depend on failure timing and request type; record real responses instead of claiming guaranteed zero dropped requests.

## Network isolation (negative test)

```bash
curl --max-time 2 http://localhost:3000/
docker compose ps
docker compose logs --tail=30 nginx
```

The direct `localhost:3000` request should fail because neither backend publishes a host port. Note that a different program on your host might be listening on that port; use `docker compose ps` to verify Docker-published ports. From the host, only Nginx is published at port 8080.

## Run the walkthrough test

```bash
bash test.sh
```

Fill in `qa-results.md` with the actual results, and inspect your browser DevTools Network/Console tabs.

## Cleanup

```bash
docker compose down
```

If you recreate backend containers and their IPs change, restart Nginx (`docker compose restart nginx`) so its service-name upstreams are resolved again. Stopping and starting the same existing backend container should retain its IP.

## AI disclosure, exact prompt appendix, and audit

**AI tool:** ChatGPT. The actual short user requests that led to this code were:

> what i put on github for this assignment
>
> what codes i put on github

The full assignment text was also provided earlier in the chat, including its sample initial architect prompt. For an exact record of *all* prompt context, include that full pasted assignment or record your future prompts verbatim in `ai-prompts.md`.

**AI audit example:** `audit/initial-compose.yml` is an **intentionally insecure AI-created draft for comparison**, not a file to run. It publishes host ports 3001/3002 for the backends and connects them to the public network. In the corrected `docker-compose.yml`, both backends are private-only, no backend ports are published, and `private_subnet` has `internal: true`. Nginx is the only public entry point. Confirm these details yourself and explain what you personally checked in the video.

## QA Summary (Test Results)

| Check | Expected | Actual Result |
|---|---|---|
| 10 round-robin HTTP requests | About 5 responses per backend | PASSED - Backend 1: 5, Backend 2: 5 |
| One backend stopped | Successful requests handled by surviving backend | PASSED - Backend 2 returned HTTP 200 |
| Backend restarted | Both servers appear again | PASSED - Both servers responded |
| Host request to backend port | Direct backend access blocked | PASSED - Connection refused |
| /healthz through Nginx | HTTP 200 | PASSED - HTTP 200 OK |
| Browser Network/Console | No unexpected errors | NOT TESTED YET |

See `qa-results.md` for a more complete table and notes. Do not claim Docker tests were passed until you run them yourself.

## Video walkthrough (5–7 minutes)

1. 0:00–1:30 — diagram and insecure draft versus corrected Compose.
2. 1:30–3:00 — run and send 10 requests.
3. 3:00–5:00 — stop backend1, test traffic, test isolation, restart it, show logs.
4. 5:00–6:30 — explain Nginx, subnet segmentation, and lessons learned.

## Submission links

- GitHub repository: [add link]
- Video recording: [add link]
- Live demo URL: N/A — Local Docker Topology
