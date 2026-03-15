# Tests for 3.12 try/except
try:
    x = 1 / 0
except ZeroDivisionError:
    print("caught")
