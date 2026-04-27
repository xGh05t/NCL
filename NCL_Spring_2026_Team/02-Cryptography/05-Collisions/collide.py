#!/usr/bin/env python3
import socket, hashlib, re, sys, time

HOST, PORT = "services.cityinthe.cloud", 31337

def recv_until(s, marker, timeout=10):
    s.settimeout(timeout); buf = b""
    while marker not in buf:
        try:
            ch = s.recv(4096)
            if not ch: break
            buf += ch
        except socket.timeout:
            break
    return buf

def find_collision(target):
    i = 0
    while True:
        g = str(i).encode()
        if hashlib.sha1(g).hexdigest().startswith(target):
            return g, i
        i += 1

s = socket.socket(); s.connect((HOST, PORT))
banner = recv_until(s, b"guess>")
target = re.search(rb"first 6 hex chars\): ([0-9a-f]{6})", banner).group(1).decode()
print(f"[+] Target: {target}")

t0 = time.time()
guess, tried = find_collision(target)
print(f"[+] Found '{guess.decode()}' after {tried:,} tries in {time.time()-t0:.1f}s")

s.sendall(guess + b"\n")
print(recv_until(s, b"guess>", timeout=10).decode(errors='replace'))
s.settimeout(3)
try:
    while True:
        ch = s.recv(4096)
        if not ch: break
        sys.stdout.write(ch.decode(errors='replace'))
except: pass
s.close()
