#!/usr/bin/env python3
import sqlcipher3, shutil, sys, os, tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed

DB = 'data.db'
WORDLIST = sys.argv[1] if len(sys.argv) > 1 else 'mutated.txt'

def test_one(args):
    pwd, idx, tmpdir = args
    tmp = f"{tmpdir}/t{idx}.db"
    try: shutil.copy(DB, tmp)
    except: return None
    for compat in [4, 3]:
        con = None
        try:
            con = sqlcipher3.connect(tmp)
            cur = con.cursor()
            esc = pwd.replace("'","''")
            cur.execute(f"PRAGMA key = '{esc}'")
            if compat != 4:
                cur.execute(f"PRAGMA cipher_compatibility = {compat}")
            cur.execute("SELECT count(*) FROM sqlite_master")
            n = cur.fetchone()[0]
            con.close()
            try: os.remove(tmp)
            except: pass
            return (pwd, compat, n)
        except Exception:
            try:
                if con: con.close()
            except: pass
    try: os.remove(tmp)
    except: pass
    return None

if __name__ == '__main__':
    with open(WORDLIST, errors='ignore') as f:
        cands = [l.rstrip('\n') for l in f if l.strip()]
    print(f"Loaded {len(cands)} candidates from {WORDLIST}")
    tmpdir = tempfile.mkdtemp()
    sys.stderr = open(os.devnull, 'w')
    found = None
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        futs = {ex.submit(test_one, (p, i, tmpdir)): p for i, p in enumerate(cands)}
        done = 0
        for fut in as_completed(futs):
            done += 1
            r = fut.result()
            if r:
                found = r
                break
            if done % 500 == 0:
                sys.stderr = sys.__stderr__
                print(f"  {done}/{len(cands)}")
                sys.stderr = open(os.devnull, 'w')
    sys.stderr = sys.__stderr__
    if not found:
        print("No match"); sys.exit(1)
    pwd, compat, n = found
    print(f"\n*** HIT *** password={pwd!r} compat={compat}")
    con = sqlcipher3.connect(DB); cur = con.cursor()
    esc = pwd.replace("'","''")
    cur.execute(f"PRAGMA key='{esc}'")
    if compat != 4: cur.execute(f"PRAGMA cipher_compatibility = {compat}")
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for (t,) in cur.fetchall():
        if t.startswith('sqlite_'): continue
        cur.execute(f"SELECT * FROM '{t}'")
        cols = [d[0] for d in cur.description]
        print(f"\n=== {t} ===\nCOLUMNS: {cols}")
        for row in cur.fetchall(): print(" ROW:", row)
