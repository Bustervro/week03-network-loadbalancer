# Week 03 - QA Test Results

## Test 1: Load Balancing - PASSED
I sent 10 requests to the load balancer.
- Backend 1 received 5 requests.
- Backend 2 received 5 requests.
- All requests returned HTTP 200.
- Round-robin balancing worked correctly.

## Test 2: Failover - PASSED
I stopped Backend 1.
- Backend 2 continued responding.
- The requests I tested returned HTTP 200.
- I restarted Backend 1 successfully.

## Test 3: Backend Recovery - PASSED
After restarting Backend 1, I tested again.
- Both backends responded.
- All 10 requests returned HTTP 200.

## Test 4: Network Isolation - PASSED
I attempted to connect directly to localhost:3000.
- The connection was refused.
- The backend was not exposed on that host port.

## Test 5: Health Check - PASSED
I tested http://localhost:8080/healthz.
- The response was HTTP 200 OK.
- Nginx successfully routed the request.

## Conclusion
The observed tests showed successful load balancing,
backend failover, recovery, and basic network isolation.
