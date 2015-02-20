import nltk
from nltk.corpus import inaugural
import unittest

from app import analyze_words, analyze_text, get_word_frequency_at, \
    analyze_sentences, get_common_word_threshold, get_uncommon_word_threshold


class TestWriteBetter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nltk.download('inaugural')

    def setUp(self):
        self.test_corpus = inaugural.raw('2009-Obama.txt')

    def test_analyze_words_obama(self):
        results = analyze_words(self.test_corpus)
        self.assertEquals(results[u'America']['count'], 10)
        self.assertEquals(results[u'America']['pos_tag'], 'NNP')

    def test_analyze_words_simple(self):
        results = analyze_words("Hi hi hello")
        self.assertEquals(results[u'hi']['count'], 2)
        self.assertEquals(results[u'hello']['count'], 1)
        self.assertEquals(results[u'hi']['pos_tag'], 'NN')
        self.assertEquals(results[u'hello']['pos_tag'], 'NN')

    def test_get_word_frequency_at(self):
        text = "This is a sentence. This is a sentence. I am testing."
        tokens = nltk.tokenize.word_tokenize(text)
        fdist = nltk.FreqDist(tokens)

        self.assertEqual(get_word_frequency_at(fdist, 0.1), 3)
        self.assertEqual(get_word_frequency_at(fdist, 0.5), 2)
        self.assertEqual(get_word_frequency_at(fdist, 0.9), 1)

    def test_analyze_sentences(self):
        text = "This is a sentence. This is a sentence. I am testing."
        tokens = nltk.tokenize.word_tokenize(text)
        fdist = nltk.FreqDist(tokens)

        common_word_threshold = get_common_word_threshold(fdist)
        uncommon_word_threshold = get_uncommon_word_threshold(fdist)

        results = analyze_sentences(text)
        for sentence, result in results.items():
            for word in result['common_words']:
                self.assertTrue(fdist[word] >= common_word_threshold)
            for word in result['uncommon_words']:
                self.assertTrue(fdist[word] <= uncommon_word_threshold)

    def test_analyze_text(self):
        score = analyze_text(self.test_corpus)
        self.assertTrue(score >= 0)


if __name__ == '__main__':
    unittest.main()
