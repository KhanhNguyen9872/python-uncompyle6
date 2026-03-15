# Hard: number base conversion
def to_base(n, base):
    if n == 0:
        return "0"
    digits = "0123456789ABCDEF"
    result = ""
    negative = False
    if n < 0:
        negative = True
        n = -n
    while n > 0:
        result = digits[n % base] + result
        n = n // base
    if negative:
        result = "-" + result
    return result

print(to_base(255, 16))
print(to_base(255, 2))
print(to_base(255, 8))
print(to_base(0, 10))
print(to_base(-42, 10))
