from collections import OrderedDict

import nltk
from nltk import FreqDist
from nltk.tokenize import sent_tokenize
import numpy


COMMON_THRESH = 0.1
UNCOMMON_THRESH = 0.9


def get_words(text, lower=False):
    """Returns word tokens from the text, optionally
    in lowercase."""

    tokens = nltk.tokenize.word_tokenize(text)
    if lower:
        return [word.lower() for word in tokens]
    else:
        return tokens


def get_fdist(text):
    """Returns the frequency distribution for lowercase
    words in the text argument"""

    return FreqDist(get_words(text, lower=True))


def get_word_frequency_at(fdist, percentage):
    """Returns the frequency of the word at the given
    percentile in the word frequency distribution.
    Returns None if sample is too small."""

    n_of_words = fdist.B()
    nth = int(n_of_words * percentage)

    if nth < 1:
        nth = 1

    words = fdist.most_common(nth)

    if len(words) > 0:
        return fdist[words[-1][0]]
    else:
        return None


def get_common_word_threshold(fdist):
    """Returns frequency threshold for a common word."""

    threshold = get_word_frequency_at(fdist, COMMON_THRESH)
    if threshold:
        return threshold
    else:
        return 2


def get_uncommon_word_threshold(fdist):
    """Returns frequency threshold for an uncommon word."""

    threshold = get_word_frequency_at(fdist, UNCOMMON_THRESH)
    if threshold:
        return threshold
    else:
        return 1


def analyze_words(text, ordered=False):
    """Returns a dict of word-dict pairs, where
    the associated dict contains the count and POS-
    tag for the word.

    If ordered is specified, then return an OrderedDict
    sorted by count.
    """

    words = get_words(text)
    pos_tags = nltk.pos_tag(words)

    fdist = get_fdist(text)

    result_dict = {}

    for word, word_type in pos_tags:
        result_dict[word] = {
            'count': fdist[word.lower()],
            'pos_tag': word_type
        }

    if ordered:
        result_dict = OrderedDict(
            sorted(result_dict.items(), key=lambda t: t[1]['count'],
                   reverse=True))
    return result_dict


def analyze_sentences(text):
    """Returns a dict of sentence-dict pairs,
    where the associated dict contains the sentence
    length and lists of common and uncommon words
    appearing in the sentence"""

    sent_tokens = sent_tokenize(text)
    fdist = get_fdist(text)

    common_word_threshold = get_common_word_threshold(fdist)
    uncommon_word_threshold = get_uncommon_word_threshold(fdist)

    result_dict = {}

    for sentence in sent_tokens:
        common_words = []
        uncommon_words = []
        words = get_words(sentence, lower=True)

        for word in words:
            if fdist[word] >= common_word_threshold:
                common_words.append(word)
            elif fdist[word] <= uncommon_word_threshold:
                uncommon_words.append(word)

        result_dict[sentence] = {
            'length': len(sentence),
            'common_words': common_words,
            'uncommon_words': uncommon_words,
        }

    return result_dict


def analyze_text(text):
    """Returns the average relative sentence length
    difference between one sentence to the next for all
    the sentences in the text."""

    sent_tokens = sent_tokenize(text)
    previous_sentence_len = len(sent_tokens[0])

    sentence_diffs = []
    for sentence in sent_tokens:
        curr_sentence_len = len(sentence)

        # Get the relative length difference from previous
        # sentence
        relative_diff = (curr_sentence_len - previous_sentence_len) \
                        / previous_sentence_len

        sentence_diffs.append(abs(relative_diff))

        previous_sentence_len = curr_sentence_len

    # Return the mean of all sentence_diffs for an indicator
    # of sentence length variance.
    return numpy.mean(sentence_diffs)

def get_most_common_by_pos(text, pos_tag, amount=5):
    """Returns the most common words by POS-tag"""

    all_tokens = analyze_words(text)
    words = list(filter(lambda w: w[1]['pos_tag'] == pos_tag,
        all_tokens.items()
    ))

    most_common = FreqDist([w for w, r in words]).most_common(amount)
    
    return [word for word, freq in most_common]

