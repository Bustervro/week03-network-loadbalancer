# Week 03 video walkthrough — 6 to 6.5 minutes

**You must record your own face and screen.** Suggested tool: Zoom, OBS, or Loom. This is a speaking guide, **not a completed video**. Show live results; if a test fails, explain what happened instead of pretending it passed.

## 0:00–1:30 — Diagram and security audit

Show `README.md` and the ASCII diagram.

"My project uses Docker and Nginx to route web requests to two Python servers. Users connect to Nginx on port 8080. Nginx can reach both private backend servers. Neither backend publishes its port directly to the host. I used ChatGPT to build the starter project and reviewed an intentionally insecure example. That example exposed ports 3001 and 3002 and connected the backends to the public network. The corrected project has only Nginx published and a private bridge marked internal. This comparison example was intentionally created for the audit."

## 1:30–3:00 — Start servers and balance traffic

Show terminal or GitHub Actions test logs. In a Docker terminal, run:

```bash
docker compose up --build -d
docker compose ps
for i in {1..10}; do curl -sS -w ' HTTP %{http_code}\n' http://localhost:8080/; done
```

"I have three containers: Nginx, Backend 1, and Backend 2. Each backend returns its name so I can see which server handled the request. Across ten requests, we expect five from each backend using round-robin. Here is my actual output."

## 3:00–5:00 — Failover, recovery, isolation and logs

```bash
docker compose stop backend1
for i in {1..10}; do curl -sS -w ' HTTP %{http_code}\n' http://localhost:8080/; done
docker compose start backend1
sleep 8
for i in {1..10}; do curl -sS -w ' HTTP %{http_code}\n' http://localhost:8080/; done
curl -v --max-time 3 http://localhost:3000/
docker compose ps
docker compose logs --tail=15 nginx
```

"When I stop Backend 1, Nginx should use Backend 2. I restart Backend 1 and show that the load balancer uses both again. Direct access to localhost port 3000 should fail, because the backend isn't published there. The container listing shows only port 8080 published by Nginx. Nginx logs record the routed requests."

## 5:00–6:30 — Browser and conclusion

```bash
curl -i http://localhost:8080/healthz
```

Open the forwarded port 8080 app JSON page. Use browser DevTools Network → All → refresh; then Console. If errors appear, describe them accurately.

"The health endpoint returns HTTP 200, showing the application responds. The main lesson is that Nginx can spread traffic and reduce the impact when one backend stops. Private networking also limits direct exposure. This is a learning project, not production high availability or HTTPS. ChatGPT gave me a starting point, but running and checking the code was essential."

## Submit

1. Record your own webcam and screen together for 5–7 minutes.
2. Upload video to YouTube as unlisted or public (or as allowed by instructor).
3. Paste real video link into README and the LMS submission.
4. Keep screenshots of actual tests. Do not claim new GitHub Actions tests passed until they have a green run.
