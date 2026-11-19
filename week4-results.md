# Week 4 – Backend Failure Testing

## Objective
Test how the Nginx load balancer responds when one backend server stops working.

## Test Results

**Test 1: Start Docker containers**
- Result: PASS
- Both backend servers started successfully.

**Test 2: Health Check**
- Result: PASS
- Nginx returned HTTP 200 OK.

**Test 3: Backend Failure**
- Result: PASS
- Stopped Backend 1 using Docker Compose.
- Nginx continued returning HTTP 200 OK.
- Backend 2 successfully handled requests.

**Test 4: Backend Recovery**
- Result: Pending
- Restart Backend 1 and confirm it becomes healthy.

## Key Learnings
I learned how Nginx distributes requests between backend servers and how the load balancer can continue responding when one backend becomes unavailable.

## Conclusion
The failure test passed. Backend 2 continued serving health-check requests when Backend 1 was stopped. Recovery testing is still needed.
