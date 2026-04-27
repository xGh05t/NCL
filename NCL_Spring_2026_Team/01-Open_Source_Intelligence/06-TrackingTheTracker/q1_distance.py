import sqlite3, math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

con = sqlite3.connect("logs.kismet")
rows = con.execute("""
    SELECT ts_sec, AVG(lat), AVG(lon), AVG(COALESCE(speed,0))
    FROM packets WHERE lat != 0 AND lon != 0
    GROUP BY ts_sec ORDER BY ts_sec
""").fetchall()

# Method A: raw haversine sum with a small jitter floor (3 m)
total_a = 0.0
prev = None
for ts, lat, lon, spd in rows:
    if prev:
        d = haversine(prev[1], prev[2], lat, lon)
        if d > 0.003:
            total_a += d
    prev = (ts, lat, lon)

# Method B: integrate reported speed (m/s) over time — sometimes cleaner
total_b = 0.0
prev = None
for ts, lat, lon, spd in rows:
    if prev and spd is not None:
        dt = ts - prev[0]
        if 0 < dt <= 5:
            total_b += (spd * dt) / 1000.0
    prev = (ts, lat, lon, spd)

print(f"Method A (haversine):   {total_a:.2f} km")
print(f"Method B (speed*time):  {total_b:.2f} km")
