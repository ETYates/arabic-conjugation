from collections import defaultdict
import pprint
pp = pprint.PrettyPrinter(indent=4)


class Radical:
    
    # Model of the semantic three letter system in semitic languages. In the
    # case of Arabic, also includes two characteristic vowels.

    def __init__(self, fundamentals):
        bound = 3
        fundamentals = list(fundamentals)
        self.first, self.middle, self.last = fundamentals[:bound]
        self.vowel1, self.vowel2 = fundamentals[bound:]


class FeatureNames:
    # Converts single letter variable names into Arabic grammatical terminology.
    int2mood = ['past', 'indicative', 'subjunctive', 'jussive']
    int2pattern = ['fa`ala',   'fa``ala',   'fā`ala', 
                   'ʾaf`ala',  'tafa``ala', 'tafā`ala',
                   'infa`ala', 'ifta`ala', 'if`alla',
                   'istafʿala']
    # These are the names for each pattern in Arabic grammatical terminology.
    # They are based off the verb radical (f ` l) in each respective pattern.
    int2voice = ['active', 'passive']


class Conjugation:
    # Single letter variable names are used for easy reference to variables
    # in the original paper.
    i = ['1',  '2m', '2f', 
         '3m', '3f', '4', 
         '5m', '5f', '5d', 
         '6m', '6f', '6dm', 
         '6df']
    j = 3                               # Four moods.
    k = 9                               # Ten forms, or "patterns".
    l = 1                               # Two voices: active and passive.
    p = defaultdict(lambda: 't')        # Prefixes.
    q = defaultdict(lambda: '')         # Non-past suffixes.
    q_prime = defaultdict(lambda: '')   # Past suffixes.
    s = defaultdict(lambda: '')         # Non-past patterns.
    s_prime = defaultdict(lambda: '')   # Past patterns.
    r = defaultdict(lambda: '')         # Final desinences.
    radical = None                      # Original three consonant semitic radical.

    def __init__(self, fundamentals):
        self.radical = Radical(fundamentals)
        self.load_morphemes('data/prefixes', self.p)
        self.load_morphemes('data/suffixes', self.q)
        self.load_morphemes('data/suffixes_prime', self.q_prime)
        self.load_patterns('data/forms', self.s)
        self.load_patterns('data/forms_prime', self.s_prime)
        self.load_finals('data/finals', self.r)

    def split_and_strip(self, element, delimiter):
        elements = element.split(delimiter)
        for n in range(len(elements)):
            elements[n] = elements[n].strip()
        return elements

    # For reading in prefixes and suffixes from text documents.
    def load_morphemes(self, filename, dictionary):
        with open(filename) as f:
            for line in f:
                key, person = self.split_and_strip(line, '->') # MAKE THIS INTO A HELPER FUNCTION
                dictionary[key] = person

    # For reading the semitic stem forms/patterns from text documents.
    def load_patterns(self, filename, dictionary):
        with open(filename) as f:
            for line in f:
                keys, pattern = self.split_and_strip(line, '->')
                key1, key2 = self.split_and_strip(keys, ',')
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
                key, rules = self.split_and_strip(line, '->')
                rules = self.split_and_strip(rules, ',')
                key = int(key)
                for n in range(len(rules)):
                    result, context = self.split_and_strip(rules[n], 'after')
                    if dictionary[key] == '':
                        dictionary[key] = defaultdict(lambda: '0')
                        dictionary[key][context] = result
                    else:
                        dictionary[key][context] = result

    # Fills abstract patterns with consonants and vowels from verb radical.
    def insert_pattern(self, l, k, j):
        if j == 0:
            pattern = self.s_prime[l][k]
        else:
            pattern = self.s[l][k]
        if pattern == 'EMPTY':
            return pattern
        pattern = pattern.replace('F', self.radical.first)
        pattern = pattern.replace('M', self.radical.middle)
        pattern = pattern.replace('L', self.radical.last)
        pattern = pattern.replace('A', self.radical.vowel1)
        pattern = pattern.replace('E', self.radical.vowel2)
        return pattern
       
    # Main conjugation formula.
    def conjugate(self, i, j, k, l):
        pattern = self.insert_pattern(l, k, j)
        if pattern == 'EMPTY':
            return 'EMPTY'
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
        if j == 3:
            return ''
        final = form[-2:]
        if final in self.r[j]:
            return self.r[j][final]
        else:
            if type(self.r[j]) == str:
                return self.r[j]
            else:
                return self.r[j]['C']


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
                    print(conj.conjugate(person, mood, pattern, voice))
test()
