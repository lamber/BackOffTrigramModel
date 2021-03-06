#!/usr/bin/env python

import BackOffTrigramModelPipe
import unittest

DECIMAL_PLACES = 5

class TmpipeUnklessTest(unittest.TestCase):

    @classmethod  
    def setUpClass(cls):  
        cls.unkless_tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe("BackOffTrigramModelPipe", "test/data/pos_trigram_model_0.05K.arpa")

    def test_unicode(self):
	unicode_char = u'\xb6'
	self.unkless_tmpipe_obj.in_vocabulary(unicode_char) 

    def test_in_vocabulary(self):
        assert self.unkless_tmpipe_obj.in_vocabulary('"')
        assert self.unkless_tmpipe_obj.in_vocabulary("'s")
        assert self.unkless_tmpipe_obj.in_vocabulary('with')
        assert not self.unkless_tmpipe_obj.in_vocabulary('wax')

    def test_get_vocabulary_with_prefix(self):
        prefix = self.unkless_tmpipe_obj.vocabulary_with_prefix('c')
        self.assertListEqual(prefix, ["can"], prefix)
        prefix = self.unkless_tmpipe_obj.vocabulary_with_prefix("n")
        self.assertListEqual(prefix, ["not", "nuclear"], prefix)

    def test_unigram_probability(self):
        probability = self.unkless_tmpipe_obj.unigram_probability('"')
        self.assertAlmostEqual(probability, -2.589533, DECIMAL_PLACES, msg=probability)

        probability = self.unkless_tmpipe_obj.unigram_probability("'s")
        self.assertAlmostEqual(probability, -2.52453, DECIMAL_PLACES, msg=probability)

        probability = self.unkless_tmpipe_obj.unigram_probability('with')
        self.assertAlmostEqual(probability, -2.395761, DECIMAL_PLACES, msg=probability)

        probability = self.unkless_tmpipe_obj.unigram_probability('wax')
        self.assertIs(probability, None, msg=probability)

    def test_unigram_backoff(self):
        probability = self.unkless_tmpipe_obj.unigram_backoff('"')
        self.assertAlmostEqual(probability, 0.217034, DECIMAL_PLACES, msg=probability)

        probability = self.unkless_tmpipe_obj.unigram_backoff("'s")
        self.assertAlmostEqual(probability, -0.933541, DECIMAL_PLACES, msg=probability)

        probability = self.unkless_tmpipe_obj.unigram_backoff('wax')
        self.assertIs(probability, None, msg=probability)

    def test_in_bigrams(self):
        self.assertTrue(self.unkless_tmpipe_obj.in_bigrams(['that', 'with']))
        self.assertFalse(self.unkless_tmpipe_obj.in_bigrams(['with', 'with']))
        self.assertFalse(self.unkless_tmpipe_obj.in_bigrams(['understood', 'with']))

    def test_bigram_backoff(self):
        backoff = self.unkless_tmpipe_obj.bigram_backoff(['that', 'with'])
        self.assertAlmostEqual(backoff, -0.001158208, DECIMAL_PLACES, msg=backoff)
        backoff = self.unkless_tmpipe_obj.bigram_backoff(['understood', 'can'])
        self.assertIs(backoff, None), backoff
        backoff = self.unkless_tmpipe_obj.bigram_backoff(['with', 'with'])
        self.assertIs(backoff, None), backoff

    def test_trigram_probability(self):
        """
        Testing all backoff conditions.  See TrigramModel.h for formulas.
        """
        # attested
        probability = self.unkless_tmpipe_obj.trigram_probability(["that", "with","the"])
        self.assertAlmostEqual(probability, -0.4422206, DECIMAL_PLACES, msg=probability)
        # backedoff w1 w2 attested, w2 w3 attested
        probability = self.unkless_tmpipe_obj.trigram_probability(["and", "that","with"])
        self.assertAlmostEqual(probability, -2.333839, DECIMAL_PLACES, msg=probability)
        # backedoff w1 w2 attested, w2 w3 not
        probability = self.unkless_tmpipe_obj.trigram_probability(["and", "that","and"])
        self.assertAlmostEqual(probability, -3.66923311, DECIMAL_PLACES, msg=probability)
        # backedoff w1 w2 not attested, w2 w3 attested
        probability = self.unkless_tmpipe_obj.trigram_probability(["the", "that","government"])
        self.assertAlmostEqual(probability, -2.759567, DECIMAL_PLACES, msg=probability)
        # backedoff w1 w2 not attested, w2 w3 not attested
        probability = self.unkless_tmpipe_obj.trigram_probability(["the", "that","and"])
        self.assertAlmostEqual(probability, -3.637584, DECIMAL_PLACES, msg=probability)
        # Contains oov
        probability = self.unkless_tmpipe_obj.trigram_probability(["that", "they","understood"])
        self.assertIs(probability, None, msg=probability)

    def test_in_trigrams(self):
        attested = self.unkless_tmpipe_obj.in_trigrams(["that", "with","the"])
        self.assertTrue(attested), attested
        attested = self.unkless_tmpipe_obj.in_trigrams(["and", "that", "with"])
        self.assertFalse(attested), attested
        attested = self.unkless_tmpipe_obj.in_trigrams(["and", "that", "understood"])
        self.assertFalse(attested), attested

    def test_is_unk(self):
        self.assertFalse(self.unkless_tmpipe_obj.is_unk_model())

class TmpipeUnkfulTest(unittest.TestCase):
        
    @classmethod  
    def setUpClass(cls):  
        cls.unkful_tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe("BackOffTrigramModelPipe", "test/data/trigram_model_0.1K.arpa")

    def test_in_vocabulary(self):
        in_v = self.unkful_tmpipe_obj.in_vocabulary('that')
        self.assertEqual(in_v, 1), in_v
        in_v = self.unkful_tmpipe_obj.in_vocabulary('understood')
        self.assertEqual(in_v, 0), in_v

    def test_get_vocabulary_with_prefix(self):
        prefix = self.unkful_tmpipe_obj.vocabulary_with_prefix('c')
        self.assertListEqual(prefix, ["can", "cost", "country"], prefix)
        prefix = self.unkful_tmpipe_obj.vocabulary_with_prefix("gen")
        self.assertListEqual(prefix, ["generation", "genetic"], prefix)


    def test_unigram_probability(self):
        probability = self.unkful_tmpipe_obj.unigram_probability('"')
        self.assertAlmostEqual(probability, -2.589533, DECIMAL_PLACES, msg=probability)

        probability = self.unkful_tmpipe_obj.unigram_probability("'s")
        self.assertAlmostEqual(probability, -2.52453, DECIMAL_PLACES, msg=probability)

        probability = self.unkful_tmpipe_obj.unigram_probability('with')
        self.assertAlmostEqual(probability, -2.325526, DECIMAL_PLACES, msg=probability)

        probability = self.unkful_tmpipe_obj.unigram_probability('wax')
        self.assertAlmostEqual(probability, -0.3612903, DECIMAL_PLACES, msg=probability)

    def test_in_bigrams(self):
        self.assertTrue(self.unkful_tmpipe_obj.in_bigrams(['that', 'with']))
        self.assertTrue(self.unkful_tmpipe_obj.in_bigrams(['understood', 'can']))
        self.assertFalse(self.unkful_tmpipe_obj.in_bigrams(['with', 'with']))
        self.assertFalse(self.unkful_tmpipe_obj.in_bigrams(['http', 'understood']))

    def test_bigram_backoff(self):
        backoff = self.unkful_tmpipe_obj.bigram_backoff(['that', 'with'])
        self.assertAlmostEqual(backoff, 0.05899763, DECIMAL_PLACES, msg=backoff)
        backoff = self.unkful_tmpipe_obj.bigram_backoff(['understood', 'can'])
        self.assertAlmostEqual(backoff, 0.1654586, DECIMAL_PLACES, msg=backoff)
        backoff = self.unkful_tmpipe_obj.bigram_backoff(['with', 'with'])
        self.assertIs(backoff, None), backoff
        backoff = self.unkful_tmpipe_obj.bigram_backoff(['http', 'understood'])
        self.assertIs(backoff, None), backoff

    def test_trigram_probability(self):
        """
        Testing all backoff conditions.  See TrigramModel.h for formulas.
        """
        # attested
        probability = self.unkful_tmpipe_obj.trigram_probability(["that", "with","the"])
        self.assertAlmostEqual(probability, -0.4419316, DECIMAL_PLACES, msg=probability)
        # backedoff w1 w2 attested, w2 w3 attested
        probability = self.unkful_tmpipe_obj.trigram_probability(["and", "that","with"])
        self.assertAlmostEqual(probability, -2.27247187, DECIMAL_PLACES, msg=probability)
        # backedoff w1 w2 attested, w2 w3 not
        probability = self.unkful_tmpipe_obj.trigram_probability(["and", "that","and"])
        self.assertAlmostEqual(probability, -3.09802487, DECIMAL_PLACES, msg=probability)
        # backedoff w1 w2 not attested, w2 w3 attested
        probability = self.unkful_tmpipe_obj.trigram_probability(["the", "that","government"])
        self.assertAlmostEqual(probability, -2.763977, DECIMAL_PLACES, msg=probability)
        # backedoff w1 w2 not attested, w2 w3 not attested
        probability = self.unkful_tmpipe_obj.trigram_probability(["the", "that","and"])
        self.assertAlmostEqual(probability, -3.132153, DECIMAL_PLACES, msg=probability)
        # Contains oov
        probability = self.unkful_tmpipe_obj.trigram_probability(["that", "they","understood"])
        self.assertAlmostEqual(probability, -0.4997397, DECIMAL_PLACES, msg=probability)

    def test_in_trigrams(self):
        attested = self.unkful_tmpipe_obj.in_trigrams(["that", "with","the"])
        self.assertTrue(attested), attested
        attested = self.unkful_tmpipe_obj.in_trigrams(["and", "that", "understood"])
        self.assertTrue(attested), attested
        attested = self.unkful_tmpipe_obj.in_trigrams(["and", "that", "with"])
        self.assertFalse(attested), attested
        attested = self.unkful_tmpipe_obj.in_trigrams(["generation", "that", "understood"])
        self.assertFalse(attested), attested

    def test_is_unk(self):
        self.assertTrue(self.unkful_tmpipe_obj.is_unk_model())

if __name__ == '__main__':
    unittest.main()
