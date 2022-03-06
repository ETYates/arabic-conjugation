import unittest

from arabic_verb import Radical, Conjugation, FeatureNames

"""
def test():
    names = FeatureNames()
    conj = Conjugation('qtlua')
    for pattern in range(conj.k+1):
        for mood in range(conj.j+1):
            for voice in range(conj.l+1):
                for person in conj.i:
                    print(names.int2pattern[pattern], end=' ')
                    print(names.int2voice[voice], end=' ')
                    print(names.int2mood[mood], end=' ')
                    print(person, end=' ')
                    print(person, mood, pattern, voice)
                    print(conj.conjugate(person, mood, pattern, voice))
test()
"""
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

