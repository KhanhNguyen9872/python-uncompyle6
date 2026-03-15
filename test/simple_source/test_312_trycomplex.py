# Test try-except-else-finally

# Full try-except-else-finally
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("cannot divide by zero")
        return None
    else:
        print("division successful")
        return result
    finally:
        print("cleanup done")

print(divide(10, 2))
print(divide(10, 0))

# Multiple except clauses
def convert(value):
    try:
        return int(value)
    except ValueError:
        print("not a number")
    except TypeError:
        print("wrong type")
    return None

print(convert("42"))
print(convert("abc"))
