# AI Use and Configuration Audit

## 1. AI Tool Used

I used ChatGPT to help me create my Week 03 Docker Network Segmentation and Load Balancing project.

ChatGPT helped me generate Docker configuration files, Nginx load balancing settings, backend application code, and testing instructions.

I used GitHub to store my project and GitHub Codespaces to run and test it.

## 2. Exact ChatGPT Requests

These are the original requests I submitted to ChatGPT:

1. "what i put on github for this assignment"
2. "what codes i put on github"

I also pasted the full assignment instructions into ChatGPT, including the instructor's sample architecture prompt.

## 3. Original Assignment Sample Prompt

**Source:** This prompt was included in the original assignment instructions I provided to ChatGPT. It was not submitted separately as a standalone request.

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

## 4. AI-Generated Draft and Configuration Audit

ChatGPT helped generate an initial project and an intentionally insecure example configuration saved in `audit/initial-compose.yml`.

I used this insecure example to understand and compare network configuration problems with the corrected `docker-compose.yml` file.

### Security Problems in the Example

**Problem 1: Backend Ports Exposed**

The insecure example exposed backend ports 3001 and 3002 directly to the host.

This could let users access backend servers without going through Nginx.

**Problem 2: Incorrect Network Connections**

Both backend servers were connected to the public network.

Backend servers should connect only to the private network.

**Problem 3: Missing Private Network Protection**

The insecure example did not mark the private network as internal.

### Corrected Configuration

The working project includes these security improvements:

1. Only Nginx publishes a host port (`8080:80`).
2. Backend 1 and Backend 2 connect only to `private_subnet`.
3. The private Docker network uses `internal: true`.
4. Nginx connects to both public and private networks.
5. Nginx uses Docker service names instead of fixed backend IP addresses.
6. Nginx distributes traffic using round-robin load balancing and includes timeout and retry settings.

The insecure configuration was deliberately provided as an audit example. It was not an accidental issue I independently discovered while running an earlier version.

## 5. My Personal Verification

**Date tested:** November 1, 2026 (Pacific Time)

**Testing environment:** GitHub Codespaces using Docker Compose.

I ran the application and checked whether the load balancer and private backend servers worked correctly.

### Test 1: Load Balancing — PASSED

I sent 10 HTTP requests through Nginx.

**Results:**

- Backend 1 received 5 requests.
- Backend 2 received 5 requests.
- All 10 requests returned HTTP 200.
- Round-robin load balancing worked correctly.

### Test 2: Failover — PASSED

I stopped Backend 1 using Docker Compose.

**Results:**

- Backend 2 continued responding to requests.
- The failover test returned HTTP 200 responses.
- The application continued working during the observed test.

### Test 3: Backend Recovery — PASSED

I restarted Backend 1 and tested again.

**Results:**

- Backend 1 returned to service.
- Both backend servers handled requests again.
- All 10 requests returned HTTP 200.

### Test 4: Network Isolation — PASSED

I attempted to connect directly to `localhost:3000`.

**Results:**

- The connection was refused.
- The backend was not published on that host port.
- The project was configured so external requests go through Nginx.

### Test 5: Health Check — PASSED

I tested `http://localhost:8080/healthz`.

**Results:**

- The endpoint returned HTTP 200 OK.
- Nginx successfully forwarded the request.
- The backend returned a healthy response.

### Test 6: Browser Console and Network Tab — NOT YET VERIFIED

I still need to inspect the browser Developer Tools Network and Console tabs to confirm there are no unexpected browser or gateway errors.

## 6. What I Learned

I learned that a load balancer helps distribute traffic between different servers.

I also learned that when one backend server stops working, another server can continue responding to requests.

Keeping backend servers on a private network helps protect them from direct external access.

Using Docker and GitHub Codespaces helped me understand how applications and networks work together.

## 7. Remaining Limitations

This project demonstrates local Docker networking and basic load balancing.

It does not include production HTTPS, cloud security groups, or a fully production-ready high-availability setup.

The observed tests show that the application worked under the conditions I tested, but they do not guarantee that every request will succeed during all possible failures.

## 8. Conclusion

ChatGPT helped me generate the project files and an example configuration audit.

I reviewed the network setup and used GitHub Codespaces to run the project.

My testing demonstrated successful round-robin load balancing, backend failover, recovery, health checks, and basic network isolation.

This assignment helped me understand why applications need load balancers and protected private networks.
