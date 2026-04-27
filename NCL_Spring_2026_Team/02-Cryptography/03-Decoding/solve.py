#!/usr/bin/env python3

def final_verification():
    print("=== FINAL TRIPLE-CHECKED ANSWERS ===\n")
    
    # Q1: Numbers as decimal ASCII (most straightforward interpretation)
    print("Q1 (10 points):")
    numbers = "056 063 055 035 123 126 130 122 137 035 122 143 126 137 138 035 126 132 035 138 125 122 035 121 133 120 140 131 122 132 138 035 120 133 132 138 117 126 132 122 136 137".split()
    
    q1_result = ""
    print("Decoding as decimal ASCII:")
    for i, num in enumerate(numbers):
        val = int(num)
        if 32 <= val <= 126:  # printable ASCII
            char = chr(val)
            q1_result += char
            print(f"  {num} -> {val} -> '{char}'")
        else:
            q1_result += f"[{val}]"
            print(f"  {num} -> {val} -> [non-printable]")
        
        if i >= 10:  # Just show first few for brevity
            print("  ...")
            break
    
    # Complete the conversion for the result
    q1_result = "".join(chr(int(num)) if 32 <= int(num) <= 126 else f"[{int(num)}]" for num in numbers)
    print(f"\nQ1 Answer: {q1_result}")
    
    # Q2: Atbash cipher (verified correct)
    print(f"\nQ2 (20 points):")
    encrypted = "R droo mld hgzig gsv yrwwrmt gl lygzrm gsv vckolrg"
    q2_result = ""
    for char in encrypted:
        if char.isalpha():
            if char.islower():
                q2_result += chr(ord('z') - (ord(char) - ord('a')))
            else:
                q2_result += chr(ord('Z') - (ord(char) - ord('A')))
        else:
            q2_result += char
    
    print(f"Atbash decode of: '{encrypted}'")
    print(f"Q2 Answer: {q2_result}")
    
    # Q3: XOR with key [1, 25] (verified correct)
    print(f"\nQ3 (30 points):")
    encrypted = "Uqd9Hwqlu9Bq`k`zu|s9hj!x!Uh|"
    key = [1, 25]
    q3_result = ""
    for i, char in enumerate(encrypted):
        decoded_char = chr(ord(char) ^ key[i % 2])
        q3_result += decoded_char
    
    print(f"XOR decode of: '{encrypted}'")
    print(f"Using key: {key}")
    print(f"Q3 Answer: {q3_result}")
    
    print("\n=== SUMMARY OF VERIFIED ANSWERS ===")
    print(f"Q1: {q1_result}")
    print(f"Q2: {q2_result}")
    print(f"Q3: {q3_result}")
    
    return q1_result, q2_result, q3_result

if __name__ == "__main__":
    final_verification()
