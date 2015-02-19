import nltk

def analyze_words(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    return pos_tags
