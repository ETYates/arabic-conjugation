# Arabic Conjugation

This program is a partial implementation of a computational analysis of Arabic
conjugation by D. Bargelli and J. Lambek (cited below). With this program, 
every form of every Arabic verb should be generated. With this program, data
can be generated for use in linguistic annotation for machine learning.

The following is sample output:

```
fa`ala active past 1 qataltu
fa`ala active past 2m qatalta
fa`ala active past 2f qatalti
fa`ala active past 3m qatala
fa`ala active past 3f qatalat
fa`ala active past 4 qatalnaa
fa`ala active past 5m qataltum
fa`ala active past 5f qataltuma
fa`ala active past 5d qataltumaa
fa`ala active past 6m qataluu
fa`ala active past 6f qatalna
fa`ala active past 6dm qatalaa
fa`ala active past 6df qataltaa
```

This project is a proof of concept. Many languages are resource-poor and
are not conducive towards the quick creation of annotated corpra (i.e. 
minority languages, dead languages). Morphology is important to Natural
Language Processing because many languages, unlike English and Chinese, 
hold critical semantic and structural information within the word level
(at the morpheme level). Therefore, morphological annotation for a
a language with complex morphology (such as Arabic and other Semitic languages)
is crucial. 

The mathematician Joachim Lambek wrote multiple mathematical analyses of
conjugational systems in various languages (including French, Latin, Hebrew,
Arabic, and Turkish, among others). These analyses heavily utilized rewrite 
systems. This implementation of Lambek and Bargelli's analysis utilizes
templatic data in which letters are rewritten and morphemes concatenated.

In the context of Arabic, the program (very basically) selects a template 
```
FaMEL
``` 
with F, M, L respectively representing the first, middle, and last radicals
in the templatic semitic root system (usually consisting of three
consonants). 

TO DOs:
- Implement phonological rules for (t), and section symbol.
- Implement morphological rules for weak verbs. 
- Verify generated forms against pre-annotated data.

D. Bargelli and J. Lambek, "A Computational Approach to Arabic Conjugation"
Linguistic Analysis 31, 1-2 (2001): 110-131.
