import nltk
from nltk import FreqDist
from nltk.tokenize import sent_tokenize

def analyze_words(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    fdist = FreqDist(tokens)

    result_dict = {}

    for word, word_type in pos_tags:
        result_dict[word] = {
            'count': fdist[word],
            'pos_tag': word_type
        }

    return result_dict

def analyze_sentences(text):
    sent_tokens = sent_tokenize(text)
    result_dict = {}
    for sentence in sent_tokens:
        result_dict[sentence] = {
            'length': len(sentence),
            'common_words': [],
            'uncommon_words': []
        }
        
    return result_dict

