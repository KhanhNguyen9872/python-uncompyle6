# Test try/except
try:
    x = 1 / 0
except ZeroDivisionError:
    print("caught")
