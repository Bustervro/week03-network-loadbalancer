# QA Test Results — Fill in with YOUR observed output

Run the included `bash test.sh` after `docker compose up --build -d`.

| Test | Expected result | Actual result | Pass/Fail |
|---|---|---|---|
| Round-robin (10 requests) | Roughly 5 requests per backend | [fill in] | [fill in] |
| Failover after stopping backend1 | 10 successful responses from backend2 | [fill in] | [fill in] |
| Backend1 restored | Both backend IDs appear again | [fill in] | [fill in] |
| Backend host isolation | Host `localhost:3000` cannot reach a backend | [fill in] | [fill in] |
| Health endpoint | HTTP 200 at `localhost:8080/healthz` | [fill in] | [fill in] |
| Browser DevTools | Successful requests; no unexpected errors | [fill in] | [fill in] |

Important caveat: Nginx retries *eligible* failed requests to another backend, but no system can promise zero dropped requests for all failure timings and HTTP request types. Document any errors you actually see.
