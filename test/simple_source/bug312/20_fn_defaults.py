# Adapted from bug36/03_fn_defaults.py
# Tests function default parameters
def foo1(bar, baz=1):
    return 1

def foo2(bar, baz, qux=1):
    return 2

def foo3(bar, baz=1, qux=2):
    return 3
