# Test while with and condition (no break)
def getopt(args, n):
    while args and n > 0:
        n -= 1
    return n
