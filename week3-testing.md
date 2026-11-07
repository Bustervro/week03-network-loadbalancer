Week 3 – Load Balancer Testing

Project

Docker Network Load Balancer

Goal

This week, I will test my Nginx load balancer to see if it works correctly with two Python backend servers.

Test 1: Health Check

Run:
curl -i http://localhost:8080/healthz

Expected result: HTTP 200 if the service is healthy.

Test 2: Load Balancing

Send 10 requests to the load balancer.

Expected result: Both backend servers receive requests.

Test 3: Network Security

Check that the Python backend servers are not directly exposed to the host.

Expected result: Only Nginx publishes the application’s host port.

Test Results

Key Learnings

I am learning how to test server health, request distribution, and network security.

Next Steps

Run the tests, record the actual results, and improve the system if problems are found.

Health Check: PASSED — HTTP 200 OK.
Load Balancing: PASSED — Backend 1 received 5 requests and Backend 2 received 5 requests.
Network Security: Pending verification.
