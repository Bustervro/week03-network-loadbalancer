
# Week 3 – Load Balancer Testing

## Project
Docker Network Load Balancer

## Goal
This week, I tested my Nginx load balancer to see if it works correctly with two Python backend servers. I used GitHub Actions to run the tests without installing Docker on my computer.

## Test 1: Health Check
I tested whether the application was running correctly.

Command:
```bash
curl -i http://localhost:8080/healthz
```

Expected Result: HTTP 200 OK.

Actual Result: HTTP 200 OK.

Status: PASSED

## Test 2: Load Balancing
I sent 10 requests to the Nginx load balancer.

Expected Result: Both Python backend servers receive requests.

Actual Result:
- Backend 1 received 5 requests.
- Backend 2 received 5 requests.

Status: PASSED

## Test 3: Network Security
I checked whether the Python backend servers were directly exposed to the host.

Expected Result: Only Nginx publishes the application's host port.

Actual Result:
- Nginx publishes port 8080.
- Backend 1 has no published host port.
- Backend 2 has no published host port.
- Both backend servers were healthy.

Status: PASSED

## Test Results
- Health Check: PASSED
- Load Balancing: PASSED
- Network Security: PASSED

All three tests passed using GitHub Actions.

## Key Learnings
I learned how to test server health, load balancing, and network security. I also learned how to use GitHub Actions to run Docker tests automatically.

## Progress Summary
This week, I created a testing plan and tested my Nginx load balancer. All three tests passed. I confirmed that both Python backend servers received requests and that only Nginx published a host port.

## Next Steps
My next step is to save screenshots of my test results, update my pull request, and submit my Week 3 development update.

## Testing Evidence
The GitHub Actions workflow completed successfully. Screenshots of the health check, load balancing results, and container port configuration can be used as testing evidence.
