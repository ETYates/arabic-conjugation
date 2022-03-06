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

TO DOs:
- Implement phonological rules for (t), and section symbol.
- Implement morphological rules for weak verbs. 
- Verify generated forms against pre-annotated data.

D. Bargelli and J. Lambek, "A Computational Approach to Arabic Conjugation"
Linguistic Analysis 31, 1-2 (2001): 110-131.
