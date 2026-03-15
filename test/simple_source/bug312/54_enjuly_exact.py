# Exact enjuly-A first-block pattern (simpler version)
# Tests: bool(bool(bool(bool))) < bool(type(x > y < z))
result = bool(bool(bool(bool))) < bool(type(int(110) > int(121) < int(156)))
print(result)
