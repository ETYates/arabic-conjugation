from collections import defaultdict

class Radical:
    """
    This class represents the semitic triconsonantal radical system of morphology in Arabic.
    ...
    Attributes
    ----------
    first : char
        first consonant in radical
    middle : char
        middle consonant in radical
    last : char
        last consonant in radical
    vowel1 : char
        first characteristic vowel for verb
    vowel2 : char
        second characteristic vowel for verb
    """
    def __init__(self, fundamentals):
        """
        Populates radical attributes with respective character values.

        @param
        ------
            fundamentals : str
                five characters representing first, middle, last consonants,
                and the two characteristic vowels, in that order.
        """
        bound = 3
        fundamentals = list(fundamentals)
        self.first, self.middle, self.last = fundamentals[:bound]
        self.vowel1, self.vowel2 = fundamentals[bound:]


class FeatureNames:
    """
    Converts single letter variable names into Arabic grammatical terminology.
    ...
    Attributes
    ----------
    int2mood : list 
        list containing names for each grammatical mood
    int2pattern : list
        list containing Arabic names for each morphological "pattern" in the 
        semitic system of conjugation.
    int2voice : list 
        list containing names for each grammatical voice-active and passive.
    """
    int2mood = ['past', 'indicative', 'subjunctive', 'jussive']
    int2pattern = ['fa`ala',   'fa``ala',   'fā`ala', 
                   'ʾaf`ala',  'tafa``ala', 'tafā`ala',
                   'infa`ala', 'ifta`ala',  'if`alla',
                   'istafʿala']
    # These are the names for each pattern in Arabic grammatical terminology.
    # They are based off the verb radical (f ` l) in each respective pattern.
    int2voice = ['active', 'passive']


class Conjugation:
    """
    This class represents the core of the rule-based approach to Arabic
    conjugation. It contains the variables used in the paper for counting and
    identifying features, along with the matrices containing endings, prefixes,
    and patterns. Single letter variable names are used for easy reference to
    variables in the original paper.

    Attributes
    ----------
    i : list
        array containing person and number labels
    j : int
        number of grammatical moods
    l : int
        number of grammatical voices (0 = active, 1 = passive)
    p : defaultdict
        Dictionary containing prefixes accessed by their person and number
        labels.
    q : defaultdict
        dictionary containing non-past suffixes
    q_prime : defaultdict
        dictionary containing past-tense suffixes
    s : defaultdict
        dictionary containing non-past conjugational patterns or "forms"
    s_prime : defaultdict
        dictionary containing past-tense conjugational patterns or "forms"
    r : defaultdict
        dictionary containing final endings for non-past forms
    radical : Radical
        instance of Radical class representing the abstract triconsonantal
        radical

    Methods
    -------
    split_and_strip(fundamentals) 
        helper function to split string and remove whitespace
    load_morphemes(filename, dictionary)
        function to load prefix and suffix matrices from files and deposits
        them in the respective dictionary
    load_patterns(filename, dictionary)
        function to load form/pattern matrices into dictionaries from
        respective file
    load_finals(filename, dictionary)
        loads final non-past suffixes into dictionary from file
    insert_pattern(l, k, j)
        loads verb radical (consonants and vowels) into the selected templatic
        form
    conjugate(self, i, j, k, l)
        main conjugation function--takes all morphological features and a verb
        and produces the desired form
    determine_final(self, form, j)
        determines the final non-past desinence based on the phonological context
    """
    i = ['1',  '2m', '2f', 
         '3m', '3f', '4', 
         '5m', '5f', '5d', 
         '6m', '6f', '6dm', 
         '6df']
    j = 3                               # Four grammatical moods.
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
        """
        Populates matrice values--loads values from files.
        
        @param
        ------
        fundamentals : str
            The characters used to load the radical and fill in morphological
            templates.
        """
        self.radical = Radical(fundamentals)
        self.load_morphemes('data/prefixes', self.p)
        self.load_morphemes('data/suffixes', self.q)
        self.load_morphemes('data/suffixes_prime', self.q_prime)
        self.load_patterns('data/forms', self.s)
        self.load_patterns('data/forms_prime', self.s_prime)
        self.load_finals('data/finals', self.r)

    def split_and_strip(self, element, delimiter):
        """
        Helper function to split strings and strip whitespace in one step.

        @param
        ------
        element : str
            string containing delimited objects
        delimiter : str
            string containing delimiter for splitting element string

        @return
        -------
        elements : list
            list containing delimited substrings in element
        """
        elements = element.split(delimiter)
        for n in range(len(elements)):
            elements[n] = elements[n].strip()
        return elements

    def load_morphemes(self, filename, dictionary):
        """
        For reading in prefixes and suffixes from text documents.

        @param
        ------
        filename : str
            name of file to be loaded
        dictionary : defaultdict 
            dictionary to which file information is saved
        """
        with open(filename) as f:
            for line in f:
                key, person = self.split_and_strip(line, '->') # MAKE THIS INTO A HELPER FUNCTION
                dictionary[key] = person

    def load_patterns(self, filename, dictionary):
        """
        For reading the semitic stem forms/patterns from text documents.

        @param
        ------
        filename : str
            name of file to be loaded
        dictionary : defaultdict 
            dictionary to which file information is saved
        """
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

    def load_finals(self, filename, dictionary):
        """
        For loading final desinences for non-past forms.

        @param
        ------
        filename : str
            name of file to be loaded
        dictionary : defaultdict 
            dictionary to which file information is saved
        """
        with open(filename) as f:
            for line in f:
                key, rules = self.split_and_strip(line, '->')
                rules = self.split_and_strip(rules, ',')
                key = int(key)
                for n in range(len(rules)):
                    result, context = self.split_and_strip(rules[n], 'after')
                    if dictionary[key] == '':
                        dictionary[key] = defaultdict(lambda: '')
                        dictionary[key][context] = result
                    else:
                        dictionary[key][context] = result

    def insert_pattern(self, l, k, j):
        """
        Fills abstract patterns with consonants and vowels from verb radical.

        @param
        ------
        l : int
            voice
        k : int
            pattern/form
        j : int 
            mood

        @return 
        -------
        pattern : str
            morphological 'pattern' or 'form' with radical consonants and vowels
            substituted into the respective variables
        """
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
       
    def conjugate(self, i, j, k, l):
        """
        Main conjugation formula.

        @param
        ------
        i : str
            person/number
        j : int
            mood
        k : int
            pattern/form
        l : int
            voice

        @return
        -------
        final verb form output
        """
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

    def determine_final(self, form, j):
        """
        Determines which non-past final desinence to choose, based on
        phonological context.

        @param
        ------
        form : str
            morphological stem to be analyzed
        j : int
            morphological mood
        """
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
