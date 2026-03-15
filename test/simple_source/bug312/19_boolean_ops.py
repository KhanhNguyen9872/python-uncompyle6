# Test boolean operators
def check(a, b, c):
    if a and b:
        print("a and b")
    if a or b:
        print("a or b")
    if not a:
        print("not a")
    if a and b and c:
        print("all three")
    if a or b or c:
        print("at least one")

check(True, False, True)
