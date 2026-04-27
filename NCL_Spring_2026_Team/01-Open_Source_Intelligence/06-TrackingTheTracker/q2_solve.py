import json, sqlite3, math
from datetime import datetime, timezone

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

con = sqlite3.connect("logs.kismet")
track = con.execute("""
    SELECT AVG(lat), AVG(lon) FROM packets
    WHERE lat != 0 AND lon != 0 GROUP BY ts_sec ORDER BY ts_sec
""").fetchall()
print(f"Agent's track: {len(track)} GPS points")

with open('raleigh_20260325.geojson') as f:
    data = json.load(f)
print(f"Incidents on 2026-03-25: {len(data.get('features',[]))}\n")

results = []
for feat in data.get('features', []):
    p = feat.get('properties', {})
    g = feat.get('geometry') or {}
    coords = g.get('coordinates') if g else None
    
    lat = p.get('latitude'); lon = p.get('longitude')
    if (lat is None or lon is None or lat == 0 or lon == 0) and coords:
        lon, lat = coords[0], coords[1]
    if not lat or not lon:
        continue
    
    d = min(haversine(lat, lon, tlat, tlon) for tlat, tlon in track)
    
    rd = p.get('reported_date')
    rd_str = datetime.fromtimestamp(rd/1000, timezone.utc).strftime('%H:%M') if rd else '?'
    
    results.append((d, p.get('case_number'), p.get('crime_description'),
                    p.get('reported_block_address'), rd_str, lat, lon))

results.sort()

print(f"Top 15 incidents closest to agent's route:")
print(f"{'Dist':>7s}  {'Case':<14s}  {'UTC':<6s}  {'Address':<35s}  Description")
print('-'*110)
for d, cn, desc, addr, rd_str, lat, lon in results[:15]:
    print(f"  {d*1000:5.0f}m  {str(cn or '?'):<14s}  {rd_str:<6s}  {(addr or '?')[:33]:<35s}  {desc or '?'}")

if results:
    closest = results[0]
    print(f"\n{'='*70}")
    print(f">>> Q2 ANSWER: case_number = {closest[1]}")
    print(f"    Distance from agent's track: {closest[0]*1000:.0f} m")
    print(f"    Description: {closest[2]}")
    print(f"    Location: {closest[3]}")
    print(f"{'='*70}")
