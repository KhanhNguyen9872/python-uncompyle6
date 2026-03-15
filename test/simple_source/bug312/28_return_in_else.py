# Adapted from bug35/05_return_in_else.py
# Tests return in else branch
def parseline(line):
    if not line:
        return 5
    elif line > 0:
        return 3
    return 6

print(parseline(0))
print(parseline(1))
print(parseline(-1))
