from collections import defaultdict
import pprint
pp = pprint.PrettyPrinter(indent=4)

class Radical:
    
    # Model of the semantic three letter system in semitic languages. In the
    # case of Arabic, also includes two characteristic vowels.
    first = None
    middle = None
    last = None
    vowel1 = None
    vowel2 = None

    def __init__(self, fundamentals):
        fundamentals = list(fundamentals)
        self.first, self.middle, self.last = fundamentals[:3]
        self.vowel1, self.vowel2 = fundamentals[3:5]

class Conjugation:
    # Single letter variable names are used for easy reference to variables
    # in the original paper.
    i = [
        '1', '2m', '2f', 
        '3m', '3f', '4', 
        '5m', '5f', '5d', 
        '6m', '6f', '6dm', 
        '6df']
    j = 3 # Four moods.
    k = 9 # Ten forms, or "patterns".
    l = 1 # Two voices: active and passive.
    p = defaultdict(lambda: 't') # Prefixes.
    q = defaultdict(lambda: '') # Non-past suffixes.
    q_prime = defaultdict(lambda: '') # Past suffixes.
    s = defaultdict(lambda: '') # Non-past patterns.
    s_prime = defaultdict(lambda: '') # Past patterns.
    r = defaultdict(lambda: '0') # Final desinences.
    radical = None # Original three consonant semitic radical.

    def __init__(self, fundamentals):
        self.radical = Radical(fundamentals)
        self.load_morphemes('prefixes.txt', self.p)
        self.load_morphemes('suffixes.txt', self.q)
        self.load_morphemes('suffixes_prime.txt', self.q_prime)
        self.load_patterns('forms.txt', self.s)
        self.load_patterns('forms_prime.txt', self.s_prime)
        self.load_finals('finals.txt', self.r)

    # For reading in prefixes and suffixes from text documents.
    def load_morphemes(self, filename, dictionary):
        with open(filename) as f:
            for line in f:
                key, person = line.split('->')
                key = key.strip()
                person = person.strip()
                dictionary[key] = person

    # For reading the semitic stem forms/patterns from text documents.
    def load_patterns(self, filename, dictionary):
        with open(filename) as f:
            for line in f:
                keys, pattern = line.split('->')
                keys = keys.strip()
                pattern = pattern.strip()
                key1, key2 = keys.split(',')
                key1 = int(key1)
                key2 = int(key2)
                if dictionary[key1] == '':
                    dictionary[key1] = defaultdict(lambda: None)
                    dictionary[key1][key2] = pattern
                else:
                    dictionary[key1][key2] = pattern
        # pp.pprint(dict(dictionary))

    # For loading final desinences for non-past forms.
    def load_finals(self, filename, dictionary):
        with open(filename) as f:
            for line in f:
                key, rules = line.split('->')
                key = key.strip()
                key = int(key)
                rules = rules.split(',')
                for n in range(len(rules)):
                    rules[n] = rules[n].strip()
                    result, context = rules[n].split('after')
                    result = result.strip()
                    context = context.strip()
                    if dictionary[key] == '0':
                        dictionary[key] = defaultdict(lambda: '0')
                        dictionary[key][context] = result
                    else:
                        dictionary[key][context] = result
        pp.pprint(dict(dictionary))

    # Fills abstract patterns with consonants and vowels from verb radical.
    def insert_pattern(self, l, k, j):
        if j == 0:
            pattern = self.s_prime[l][k]
        else:
            pattern = self.s[l][k]
        pattern = pattern.replace('F', self.radical.first)
        pattern = pattern.replace('M', self.radical.middle)
        pattern = pattern.replace('L', self.radical.last)
        pattern = pattern.replace('A', self.radical.vowel1)
        pattern = pattern.replace('E', self.radical.vowel2)
        return pattern
       
    # Main conjugation formula.
    def conjugate(self, i, j, k, l):
        pattern = self.insert_pattern(l, k, j)
        if j == 0:
            suffix = self.q_prime[i]
            verb = pattern + suffix
        else:
            prefix = self.p[i]
            suffix = self.q[i]
            form = prefix + pattern + suffix
            final = self.determine_final(form, j)
            verb = form + final
        verb = verb.replace('0', '')
        return verb

    # Determines which non-past final desinence to choose, based on
    # phonological context.
    def determine_final(self, form, j):
        final = form[-2:]
        if final in self.r[j]:
            return self.r[j][final]
        else:
            if final[-1:] not in 'aiu':
                return self.r[j]['C']
            else: 
                return 'ERROR'


def test():
    conj = Conjugation('qtlua')
    conj.insert_pattern(0, 1, 0)
    conj.insert_pattern(0, 1, 1)
    for n in range(conj.l):
        for o in range(conj.j):
            for p in range(conj.k):
                for q in conj.i:
                    place = f"l={n}, j={o}, k={p}, i={q}"
                    # print(place)
                    print(conj.conjugate(q, o, 0, n))

test()
