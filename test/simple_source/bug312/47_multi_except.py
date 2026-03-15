# Hard: try/except in loop at module level
results = []
items = ["1", "bad", "3", "4"]
for item in items:
    try:
        results.append(int(item))
    except:
        results.append(-1)
print(results)
