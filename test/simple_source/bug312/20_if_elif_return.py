# Adapted from bug36/00_if_elif.py
# Bug: not detecting end bounds of if elif
# RUNNABLE!
def testit(b):
    if b == 1:
        a = 1
    elif b == 2:
        a = 2
    else:
        a = 4
    return a

print(testit(1))
print(testit(2))
print(testit(3))
