# Adapted from bug36/05-for-ifelse.py
# Test nested for with if-else
def process(fp, items):
    for line in fp:
        for prefix in items:
            print(prefix)
        if line and fp:
            print("yes")
        else:
            print("no")
