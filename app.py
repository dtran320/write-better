import nltk
from nltk import FreqDist
from nltk.tokenize import sent_tokenize

def get_words(text):
    return nltk.tokenize.word_tokenize(text)

def lower_tokens(tokens):
    return [word.lower() for word in tokens]

def get_fdist(text):
    return FreqDist(get_words(text))

def analyze_words(text):
    words = get_words(text)
    pos_tags = nltk.pos_tag(words)
    fdist = FreqDist(lower_tokens(words))

    result_dict = {}

    for word, word_type in pos_tags:
        result_dict[word] = {
            'count': fdist[word.lower()],
            'pos_tag': word_type
        }

    return result_dict

def analyze_sentences(text):
    sent_tokens = sent_tokenize(text)
    result_dict = {}

    fdist = get_fdist(text)
    n_of_words = fdist.N()

    common_word_threshold = fdist.freq(fdist.most_common(n_of_words // 4)[-1])
    uncommon_word_threshold = 5 # Needs fixing

    for sentence in sent_tokens:
        common_words = []
        uncommon_words = []
        words = lower_tokens(get_words(sentence))

        for word in words:
            if fdist[word] > common_word_threshold:
                common_words.append(word)
            if fdist[word] < uncommon_word_threshold:
                uncommon_words.append(word)

        result_dict[sentence] = {
            'length': len(sentence),
            'common_words': common_words,
            'uncommon_words': uncommon_words,
        }

    return result_dict

