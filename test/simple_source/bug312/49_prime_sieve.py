# Hard: prime sieve
def sieve(limit):
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False
    p = 2
    while p * p <= limit:
        if is_prime[p]:
            i = p * p
            while i <= limit:
                is_prime[i] = False
                i += p
        p += 1
    result = []
    for i in range(len(is_prime)):
        if is_prime[i]:
            result.append(i)
    return result

print(sieve(50))
