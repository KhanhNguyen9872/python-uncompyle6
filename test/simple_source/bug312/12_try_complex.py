# Test try-except in 3.12
# Simple single-except (multi-except not yet supported)
try:
    x = 1 / 0
except ZeroDivisionError:
    print("caught")
