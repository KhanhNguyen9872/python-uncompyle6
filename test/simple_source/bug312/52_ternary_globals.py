# Test: ternary conditional + globals store
# This is the exact pattern from enjuly-A.pyc
x = 5
globals()["result"] = (bool if x > 3 else int)
