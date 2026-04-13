#!/usr/bin/env python3
import sys
path = sys.argv[1]
with open(path,'rb') as f: data = f.read()
salt = data[:16]
for ver, page_size, kdf_iter, hmac_len in [(4,4096,256000,64),(3,1024,64000,20)]:
    if len(data) < page_size: continue
    page1 = data[:page_size]
    reserve = 16 + hmac_len
    print(f"$sqlcipher$4${ver}$1${salt.hex()}${kdf_iter}${page_size}$"
          f"{page1[16:-reserve].hex()}${page1[-reserve:-hmac_len].hex()}"
          f"${page1[-hmac_len:].hex()}")
