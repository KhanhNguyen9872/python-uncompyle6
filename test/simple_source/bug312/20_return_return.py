# Adapted from bug36/00_return_return_bug.py
# Bug: 2nd return not detected outside of if/then
# RUNNABLE!
def return_return_bug(foo):
    if foo == 'say_hello':
        return "hello"
    return "world"

print(return_return_bug('say_hello'))
print(return_return_bug('world'))
