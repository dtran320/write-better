import nltk
from nltk import FreqDist
from nltk.tokenize import sent_tokenize


def get_words(text, lower=False):
    tokens = nltk.tokenize.word_tokenize(text)
    if lower:
        return [word.lower() for word in tokens]
    else:
        return tokens


def get_fdist(text):
    return FreqDist(get_words(text, lower=True))


def analyze_words(text):
    words = get_words(text)
    pos_tags = nltk.pos_tag(words)

    fdist = get_fdist(text)

    result_dict = {}

    for word, word_type in pos_tags:
        result_dict[word] = {
            'count': fdist[word.lower()],
            'pos_tag': word_type
        }

    return result_dict


def analyze_sentences(text):
    sent_tokens = sent_tokenize(text)

    fdist = get_fdist(text)
    n_of_words = fdist.N()

    # Get the frequency of the word at the top 25% of fdist
    common_word_threshold = fdist.freq(fdist.most_common(n_of_words // 4)[-1])
    uncommon_word_threshold = 5 # TODO: Get bottom 25% threshold

    result_dict = {}

    for sentence in sent_tokens:
        common_words = []
        uncommon_words = []
        words = get_words(sentence, lower=True)

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


def analyze_text(text):
    sent_tokens = sent_tokenize(text)
    previous_sentence_len = len(sent_tokens[0])
    score = 0

    for sentence in sent_tokens:
        curr_sentence_len = len(sentence)
        score += abs(curr_sentence_len - previous_sentence_len)

    return score

