import nltk
from nltk.corpus import inaugural
import unittest

from app import analyze_words

class TestWriteBetter(unittest.TestCase):

    def setUp(self):
        nltk.download('inaugural')
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

if __name__ == '__main__':
    unittest.main()
