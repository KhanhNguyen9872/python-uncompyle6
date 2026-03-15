# Adapted from bug38/03_while_bug.py
# Test while loop with if inside
import time

r = 0
while r == 1:
    print(time.time())
    if r == 1:
        r = 0
