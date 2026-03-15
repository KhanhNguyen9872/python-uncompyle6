# Adapted from bug37/03_else_removal.py
# Tests if/else with return in both branches
def cmp(b, c):
    if b:
        if c:
            return 0
        else:
            return 1
    else:
        return -1
