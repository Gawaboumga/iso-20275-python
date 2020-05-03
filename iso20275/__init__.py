import csv
import os
import re
import pathlib
import collections

__version__ = 0, 0, 7
__all__ = 'Elf',


class OrderedProperties(type):
    "metaclass for custom ordered properties access on Python 3.5 and earlier"

    @classmethod
    def __prepare__(mcs, name, bases):
        "provide order-keeping support"
        return collections.OrderedDict()

    def __new__(cls, name, bases, classdict):
        "inject a custom __properties__ magic method"
        customclass = type.__new__(cls, name, bases, classdict)
        customclass.__properties__ = tuple(k for k,v in classdict.items() if isinstance(v, property))
        return customclass


class ElfEntry(metaclass=OrderedProperties):
    def __init__(self, data):
        self.__data = data

    @property
    def elf(self):
        return self._ElfEntry__data['elf']

    @property
    def country(self):
        return self._ElfEntry__data['country']

    @property
    def alpha2(self):
        return self._ElfEntry__data['alpha2']

    @property
    def jurisdiction(self):
        return self._ElfEntry__data['jurisdiction']

    @property
    def alpha2_2(self):
        return self._ElfEntry__data['alpha2_2']

    @property
    def local_name(self):
        return self._ElfEntry__data['local_name']

    @property
    def language(self):
        return self._ElfEntry__data['language']

    @property
    def language_code(self):
        return self._ElfEntry__data['language_code']

    @property
    def transliterated_name(self):
        return self._ElfEntry__data['transliterated_name']

    @property
    def local_abbreviations(self):
        return self._ElfEntry__data['local_abbreviations']

    @property
    def transliterated_abbreviations(self):
        return self._ElfEntry__data['transliterated_abbreviations']

    @property
    def creation_date(self):
        return self._ElfEntry__data['creation_date']

    @property
    def status(self):
        return self._ElfEntry__data['status']

    @property
    def modification(self):
        return self._ElfEntry__data['modification']

    @property
    def modification_date(self):
        return self._ElfEntry__data['modification_date']

    @property
    def reason(self):
        return self._ElfEntry__data['reason']


    def __str__(self):
        return self.elf + ': ' + self.local_name

    def __repr__(self):
        cls = type(self)
        return '<%s.Elf.%s %r>' % (
            cls.__module__, self.elf,
            self.local_name
        )


class ElfEntries:
    def __init__(self, line):
        self.__line = line

    def __getitem__(self, key):
        return self.__line[key]

    def __len__(self):
        return len(self.__line)

    def __iter__(self):
        return self


def read_from_csv(filepath:pathlib.Path, sep=','):
    "read CSV file at a given path"
    table = {}
    columns = ElfEntry.__properties__
    with filepath.open('r', encoding='utf-8') as csvfile:
        next(csvfile)
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"', strict=True)
        for tokens in spamreader:
            row = dict(zip(columns, tokens))
            code = row["elf"]
            if code in table:
                table[code].append(ElfEntry(row))
            else:
                table[code] = [ElfEntry(row)]
    return table


rgx = re.compile(r"(?i)^(?P<c>Cleaned)?[ -_]*ISO-20275[ -_]*(?P<t>\d{4}-\d{2}-\d{2})\.csv$")

def get_csv_paths(newest=None, cleaned=None, timestamp=None):
    """get provided csv file paths, optionally just newest and/or
    cleaned only and/or ones with given timestamp"""

    csvpaths = pathlib.Path(__file__).resolve().parent.glob('*.csv')
    tested = ((re.match(rgx, csvpath.name), csvpath) for csvpath in csvpaths)
    results = ((m.group("c"), m.group("t"), csvpath) for m, csvpath in tested if m)

    if cleaned is True:
       results = (r for r in results if r[0])
    elif cleaned is False:
       results = (r for r in results if not r[0])
    if timestamp:
       results = (r for r in results if r[1] == timestamp)
    if newest:
       results = sorted(results, key=lambda r: r[1], reverse=True)
       results = (results[0],) if cleaned else results[:2]

    return tuple((r[-1] for r in results))


class MetaElf(type):

    def __new__(cls, name, bases, clsdct):
        elfclass = type.__new__(cls, name, bases, clsdct)

        # by default, the latest cleaned CSV source is used
        elfclass._codes = read_from_csv(get_csv_paths(newest=True, cleaned=True)[0])
        return elfclass

    def __getitem__(cls, key):
        return ElfEntries(cls._codes[key])

    def __len__(cls):
        return len(cls._codes)

    def __iter__ (self):
        return self


class Elf(object, metaclass=MetaElf):

    @classmethod
    def load(cls, newest=None, cleaned=None, timestamp=None, csvpath:pathlib.Path=None):
        "load a particular CSV source (newest/cleaned/timestamp) or a custom file"
        pth = csvpath or get_csv_paths(newest=newest, cleaned=cleaned, timestamp=timestamp)[0]
        cls._codes = read_from_csv(pth)

    @classmethod
    def items(cls):
        return cls._codes.items()