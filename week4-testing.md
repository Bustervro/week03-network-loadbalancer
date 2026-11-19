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


<img width="1243" height="847" alt="image" src="https://github.com/user-attachments/assets/37f5a209-5dca-4130-908e-0f5f667d7b86" />
<img width="1243" height="794" alt="image" src="https://github.com/user-attachments/assets/03b98226-f900-495d-adfb-179db69632bb" />

<img width="1245" height="843" alt="image" src="https://github.com/user-attachments/assets/c99bfc09-3ff3-4272-a3b3-84292fbf00af" />
