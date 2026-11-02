# Week 03 – AI Use, Prompt Log, and Configuration Audit

## 1. AI Tool Used

**AI Tool:** ChatGPT (OpenAI)

**Project:** Docker Network Segmentation and Load Balancing

I used ChatGPT to help me create my Docker networking and load balancer project. ChatGPT helped generate the Docker Compose configuration, Nginx settings, Python backend application, README documentation, and testing instructions.

I used GitHub to store my code and GitHub Codespaces to run and test the project.

## 2. My Actual ChatGPT Requests

These are the exact short requests I submitted to ChatGPT when creating my project:

**Prompt 1:**
> what i put on github for this assignment

**Prompt 2:**
> what codes i put on github

Before these requests, I pasted the complete Week 03 assignment instructions into ChatGPT, including the instructor's sample network architecture prompt.

I also asked ChatGPT for help uploading the files, running the tests, and documenting the results.

## 3. Original Assignment Sample Prompt

**Source:** This prompt was included in the assignment instructions that I pasted into ChatGPT. It was not sent separately as a standalone prompt.

Act as a senior network systems architect. I need a multi-container network topology configured using Docker Compose (or Terraform/Cloud IaC) demonstrating isolated subnets and reverse-proxy load balancing for a web application.

The architecture must include:

**1. Two Isolated Network Subnets:**

- `public_subnet`: Accessible from the host/internet.
- `private_subnet`: Isolated backend network with no direct external port exposure.

**2. A Load Balancer (Nginx or HAProxy):**

- Dual-homed on both `public_subnet` and `private_subnet`.
- Exposes port 80/443 to the host.
- Configured with an upstream pool distributing requests across backend instances using Round-Robin.

**3. At least Two Web Application Backend Replicas (e.g., Node.js, Python, or Go):**

- Connected ONLY to `private_subnet`.
- Each instance must return a unique identifier (e.g., container hostname or server ID) so I can verify which instance handled the request.
- Includes a simple health-check endpoint (`/healthz`).

Provide the Docker Compose file, the load balancer configuration file (e.g., `nginx.conf`), the minimal backend application code, and step-by-step instructions to run and test it.

## 4. AI-Generated Project

ChatGPT helped generate the following project files:

- `docker-compose.yml` – Creates two networks, two backend servers, and Nginx.
- `nginx.conf` – Configures round-robin load balancing.
- `app.py` – Creates the Python backend application.
- `Dockerfile` – Builds the backend containers.
- `README.md` – Explains the project and how to run it.
- `qa-results.md` – Documents my testing results.
- `test.sh` – Provides testing commands.
- `audit/initial-compose.yml` – Provides an intentionally insecure example for comparing network configurations.

## 5. AI Configuration Audit

I reviewed the intentionally insecure example in `audit/initial-compose.yml` and compared it with the corrected `docker-compose.yml`.

The insecure example was generated as a learning exercise. It was not an accidental AI error I discovered in an earlier working deployment.

### Problem 1: Exposed Backend Ports

The insecure example used host ports `3001:3000` and `3002:3000`.

**Why this is a problem:**

Users could connect directly to the backend servers without passing through the load balancer.

**Corrected configuration:**

Only Nginx publishes a host port (`8080:80`). Backend servers use internal container ports.

### Problem 2: Incorrect Network Connections

The insecure example connected both backend servers to the public network.

**Why this is a problem:**

Backend application servers should not be directly connected to the public network.

**Corrected configuration:**

Backend 1 and Backend 2 connect only to `private_subnet`. Nginx connects to both public and private networks.

### Problem 3: Missing Private Network Isolation

The insecure example did not mark the private network as internal.

**Corrected configuration:**

The corrected Docker Compose configuration uses `internal: true` for the private network.

### Problem 4: Load Balancer Verification

I reviewed the Nginx configuration to understand how requests are distributed between backend servers.

The working project uses service names instead of hardcoded backend IP addresses and includes timeout and retry settings.

The load balancer uses round-robin distribution, which sends requests between available backend servers.

## 6. My Personal Verification and Testing

**Date Tested:** November 1, 2026

**Testing Environment:** GitHub Codespaces with Docker Compose

I ran the project through GitHub Codespaces and used the terminal to check the application's functionality.

### Test 1: Load Balancing – PASSED

I used this command:

`for i in {1..10}; do curl -sS -w ' HTTP %{http_code}\n' http://localhost:8080/; done`

**Results:**

- Backend 1 received 5 requests.
- Backend 2 received 5 requests.
- All 10 requests returned HTTP 200.
- Round-robin load balancing worked correctly.

### Test 2: Failover – PASSED

I stopped Backend 1 using:

`docker compose stop backend1`

Then I sent requests through Nginx.

**Results:**

- Backend 2 continued responding.
- The observed requests returned HTTP 200.
- The remaining backend handled the tested traffic.

### Test 3: Backend Recovery – PASSED

I restarted Backend 1 using:

`docker compose start backend1`

Then I repeated the request test.

**Results:**

- Backend 1 returned to service.
- Both backend servers received requests.
- All 10 requests returned HTTP 200.

### Test 4: Network Isolation – PAS
