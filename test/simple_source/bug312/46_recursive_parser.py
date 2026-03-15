# Hard: recursive parser (fewer paths)
def parse_number(text, pos):
    if pos >= len(text):
        return 0, pos
    if not text[pos].isdigit():
        return 0, pos
    n = 0
    while pos < len(text) and text[pos].isdigit():
        n = n * 10 + int(text[pos])
        pos += 1
    return n, pos

print(parse_number("123abc", 0))
print(parse_number("abc", 0))
print(parse_number("", 0))
