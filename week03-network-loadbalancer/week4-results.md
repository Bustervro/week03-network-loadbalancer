# Week 4 – Backend Failure and Recovery Testing

## Objective
Test the reliability of the Nginx Docker Network Load Balancer.

## Test Results

### Test 1: Start Docker Containers
Result: PASS
- Nginx started successfully.
- Backend 1 was healthy.
- Backend 2 was healthy.

### Test 2: Health Check
Result: PASS
- HTTP response: 200 OK.

### Test 3: Backend Failure
Result: PASS
- Stopped Backend 1.
- Backend 2 continued handling requests.
- Nginx returned HTTP 200 OK.

### Test 4: Backend Recovery
Result: PASS
- Restarted Backend 1.
- Both backends became healthy.
- Nginx returned HTTP 200 OK.

## Key Learnings
I learned how Nginx handles backend failures and how Docker Compose can restart services.

## Conclusion
The load balancer continued responding when one backend stopped, and both backends were healthy after recovery.
