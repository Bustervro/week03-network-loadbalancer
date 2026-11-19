# Week 4 – Error Handling Testing

## Objective
Improve the reliability of the Docker Network Load Balancer.

## Tasks
- Check how Nginx handles backend failures.
- Test whether the load balancer continues working when one backend stops.
- Document expected errors and recovery behavior.

## Test Plan
1. Start Docker containers.
2. Stop one backend container.
3. Send requests to the load balancer.
4. Record the responses.
5. Restart the backend and check recovery.

## Expected Result
The load balancer should handle backend failures without causing unnecessary downtime.

## Status
Test plan prepared. Execution and results still need to be recorded.
