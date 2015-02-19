import nltk
from nltk.corpus import inaugural
import unittest

from app import analyze_words

class TestWriteBetter(unittest.TestCase):

    def setUp(self):
        nltk.download('inaugural')
        self.test_corpus = inaugural.raw('2009-Obama.txt')

    def test_analyze_words(self):
        results = analyze_words(self.test_corpus)
        self.assertEquals(results[u'America']['count'], 10)
        self.assertEquals(results[u'America']['pos_tag'], 'NNP')

if __name__ == '__main__':
    unittest.main()