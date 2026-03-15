# Hard: tokenizer (no nested while)
def tokenize(text):
    tokens = []
    word = ""
    for ch in text:
        if ch == ' ':
            if word:
                tokens.append(word)
                word = ""
        else:
            word += ch
    if word:
        tokens.append(word)
    return tokens

print(tokenize("hello world foo"))
print(tokenize("  a  b  c  "))
