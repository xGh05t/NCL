#!/usr/bin/env python3
"""
Unc's Encryption — ECDSA nonce reuse on secp256k1.
Usage:  python3 solve.py firmware_log.json
"""

import json, sys
from hashlib import sha256
from collections import defaultdict
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# secp256k1 curve order
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

log = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "firmware_log.json"))

# ---------- Q1: find firmware versions that share an r value ----------
groups = defaultdict(list)
for u in log["firmware_updates"]:
    groups[u["signature"]["r"]].append(u)

reused = next(g for g in groups.values() if len(g) > 1)
print("Q1:", ", ".join(u["version"] for u in reused))

# ---------- Q2: recover private key d from two reused-nonce sigs ----
a, b = reused[0], reused[1]
h1, s1 = int(a["messageHash"], 16), int(a["signature"]["s"], 16)
h2, s2 = int(b["messageHash"], 16), int(b["signature"]["s"], 16)
r      = int(a["signature"]["r"], 16)

k = (h1 - h2) * pow(s1 - s2, -1, N) % N
d = (s1 * k - h1) * pow(r, -1, N) % N
print("Q2:", d)

# ---------- Q3: AES-128-ECB with key = SHA256(d)[:16] -----------------
key = sha256(d.to_bytes(32, "big")).digest()[:16]
ct  = bytes.fromhex(log["encrypted_flag"])
flag = unpad(AES.new(key, AES.MODE_ECB).decrypt(ct), 16).decode()
print("Q3:", flag)
