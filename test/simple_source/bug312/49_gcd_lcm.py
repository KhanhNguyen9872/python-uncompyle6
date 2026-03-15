# Hard: GCD algorithm (no swap)
def gcd(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

print(gcd(48, 18))
print(gcd(100, 75))
print(gcd(17, 5))
