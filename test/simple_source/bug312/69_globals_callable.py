# Test: storing built-in types and functions via globals()
# From enjuly-A.pyc lines 1-13: globals()['name'] = builtin if ... else builtin
globals()['h2so4'] = int if False else int
globals()['feso4'] = bytes if False else bytes
globals()['agno3'] = vars if False else vars
globals()['h2'] = callable if False else callable
globals()['h2o3'] = eval if False else eval
globals()['agno4'] = list if False else list
globals()['h3o'] = map if False else map
globals()['ch2oh4p2so4'] = __import__ if False else __import__

print(h2so4(42))
print(h2(print))
print(agno4(h3o(h2so4, ['1', '2', '3'])))
