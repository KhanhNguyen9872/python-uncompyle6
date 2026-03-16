# Test: for loop using globals() for iteration variable storage
# From enjuly-A.pyc: for globals()['enjuly19_'] in globals()['july']:
data = [65, 66, 67]
globals()['data'] = data
result = ''
for globals()['item'] in globals()['data']:
    result += str(globals()['item'])
print(result)
