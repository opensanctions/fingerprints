# fingerprints

**UPDATE 2025-05: the next generation of the `fingerprints` codebase is now included in `rigour`. See the documentation here: https://opensanctions.github.io/rigour/names/. This library is now UNMAINTAINED.**

This library helps with the generation of fingerprints for entity data. A fingerprint
in this context is understood as a simplified entity identifier, derived from it's
name or address and used for cross-referencing of entity across different datasets.

## Usage

```python
import fingerprints

fp = fingerprints.generate('Mr. Sherlock Holmes')
assert fp == 'holmes sherlock'

fp = fingerprints.generate('Siemens Aktiengesellschaft')
assert fp == 'ag siemens'

fp = fingerprints.generate('New York, New York')
assert fp == 'new york'
```

## Company type names

A significant part of what `fingerprints` does it to recognize company legal form
names. For example, `fingerprints` will be able to simplify `Общество с ограниченной ответственностью` to `ООО`, or `Aktiengesellschaft` to `AG`. The required database
is based on two different sources:

* A [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1Cw2xQ3hcZOAgnnzejlY5Sv3OeMxKePTqcRhXQU8rCAw/edit?ts=5e7754cf#gid=0) created by OCCRP.
* The ISO 20275: [Entity Legal Forms Code List](https://www.gleif.org/en/about-lei/code-lists/iso-20275-entity-legal-forms-code-list)

Wikipedia also maintains an index of [types of business entity](https://en.wikipedia.org/wiki/Types_of_business_entity).

## See also

* [Clustering in Depth](https://github.com/OpenRefine/OpenRefine/wiki/Clustering-In-Depth), part of the OpenRefine documentation discussing how to create collisions in data clustering.
* [probablepeople](https://github.com/datamade/probablepeople), parser for western names made by the brilliant folks at datamade.us.
* The study [Developing a Legal Form Classification and Extraction Approach For Company Entity Matching](https://www.tib-op.org/ojs/index.php/bis/article/view/44) by Kruse et al. (2021) investigates four approaches for identifying and classifying legal forms in company names.
* List of Legal Forms from [AnaCredit dataset](https://www.ecb.europa.eu/stats/ecb_statistics/anacredit/html/index.en.html) by ECB (one of the Annexes).
* [Transformer-based Entity Legal Form Classification](https://arxiv.org/pdf/2310.12766) by Arimond et al. (2023).

