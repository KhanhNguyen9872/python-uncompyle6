# Test: try/except/else/finally nested inside another try/except
# From enjuly-A.pyc functiondz: try/except ZeroDivisionError with else and finally
def handler(x):
    try:
        eval("1+1")
        if "abc" == "def":
            (1, 2, 3, 4)
        else:
            pass
    except ZeroDivisionError:
        try:
            eval("2+2")
        except ZeroDivisionError:
            return "inner_error"
        else:
            pass
        finally:
            str(100)
    return "ok"

print(handler(1))
