#!/usr/bin/env python3
"""Repeatable QA tests. Requires running Docker Compose and Python 3.
Reports observations; cannot promise zero loss for all failure modes.
"""
import collections
import http.client
import json
import socket
import subprocess
import time
from pathlib import Path

URL_HOST = "127.0.0.1"
BASE_PORT = 8080
OUT = Path(__file__).resolve().parent
report = {"checks": {}, "notes": [], "timestamp_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()}
lines = []


def emit(s):
    print(s, flush=True)
    lines.append(s)


def command(*args, check=True):
    p = subprocess.run(args, capture_output=True, text=True, timeout=75)
    if check and p.returncode:
        raise RuntimeError(f"{' '.join(args)} failed ({p.returncode}): {p.stderr.strip()}")
    return p


def get(path="/"):
    conn = http.client.HTTPConnection(URL_HOST, BASE_PORT, timeout=5)
    try:
        conn.request("GET", path, headers={"Connection": "close"})
        r = conn.getresponse()
        body = r.read()
        return r.status, json.loads(body.decode()), dict(r.getheaders())
    finally:
        conn.close()


def wait_healthy(seconds=40):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            if get('/healthz')[0] == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise AssertionError("Nginx health check did not become ready")


def requests(n=10, expected=None):
    counts = collections.Counter()
    for i in range(n):
        status, body, headers = get()
        who = body.get("server", "unknown")
        emit(f"{i+1:02d}: HTTP {status}, server={who}, X-Load-Balancer={headers.get('X-Load-Balancer', '?')}")
        assert status == 200, f"non-200: {status}"
        assert who in {"backend1", "backend2"}, f"unknown backend: {who}"
        if expected:
            assert who == expected, f"expected {expected}, got {who}"
        counts[who] += 1
    return dict(counts)


def verify_config():
    config = json.loads(command("docker", "compose", "config", "--format", "json").stdout)
    services = config["services"]
    assert set(services) >= {"nginx", "backend1", "backend2"}
    for name in ("backend1", "backend2"):
        assert not services[name].get("ports"), f"{name} publishes host ports"
        assert len(services[name].get("networks", {})) == 1
        assert next(iter(services[name]["networks"])).endswith("private_subnet")
    assert len(services["nginx"].get("networks", {})) == 2
    assert any(int(p.get("published", 0)) == 8080 for p in services["nginx"].get("ports", []))
    assert any(name.endswith("private_subnet") and net.get("internal") is True
               for name, net in config["networks"].items())
    report["checks"]["config"] = "PASS"
    emit("PASS: only Nginx publishes port 8080; backends private; private network internal")


def main():
    verify_config()
    wait_healthy()
    status, body, _ = get('/healthz')
    assert status == 200 and body.get('status') == 'ok'
    report['checks']['health'] = 'PASS'
    emit('PASS: /healthz HTTP 200')

    emit('--- 10 round-robin requests ---')
    counts = requests()
    assert counts.get('backend1') == 5 and counts.get('backend2') == 5, f"not evenly balanced: {counts}"
    report['checks']['balance'] = counts
    emit(f'PASS: distributed {counts}')

    emit('--- stop backend1; validate failover ---')
    command('docker', 'compose', 'stop', 'backend1')
    try:
        counts = requests(expected='backend2')
        report['checks']['failover'] = counts
        emit('PASS: ten observed requests served by backend2, all HTTP 200')
    finally:
        emit('--- restart backend1 ---')
        command('docker', 'compose', 'start', 'backend1')
    time.sleep(8)  # allow passive failure window to expire
    counts = requests()
    assert counts.get('backend1') == 5 and counts.get('backend2') == 5, f"recovery not balanced: {counts}"
    report['checks']['recovery'] = counts
    emit('PASS: both backends responding after restart')

    emit('--- host port 3000 negative test ---')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        error_code = sock.connect_ex((URL_HOST, 3000))
    assert error_code != 0, 'Something listening on host port 3000; investigate before claiming isolation'
    report['checks']['host_port_3000'] = 'PASS - no TCP listener on host localhost:3000'
    emit('PASS: connection refused on host localhost:3000')

    # This endpoint returns 204 No Content; it is tested without JSON decoding.
    conn = http.client.HTTPConnection(URL_HOST, BASE_PORT, timeout=5)
    try:
        conn.request('GET', '/favicon.ico')
        r = conn.getresponse()
        r.read()
        assert r.status == 204, f'favicon expected 204, got {r.status}'
        emit('PASS: /favicon.ico HTTP 204 (no missing icon 404)')
        report['checks']['favicon'] = 'PASS'
    finally:
        conn.close()

    emit('NOTE: Browser Console/Network tab still requires manual inspection.')
    report['notes'].append('Browser DevTools not checked by automated script')
    report['overall'] = 'PASS - automated checks only'


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        report['overall'] = 'FAIL'
        report['error'] = str(e)
        emit('FAIL: ' + str(e))
        raise
    finally:
        (OUT/'qa-report.json').write_text(json.dumps(report, indent=2) + '\n')
        (OUT/'qa-evidence.txt').write_text('\n'.join(lines) + '\n')
