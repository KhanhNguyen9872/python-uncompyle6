# Hard: stack-based expression evaluator
def evaluate(expr):
    stack = []
    for token in expr.split():
        if token.isdigit():
            stack.append(int(token))
        elif token == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif token == '-':
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif token == '*':
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        else:
            break
    if len(stack) == 1:
        return stack[0]
    return None

print(evaluate("3 4 + 2 *"))
print(evaluate("5 3 -"))
print(evaluate("2 3 4 + *"))
