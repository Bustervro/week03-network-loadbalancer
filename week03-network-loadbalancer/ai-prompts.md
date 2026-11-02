# AI Use and Configuration Audit

## AI tool
ChatGPT generated this project starter from the assignment requirements supplied in chat.

## Exact user requests in this conversation
- "what i put on github for this assignment"
- "what codes i put on github"

The complete assignment requirements (including the sample architect prompt) were also pasted into the conversation before these requests. Preserve a copy of that full text if your instructor requires a verbatim prompt log for the entire context.

## AI-generated draft and audit
The `audit/initial-compose.yml` file is a **deliberately insecure example draft created for this exercise**, not the Docker Compose file to execute.

Problems to point out when comparing the draft with `docker-compose.yml`:
1. It maps backend host ports `3001:3000` and `3002:3000`, letting users bypass Nginx.
2. It connects both backends to `public_subnet`, breaking the public/private boundary.
3. It does not mark the private network as `internal: true`.

Corrected configuration:
- Only Nginx publishes a host port (`8080:80`).
- Backends connect **only** to `private_subnet` and use `expose`, not `ports`.
- The private Docker bridge is marked `internal: true`.
- Nginx uses service names instead of fixed container IPs, and has timeouts and retry settings.

## My personal verification (complete after running Docker)
- Date tested:
- One specific issue I reviewed and how I confirmed the correction:
- Tests I personally ran and observed:
- Any remaining concerns:

**Important:** Describe the sample draft as a deliberately insecure AI example; do not present it as a mistake that you independently discovered in a prior run. Be accurate about which changes and tests you personally performed.
