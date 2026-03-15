# Test nested if/elif/else
def classify(x):
    if x > 100:
        return "huge"
    elif x > 50:
        return "large"
    elif x > 10:
        return "medium"
    elif x > 0:
        return "small"
    else:
        return "zero or negative"

print(classify(200))
print(classify(75))
print(classify(25))
print(classify(5))
print(classify(-1))
