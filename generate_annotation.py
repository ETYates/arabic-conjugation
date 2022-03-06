from arabic_verb import Radical, Conjugation, FeatureNames

def main():
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
                    print(conj.conjugate(person, mood, pattern, voice))

if __name__ == "__main__":
    main()
