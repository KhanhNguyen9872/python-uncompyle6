# Tests while with break
def countdown(n):
    while n > 0:
        if n == 3:
            break
        n -= 1
    return n

print(countdown(5))
print(countdown(2))
