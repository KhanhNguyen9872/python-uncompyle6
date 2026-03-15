# Adapted from bug27+/05_while_if_continue.py
# Test while-if-continue with return
def func(a, b):
    while a:
        if b:
            continue
        return False
    return True
