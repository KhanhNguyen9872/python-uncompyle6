# Adapted from bug36/09_while_if_while.py
# Bug: parsing the inner while
def parse(c, j, rawdata, n):
    while n:
        if c:
            j += 1
            while j < n and rawdata[j]:
                j += 1
    return -1
