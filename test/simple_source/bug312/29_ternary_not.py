# Adapted from bug33/08_if_else.py
# Tests conditional not in ternary
def init(modules=None):
    mods = set() if not modules else set(modules)
    return mods

print(init())
print(init([1, 2, 3]))
