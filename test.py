import unittest

from arabic_verb import Radical, Conjugation, FeatureNames

class TestPresentTense(unittest.TestCase):

    def test_third_person_masc_singular(self):
        conj = Conjugation('qtlua')
        generated_form = conj.conjugate('3m', 0, 0, 0)
        self.assertEqual('qatala', generated_form)

    def test_third_person_femn_singular(self):
        conj = Conjugation('qtlua')
        generated_form = conj.conjugate('3f', 0, 0, 0)
        self.assertEqual('qatalat', generated_form)

    def test_first_person_singular(self):
        conj = Conjugation('qtlua')
        generated_form = conj.conjugate('1', 0, 0, 0)
        self.assertEqual('qataltu', generated_form)

