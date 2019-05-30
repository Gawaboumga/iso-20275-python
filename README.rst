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
20275:2017 <https://www.iso.org/obp/ui/#iso:std:iso:20275:ed-1:v1:en>`__

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
   Transliteration to *latinized* alphabet (more than ASCII) of local
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

    len(Elf['254M']) # 2 entries for this specific entity.
    Elf['254M'][0].local_name # Private company limited by shares for the English entry.
    Elf['254M'][1].local_name # '私人股份有限公司' for the Chinese entry.

    len(Elf['CDOV']) # 1 entry for this specific entity.
    Elf['CDOV'][0].local_name # International Business Corporation.

    # You can iterate over all the ELF code.
    for elf_code, values in Elf.items():
        pass

    # You can access to both version of the dataset, a normalized one and the original.
    Elf['358I'][0].local_abbreviations # "corp.;inc.;co.;ltd. Incorporated;company;limited;corporation"
    OriginalElf['358I'][0].local_abbreviations # "corp., inc., co., ltd. Incorporated, company, limited, corporation, or no abbreviation"

Differences
-----------

Here, we will review which changes were made on the data or remarks were
observed.

Original file (OriginalElf)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Differences in comparison to the original file.

Modification:
^^^^^^^^^^^^^

-  ``n/a``, ``N/A``, ``""`` were converted to NA.

Remark:
^^^^^^^

-  (Opening) parenthesis are sometimes preceeded (or followed) by a
   space, sometimes not. Same with the closing ones.
-  Not trimmed data.
-  Some entries have symbol: ``“`` or ``”``.
-  Some entries have: ``&amp;``.

Modified file (Elf)
~~~~~~~~~~~~~~~~~~~

Differences in comparison to the original file.

Modification:
^^^^^^^^^^^^^

-  ``n/a``, ``N/A``, ``""``, ``no abbreviation`` were converted to NA.
-  Parenthesis have been normalized, one space before opening
   parenthesis and one after the closing one.
-  Data haves been trimmed.
-  Symbols ``“`` or ``”`` have been removed.
-  ``&amp;`` were replaced by ``&``.
-  ``and`` and ``or`` were replaced by ``;`` in abbreviations.
-  Commas ``,`` have been replaced by ``;`` in abbreviations.

Rows: 266, 269, 270, 271, 273, 274, 275, 276, 277, 278, 307, 310, 311,
312, 313, 315, 318, 322, 324, 1133 and 1743 have been modified to avoid
comments within abbreviations columns. See
`Difference.txt <Difference.txt>`__ for further information.

Written by `Youri Hubaut <https://github.com/Gawaboumga>`__.
Distributed under MIT license.
