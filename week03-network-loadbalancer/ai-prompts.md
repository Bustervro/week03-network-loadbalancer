# AI Use and Configuration Audit

## AI Tool Used

I used ChatGPT to help create my Docker networking and load balancer project.

## Prompts I Used

My requests to ChatGPT included:

1. "what i put on github for this assignment"
2. "what codes i put on github"

I also provided the complete assignment instructions, including the sample network architecture prompt.

## AI-Generated Draft and Audit

The project includes an intentionally insecure example in `audit/initial-compose.yml` for comparison with the corrected Docker configuration.

### Problems in the Example

1. Backend ports 3001 and 3002 were exposed to the host.
2. Both backend servers were connected to the public network.
3. The private network was not marked as internal.

### Corrected Configuration

1. Only Nginx exposes a host port (8080).
2. Backend 1 and Backend 2 connect only to the private network.
3. The private network uses `internal: true`.
4. Nginx distributes traffic between the two backend servers.

## My Personal Verification

**Date tested:** November 1, 2026

### Configuration Reviewed

I compared the insecure example with the corrected Docker Compose configuration. I reviewed the exposed backend ports and network connections to understand why the corrected version is safer.

### Tests I Performed

- **Load Balancing:** I sent 10 requests. Backend 1 received 5 requests and Backend 2 received 5 requests.
- **Failover:** I stopped Backend 1. Backend 2 continued responding with HTTP 200.
- **Recovery:** I restarted Backend 1 and confirmed both backend servers responded again.
- **Network Isolation:** I tried connecting to localhost:3000 and received a connection refused error.
- **Health Check:** I tested `/healthz` and received HTTP 200 OK.

### What I Learned

I learned that a load balancer distributes requests between servers. If one server stops working, another server can continue handling requests.

I also learned why backend servers should stay on a private network instead of being exposed directly to users.

### Remaining Concerns

This project demonstrates Docker network isolation in a development environment. It does not include production HTTPS or cloud security controls.

## Conclusion

ChatGPT helped me create the project files and an example security audit. I ran the Docker project in GitHub Codespaces and tested load balancing, failover, recovery, and basic network isolation.
