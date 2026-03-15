# Test while-if-return (simplest form)
def test(a):
    while a > 0:
        if a == 1:
            return True
        a -= 1
    return False
