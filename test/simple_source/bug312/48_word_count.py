# Hard: word frequency count
def count_words(text):
    words = {}
    for word in text.split():
        words[word] = words.get(word, 0) + 1
    return words

text = "hello world hello python world hello"
result = count_words(text)
for word in result:
    print(word, result[word])
