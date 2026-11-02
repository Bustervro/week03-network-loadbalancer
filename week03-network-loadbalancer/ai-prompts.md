# AI Use and Configuration Audit — Week 03

## Tool and actual prompts

**AI tool used:** ChatGPT (OpenAI). The full teacher assignment instructions were pasted into the chat before the short requests. The short, verbatim requests that directly led to the initial code files were:

1. `what i put on github for this assignment`
2. `what codes i put on github`

I subsequently asked ChatGPT for assistance uploading files, using Codespaces, testing, writing and updating the README and prompt log. I used GitHub Copilot in Codespaces for QA documentation; its changes were committed locally but a GitHub authentication failure prevented pushing that commit from Codespaces.

### Teacher-provided architecture prompt (included within the assignment; not a separate request)

> Act as a senior network systems architect. I need a multi-container network topology configured using Docker Compose (or Terraform/Cloud IaC) demonstrating isolated subnets and reverse-proxy load balancing for a web application.
>
> The architecture must include:
> 1. Two Isolated Network Subnets:
>    - `public_subnet`: Accessible from the host/internet.
>    - `private_subnet`: Isolated backend network with no direct external port exposure.
> 2. A Load Balancer (Nginx or HAProxy):
>    - Dual-homed on both `public_subnet` and `private_subnet`.
>    - Exposes port 80/443 to the host.
>    - Configured with an upstream pool distributing requests across backend instances using Round-Robin.
> 3. At least Two Web Application Backend Replicas (e.g., Node.js, Python, or Go):
>    - Connected ONLY to `private_subnet`.
>    - Each instance must return a unique identifier (e.g., container hostname or server ID) so I can verify which instance handled the request.
>    - Includes a simple health-check endpoint (`/healthz`).
>
> Provide the Docker Compose file, the load balancer configuration file (e.g., `nginx.conf`), the minimal backend application code, and step-by-step instructions to run and test it.

**Completeness note:** The entire longer teacher assignment message was also pasted into ChatGPT, but the text above is the teacher's embedded sample prompt, not that complete message. Copy the full first assignment message from the chat into an appendix if the instructor requires a verbatim log of *all* messages.

## Generated starter project and review

ChatGPT helped generate `docker-compose.yml`, `nginx.conf`, `app.py`, `Dockerfile`, docs, and a deliberately insecure comparison file `audit/initial-compose.yml`. The comparison file was intentionally designed for auditing **after** the starter was created; it was not a surprise mistake independently found in an older live deployment.

| Finding in the intentionally insecure comparison | Why wrong | Correction in running project |
|---|---|---|
| `3001:3000` and `3002:3000` host ports published | Direct backend access bypasses Nginx | No backend `ports` entries |
| Backends connected to `public_subnet` | Breaks intended two-tier boundary | Backend services on `private_subnet` only |
| Private subnet lacks `internal: true` | Weaker Docker network isolation | Marked internal |
| Bare backend addresses would be fragile if hard-coded | IP may change | Nginx uses service names, plus timeouts/retry rules |

The working topology exposes only Nginx host port 8080, and Nginx is connected to both networks.

## Actual tests performed and observed Nov 1 Pacific

- 10 requests: 5 served by `backend1`, 5 by `backend2`, each HTTP 200.
- Stopped `backend1`: observed requests returned HTTP 200 from `backend2`.
- Restarted `backend1`: both server IDs appeared again, with 10 HTTP 200 responses.
- Host `localhost:3000` returned connection refused.
- `/healthz` through Nginx returned HTTP 200.
- Browser app returned valid JSON; DevTools Console check remains incomplete. A favicon 404 appeared in logs.

## New revision and remaining testing

The revised code handles `/favicon.ico` with 204 rather than 404 and adds an optional GitHub Actions QA workflow so Docker tests can be repeated **without Codespaces**. Those modifications have not been demonstrated in the user's Codespace yet and must be tested before calling them passed.

**Limitations:** Docker bridge subnets are not cloud VPC subnets; this demo does not implement TLS, production HA, guaranteed zero-loss failover, or an always-on public URL. The real 5–7 minute webcam + screen recording is still required.
