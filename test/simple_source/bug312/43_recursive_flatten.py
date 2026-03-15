# Hard: recursive tree traversal
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            for sub in flatten(item):
                result.append(sub)
        else:
            result.append(item)
    return result

nested = [1, [2, 3], [4, [5, 6]], 7]
print(flatten(nested))
