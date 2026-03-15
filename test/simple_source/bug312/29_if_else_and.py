# Adapted from bug30/03_ifelse.py
# Tests if/else with function calls
def fn(args, value, default):
    if args and args[0] != '-':
        return value
    else:
        return default

print(fn(["hello"], 1, 2))
print(fn(["-x"], 1, 2))
print(fn([], 1, 2))
