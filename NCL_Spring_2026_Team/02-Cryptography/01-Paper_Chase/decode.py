# Hollerith / IBM 029 decoder
# Input: list of (column, [rows punched])
punches = [
    (1,  [0, 2]),
    (2,  [11, 2]),
    (3,  [0, 8]),
    (4,  [11]),
    (5,  [11, 7]),
    (6,  [11, 7]),   # wait - actually col 5 and col 7 both
    # ... fill in from visual reading
]

# Correct list from the card:
punches = [
    (1,[0,2]), (2,[11,2]), (3,[0,8]), (4,[11]), (5,[11,7]),
    (6,[12,1]), (7,[11,7]), (8,[11,9]), (9,[11]),
    (10,[1]), (11,[4]), (12,[0]), (13,[0]),
]

def decode(rows):
    rows = set(rows)
    zones = [z for z in (12,11,0) if z in rows]
    digits = sorted(r for r in rows if 1 <= r <= 9)

    # Single digit row
    if not zones and len(digits) == 1:
        return str(digits[0])
    # Zero alone
    if rows == {0}:
        return '0'
    # Hyphen
    if rows == {11}:
        return '-'
    # Slash
    if rows == {0, 1}:
        return '/'
    # Letters
    if len(zones) == 1 and len(digits) == 1:
        z, d = zones[0], digits[0]
        if z == 12: return chr(ord('A') + d - 1)
        if z == 11: return chr(ord('J') + d - 1)
        if z == 0 and d >= 2: return chr(ord('S') + d - 2)
    return '?'

msg = ''.join(decode(rs) for _, rs in sorted(punches))
print(f"Flag: {msg}")
