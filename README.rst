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
   8601, per se, 2017-11-30, 2019-11-06 or 2020-06-10.
-  ELF Status ACTV/INAC: Either Active or Inactive.
-  Modification: ``Optional`` Explanation of the modification.
-  Modification date YYYY-MM-DD (ISO 8601): ``Optional`` Date of the
   modification according to ISO 8601.
-  Reason: ``Optional`` Explanation on the legal entity type.

Code examples
-------------

/!\\ Beware /!\\ Three datasets are available within this package. The
``Elf``, the ``Elf with additional legal forms`` and the ``Original Elf``, the original one (``Original Elf``) is a
mapping of the original file without some normalization in the data. This is the
pure form. Whereas ``Elf`` got some modifications to clean up some
inputs. See `Differences section <#markdown-header-differences>`__ for
more details. ``Elf with additional legal forms`` consists of the cleaned version (``Elf``) to which the different forms present in the file `Additional legal forms.txt <iso20275/Additional legal forms.txt>`__ have been added.

By default, the package provides ``Elf with additional legal forms``, but you can load the version that you want with:

``Elf.load(newest=True, cleaned=False, additional=False)``

If you don't provide *newest*,  you can access to a previous version with *timestamp* like 2019-11-06. *Cleaned* is when you want the version with some ameliorations, *additional* is based on the *cleaned* version but with the additional legal forms.

There exists 263 elements sharing a same ELF code. You need to specify
which version you would like to use explicitly.

.. code:: python

    from iso20275 import Elf
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

Original file (Original Elf)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
- `` `` (NO-BREAK SPACE 0xa0) was replaced by `` `` (space).
- Fusion of the two X0SD.
- Parenthesis have been normalized, one space before opening parenthesis and one after the closing one. This concerns essentially pakistanese companies: 	4XMS, 7IYW, 88OX, MOI8, QR25  and RKYF.
- Change in 6W6X: ``Co-opLtd.`` is now ``Co-op Ltd.``
- Change in 2DGO and EULU: Replace ``"""`` by ``"``
- Change in CQ5X and UCU5: Replace ``Ε`` by ``E`` (Greek letter by latin).
- Change in J8DW: ``Podnik zahr. osoby, org. zložka`` is now ``Podnik zahr. osoby, org. zložka;Podnik zahr. osoby;org. zložka``.
- Change in L9WT: ``Obec, mesto (o.,m.úrad)`` is now ``Obec, mesto (o.,m.úrad);Obec;mesto;mesto (o.,m.úrad)``.
- Change in X0SX: ``tksz,;hsz.`` is now ``tksz,;tksz.;hsz.``
- Change in HBQK: Addition of abbreviations: ``AIF - Sub scheme;AIF Scheme;AIF``.
- Change in JKJX and K361: Replace ``/`` with ``;``.
- Change in 3AZY, 3S6E, 4VD7, 6CHY, CVH6, D2I2, GLN8, IAP3, IQR2, JFET, R0B6, TUE5, YX4E, Z2FQ: Add CUMA, SDIS, PETR, SAS, SAFER, SIVOM, CIAS, SIVU, SICA, SPFPL SA à directoire, GIE, OPHLM, SCPI, GIP abbreviations respectively.
- Remove double spaces in EPG7, S2E3, DBU3, LBPW, ZJTK, JKJX, K361, DBU3, LBPW and B3JS.
- Change in FF1D: Addition of abbreviations ``PULC;UC``.
- Change in KMFX: Addition of abbreviations ``ULC;UC``.
- Change in URQH: Addition of abbreviations ``PUC;UC``.
- Change in Q9Y1: Addition of abbreviation ``IBC``.
- Change in X2X1: Addition of abbreviations ``LP;L.P.``.
- Change in 7ZMX: Addition of abbreviation ``AG``.
- Change in QFYC: Addition of abbreviation ``EIRL``.
- Change in P5JT and QNWW: Transliteration is now: ``Evropaïkós Ómilos Oikonomikoú Skopoú``.
- Trimming values, notably: ``Azerbaijani `` was replaced by ``Azerbaijani``.

Modified file with additional legal forms (Elf with additional legal forms)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Differences in comparison to the original file.

Modification:
^^^^^^^^^^^^^

The file is directly based on the modified file (Elf). We added the different forms present in the file `Additional legal forms.txt <iso20275/Additional legal forms.txt>`__ thanks to the script `merge_additional_legal_forms.py <iso20275/merge_additional_legal_forms.py>`__. This adds many countries, new legal forms in some countries already present, additions to the abbreviations used in some countries as well as legal forms in other languages.

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

Differences between the version 1.1 of 2019-11-06 and the 1.2 of 2020-06-10:

New countries:

- Azerbaijan
- Bahamas
- Belarus
- Belize
- Bermuda
- Bolivia
- Brazil
- Cambodia
- Cayman Islands
- Colombia
- Cook Islands
- Costa Rica
- Dominican Republic
- Ecuador
- Guatemala
- Honduras
- Japan
- Korea, the Republic of
- Lesotho
- Malaysia
- Marshall Islands
- Mexico
- Panama
- Papua New Guinea
- Paraguay
- Peru
- Puerto Rico
- Saudi Arabia
- Seychelles
- Sint Maarten
- Solomon Islands
- Tonga

Additions:

- Australia: 7TPC and ADXG.
- Austria: E9OX.
- Canada: 16GH, 16RL, 1VTA, 27WJ, 2ODA, 30IT, 3C5P, 3FP6, 4B4B, 50Z9, 52CK, 6ZCO, 702U, 87OW, 95EN, 9CB2, 9CEN, 9IF2, AS7L, CG81, D2T8, F9CT, GAMO, HVWR, I3UX, J5SC, JBU2, JIV4, JLE0, JLZW, JQNA, JVMD, JXO5, K08P, , L26C, L3XH, LN3N, MCY8, MK1I, MQT7, MR95, NVXN, OMUP, Q8NY, RC3D, RPGT, S72N, TA7J, TKAB, UVCG, V5IH, V9GU, VGP6, VRVJ, WGEA, XS49, XW5K, YMBJ, YIIS, ZGEX, ZQQU, ZX1F.
- Cyprus: 8VZ0.
- Finland: 6PEQ, R39F.
- Hong Kong: 2QMJ.
- India: JKJX, OYDA, W0G7.
- Italy: OQ8C.
- Liechtenstein: 53QF, TV8Y.
- Malta: DJ2D, F5X7, J4S1.
- Spain: 4SJR, 8EHB, TUHS.
- United Arab Emirates: MV4S, 4VPM, 6H9F, 9I58, 9U6F, B13W, FE4G, GU5E, H8MU, HECG, KAEM, LZ3H, OSE2, PNX6, R2YL, VKZD, 375P, 3P03, 46QC, 70EO, AIR0, F3UE, RWX4, V2PA, VTIP, 35BX, FHRL, GQ8F, HNPH, QJVN, Z3P8.
- United Kingdom: 4A3J, 55MA, 5FRT, 7VVZ, AVYY, IYXU, JTCO, NBTW, STX7.
- United States of America: CR3H, CWRI, HFGV, HN8W, V65U, WDT2, 9A4Q, BRO8, D4YS, K2BJ, M886, OVBT, TRS2, VXDE, 1K9U, EJX1, KGZ8, LD2M, M4FO, MJJZ, 5HQ4, 7CDL, BADE, CVXK, EI4J, G1P6, H1UM, K7YU, PZR6, SQ7B, 81WV, BC32, HLCG, I3Z9, L10T, M64D, OWR6, PDLV, WE9D, ZCHO, 7W53, JKOT, L7HH, LKQ2, SHCN, T80N, Y182, 3N55, 5DS0, 8N21, D155, TRI2, 6IIM, QD0H, QSC7, MFYJ, S7VR, 530K, EVE6, QLWR, RU6X, U9HL, UK9P, 1WZP, 8RLE, AZUK, F5VL, HSPI, VUXH, 32AX, 7XPF, DU35, HPKC, HUSW, L22N, VVPD, 8YBQ, NDBR, O4NK? U7GR, WPCN, XST3, 1ADA, 21OE, 7F5B, EMLK, KC7Z, R8SH, SUST, 1S9L, 30PQ, 30TX, 40SO, 5AE9, 5MRP, 7OS8, A770, HEMZ, KPH8, L1PM, MY98, OOX5, PNF3, QB0A, SCX8, T91C, WRF9, 62L3, 7K6U, 8WM4, IY8C, MM8M, SUEQ, 520I, 6M6O, 9M2Q, G66U, 0J9K, P3LZ, RCNI, S97G, 7HY7, FFBM, P7RH, T4M6, XSNP, 4YOA, 7GMS, VG3S, W0U4, 51RC, BO6L, PJ10, SDX0, XIZI, B8XC, BGH4, OJDX, PQXK, VJXH, 3JTE, 9C19, 9EJ6, B8KO, HSEV, 5E0K, 7RLC, AVLE, DRSE, FW66, MG8V, N263, QMI2, RZ5R, Z54A, ZHZP, 11GD, 7QV2, DBGD, G0HE, G6VI, N10D, PNSZ, WTWK, 15JS, C276, JZWN, UX5E, Z9CH, 7TJ1, 8MBD, DQUB, I2XB, QJ9F, RD1T, 9AAS, C5K7, FE1L, MXWB, WYG5, 1CZS, 2I4P, 3ZXC, 7H0X, B12O, GIN3, IDFN, NOBH, Q1N4, T0XH, UEKV, YQLO, 8XNO, GZMZ, K4MF, NYUD, OE6T, PNZI, R8O9, TCC0, UF6Y, F8DD, LBJ1, NHYA, RR8H, RRXD, DURX, IJHI, O9MN, OJBU, PXGA, QDZK, RC5L, 6S32, C0CR, EVBW, M5RM, WNV6, Z92A, ZXZ7, 1YA4, 71ZI, 9GXA, NB58, PUJR, QR4Y, RDQZ, A35I, JTJE, WMJ9, 6EH6, BST2, GLCI, JS65, N28C, Q62B, YOP9, ZHED, A30N, AN8Z, CHWX, DMNZ, MGUM, MH3L, NNLM, PKZ2, Q367, SOX5, TA9Z, UZ9W.

Deprecated:

- Belgium: 3LMA.
- Bonaire, Sint Eustatius and Saba: JFQ5.
- Bulgaria: 3HLJ, 45D7, 9F78, O15N.
- Denmark: 5QS7.
- France: LARO.
- Suriname: KJZ3.
- Switzerland: 2WFG, JB25, R9TC, UNA9.
- United Kingdom: 1W62, A2X8, C605, CDOT, FVGZ, HX6D, TYJK, UTY8, WBQU, WJ0A, ZZGG.

Differences between the version 1.2 of 2020-06-10 and the 1.3 of 2020-11-19:

New countries:

- Jordan

Additions:

- Argentina: F0A6, HZ6C, WUAZ.
- Canada: 8ZH8, 3Q15, translations of some legal forms.
- Germany: YJ4C.
- Mexico: 2RVP, 761Z, 8QZA, CU68, JRAQ, MAM6, TTIF, W9WS, XDGC.
- Russia: 9M15, MT3A.
- Spain: R6UT.

Deprecated:

- Puerto rico: All existing ELF codes for Puerto Rico replaced with new codes to solve situation with incorrect pairing of the same legal form in 2 languages.

For the following updates of the standard, a list of changes is written on the main site: https://www.gleif.org/en/about-lei/code-lists/iso-20275-entity-legal-forms-code-list/

Written by `Youri Hubaut <https://github.com/Gawaboumga>`__.
Distributed under MIT license.
