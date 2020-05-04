ISO 20275
=========

.. image:: https://badge.fury.io/py/iso-20275.svg
.. image:: https://travis-ci.org/Gawaboumga/iso-20275-python.svg?branch=master
    :target: https://travis-ci.org/Gawaboumga/iso-20275-python

ISO standard 20275 ‘Financial Services – Entity Legal Forms (ELF)’,
Python wrapper.

Its aim is to enable legal forms within jurisdictions to be codified and
thus facilitate the classification of legal entities according to their
legal form and is codified through: `iso
20275:2019 <https://www.iso.org/obp/ui/#iso:std:iso:20275:ed-1:v1:en>`__

Column description
------------------

Everything is stored in UTF-8 format.

-  ELF Code: 4 alphanumerical characters (*[A-Z0-9]{4}*) representing
   the identifier of the legal entity type. One should pay attention
   that this code is not unique among the dataset. Indeed, a same legal
   entity can have different entries based on the language used.
-  Country of formation: Common name of the country corresponding to
   the: "English short name (using Title case)" of ISO 3166-1.
-  Country Code: Alpha-2 code of ISO 3166-1.
-  Jurisdiction of formation: ``Optional`` Common name of the
   subdivision within the country corresponding to the: "English short
   name (using Title case)" of ISO 3166-2.
-  Country sub-division code (ISO 3166-2): ``Optional`` (extended)
   Alpha-2 code of ISO 3166-2.
-  Entity Legal Form name Local name: Official name used within the
   country. If the country has different official languages, one may
   find several entries corresponding to the different languages.
-  Language: Common name of the language used to express the local name
   corresponding to the: "Name" (using Title case) of ISO 639-1.
-  Language Code (ISO 639-1): Alpha-2 code of ISO 639-1.
-  Entity Legal Form name Transliterated name (per ISO 01.140.10):
   Transliteration to *latinized* alphabet (more than ASCII - `Latin-1 section <#markdown-header-latin1>`__) of local
   name according to ISO 01.140.10.
-  Abbreviations Local language: ``Optional`` Abbreviations of the legal
   entity type local name.
-  Abbreviations transliterated: ``Optional`` Transliterated
   abbreviation of the legal entity type local name in *latinized*
   alphabet (more than ASCII).
-  Date created YYYY-MM-DD (ISO 8601): Date of creation according to ISO
   8601, per se, 2017-11-30 for the moment.
-  ELF Status ACTV/INAC: Either Active or Inactive.
-  Modification: ``Optional`` Explanation of the modification.
-  Modification date YYYY-MM-DD (ISO 8601): ``Optional`` Date of the
   modification according to ISO 8601.
-  Reason: ``Optional`` Explanation on the legal entity type.

Code examples
-------------

/!\\ Beware /!\\ Two datasets are available within this package. The
``Elf`` and the ``OriginalElf``, the original one (``OriginalElf``) is a
mapping of the file without some normalization in the data. This is the
pure form. Whereas ``Elf`` got some modifications to clean up some
inputs. See `Differences section <#markdown-header-differences>`__ for
more details.

There exists 220 elements sharing a same ELF code. You need to specify
which version you would like to use explicitly.

.. code:: python

    from iso20275 import ELF
    len(Elf['254M']) # 2 entries for this specific entity.
    Elf['254M'][0].local_name # '私人股份有限公司' for the Chinese entry.
    Elf['254M'][1].local_name # Private company limited by shares for the English entry.

    len(Elf['CDOV']) # 1 entry for this specific entity.
    Elf['CDOV'][0].local_name # International Business Corporation.

    # You can iterate over all the ELF code.
    for elf_code, values in Elf.items():
        pass

    # You can access to both version of the dataset, a normalized one and the original. Observe the Co-opLtd.
    Elf['6W6X'][0].local_abbreviations # "Co-operative Limited;Cooperative Limited;Co-op Limited;Coop Limited;Co-operative Ltd.;Cooperative Ltd.;Co-op Ltd.;Coop Ltd.;Co-operative;Cooperative;Co-op;Coop"
    Elf.load(newest=True, cleaned=False) # We load the official dataset
    Elf['6W6X'][0].local_abbreviations # "Co-operative Limited;Cooperative Limited;Co-op Limited;Coop Limited;Co-operative Ltd.;Cooperative Ltd.;Co-opLtd.;Coop Ltd.;Co-operative;Cooperative;Co-op;Coop"

Differences
-----------

Here, we will review which changes were made on the data or remarks were observed.

Original file (OriginalElf)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Differences in comparison to the original file.

Modification:
^^^^^^^^^^^^^

No modifcation were made on the file.

Since the last version published in 2017-11-30, the file format really improved and we don't find anymore heterogeneous content.

Modified file (Elf)
~~~~~~~~~~~~~~~~~~~

Differences in comparison to the original file.

Modification:
^^^^^^^^^^^^^

- ``’`` was replaced by ``'`` at the exception of the local name of JOZN.
- ``（`` was replaced by ``(`` and ``）`` by ``)`` in transliterated name (for chinese companies).
- Parenthesis have been normalized, one space before opening parenthesis and one after the closing one. This concerns essentially pakistanese companies: 	4XMS, 7IYW, 88OX, MOI8, QR25  and RKYF.
- Change in 6W6X: ``Co-opLtd.`` is now ``Co-op Ltd.``
- Change in CQ5X and UCU5: Replace ``Ε`` by ``E``.
- Change in J8DW: ``Podnik zahr. osoby, org. zložka`` is now ``Podnik zahr. osoby, org. zložka;Podnik zahr. osoby;org. zložka``.
- Change in L9WT: ``Obec, mesto (o.,m.úrad)`` is now ``Obec, mesto (o.,m.úrad);Obec;mesto;mesto (o.,m.úrad)``.

Latin1
------

The transliterated columns (namely Transliterated name and Abbreviations transliterated) are in a *latinized* alphabet (more than ASCII).

All the following characters are still present:

- ``œ`` U+0153 : LATIN SMALL LIGATURE OE
- ``Č`` U+010C : LATIN CAPITAL LETTER C WITH CARON
- ``č`` U+010D : LATIN SMALL LETTER C WITH CARON
- ``ě`` U+011B : LATIN SMALL LETTER E WITH CARON
- ``ľ`` U+013E : LATIN SMALL LETTER L WITH CARON
- ``ň`` U+0148 : LATIN SMALL LETTER N WITH CARON
- ``ř`` U+0159 : LATIN SMALL LETTER R WITH CARON
- ``Š`` U+0160 : LATIN CAPITAL LETTER S WITH CARON
- ``š`` U+0161 : LATIN SMALL LETTER S WITH CARON
- ``ť`` U+0165 : LATIN SMALL LETTER T WITH CARON
- ``Ž`` U+017D : LATIN CAPITAL LETTER Z WITH CARON
- ``ž`` U+017E : LATIN SMALL LETTER Z WITH CARON
- ``í`` U+00ED : LATIN SMALL LETTER I WITH ACUTE
- ``ý`` U+00FD : LATIN SMALL LETTER Y WITH ACUTE
- ``ć`` U+0107 : LATIN SMALL LETTER C WITH ACUTE
- ``ń`` U+0144 : LATIN SMALL LETTER N WITH ACUTE
- ``ś`` U+015B : LATIN SMALL LETTER S WITH ACUTE
- ``ă`` U+0103 : LATIN SMALL LETTER A WITH BREVE
- ``ů`` U+016F : LATIN SMALL LETTER U WITH RING ABOVE
- ``ő`` U+0151 : LATIN SMALL LETTER O WITH DOUBLE ACUTE
- ``ű`` U+0171 : LATIN SMALL LETTER U WITH DOUBLE ACUTE
- ``ö`` U+00F6 : LATIN SMALL LETTER O WITH DIAERESIS
- ``ü`` U+0075 : LATIN SMALL LETTER + U ``¨`` U+0308 : COMBINING DIAERESIS
- ``ā`` U+0101 : LATIN SMALL LETTER A WITH MACRON
- ``ī`` U+012B : LATIN SMALL LETTER I WITH MACRON
- ``ū`` U+016B : LATIN SMALL LETTER U WITH MACRON
- ``ċ`` U+010B : LATIN SMALL LETTER C WITH DOT ABOVE
- ``ė`` U+0117 : LATIN SMALL LETTER E WITH DOT ABOVE
- ``ż`` U+017C : LATIN SMALL LETTER Z WITH DOT ABOVE
- ``ą`` U+0105 : LATIN SMALL LETTER A WITH OGONEK
- ``ę`` U+0119 : LATIN SMALL LETTER E WITH OGONEK
- ``į`` U+012F : LATIN SMALL LETTER I WITH OGONEK
- ``ų`` U+0173 : LATIN SMALL LETTER U WITH OGONEK
- ``ł`` U+0142 : LATIN SMALL LETTER L WITH STROKE
- ``ș`` U+0219 : LATIN SMALL LETTER S WITH COMMA BELOW
- ``ț`` U+021B : LATIN SMALL LETTER T WITH COMMA BELOW
- ``ş`` U+015F : LATIN SMALL LETTER S WITH CEDILLA
- ``ţ`` U+0163 : LATIN SMALL LETTER T WITH CEDILLA
- ``у`` U+0443 : CYRILLIC SMALL LETTER U

One can found the following characters, in addition to the previously described, in the original:

- ``Ε`` U+0395 : GREEK CAPITAL LETTER EPSILON - Converted into ``E``.
- ``（`` U+FF08 : FULLWIDTH LEFT PARENTHESIS - Converted into ``(``.
- ``）`` U+FF09 : FULLWIDTH RIGHT PARENTHESIS - Converted into ``)``.

Written by `Youri Hubaut <https://github.com/Gawaboumga>`__ and `Petri Savolainen <https://github.com/petri>`__.
Distributed under MIT license.
