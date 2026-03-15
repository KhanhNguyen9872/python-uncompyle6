# Hard: counter simulation using dict
counter = {"val": 0, "limit": 5}

def tick(c):
    c["val"] = c["val"] + 1
    return c["val"] <= c["limit"]

while tick(counter):
    print(counter["val"])
