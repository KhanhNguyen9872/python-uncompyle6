# Adapted from bug33/05_nonlocal.py
# Tests nonlocal access in closure
def not_bug():
    cache_token = 5
    def register():
        nonlocal cache_token
        return cache_token == 5
    return register()

print(not_bug())
