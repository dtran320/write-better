import nltk
from nltk import FreqDist

def analyze_words(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    fdist = FreqDist(text)

    result_dict = {}

    for word, word_type in pos_tags:
        result_dict[word] = {
            'count': fdist[word],
            'pos_tag': word_type
        }

    return result_dict
