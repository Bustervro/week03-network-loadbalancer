#!/usr/bin/env bash
set -u

BASE_URL="http://localhost:8080"

echo "== Verify health endpoint =="
curl -i --max-time 5 "${BASE_URL}/healthz" || exit 1

echo
echo "== Round-robin: 10 requests =="
for i in $(seq 1 10); do
  printf '%02d: ' "$i"
  curl -fsS --max-time 5 "${BASE_URL}/" || exit 1
  echo
done

echo
echo "== Failover: stop backend1 =="
docker compose stop backend1 || exit 1
trap 'docker compose start backend1 >/dev/null 2>&1 || true' EXIT
for i in $(seq 1 10); do
  printf '%02d: ' "$i"
  curl -fsS --max-time 5 "${BASE_URL}/" || exit 1
  echo
done

echo
echo "== Isolation: backend port must not be published on host =="
if curl -fsS --max-time 2 "http://localhost:3000/" >/dev/null 2>&1; then
  echo "WARNING: Something is reachable on localhost:3000. Check whether a backend port was published (or another app is running there)."
else
  echo "PASS: No HTTP service reachable on localhost:3000"
fi

echo
echo "== Recovery: restart backend1 =="
docker compose start backend1 || exit 1
trap - EXIT
sleep 6
for i in $(seq 1 10); do
  printf '%02d: ' "$i"
  curl -fsS --max-time 5 "${BASE_URL}/" || exit 1
  echo
done

echo
echo "== Docker networks and published ports =="
docker compose ps
docker compose logs --tail 12 nginx

echo
echo "Copy observed responses into qa-results.md."
