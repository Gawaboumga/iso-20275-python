import csv
import re
from pathlib import Path
from collections import OrderedDict
from collections.abc import Iterable
from typing import Sequence, Union
from functools import singledispatch


__version__ = 0, 0, 8
__all__ = 'Elf',


class OrderedProperties(type):
    "metaclass for custom ordered properties access on Python 3.5 and earlier"

    @classmethod
    def __prepare__(mcs, name, bases):
        "provide order-keeping support"
        return OrderedDict()

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


@singledispatch
def read_entries(source:Iterable):
    "produce list of ElfEntry items from a source, by default an iterator"
    table = {}
    columns = ElfEntry.__properties__

    for tokens in source:
        row = dict(zip(columns, tokens))
        entry = ElfEntry(row)
        if entry.elf in table:
            table[entry.elf].append(entry)
        else:
            table[entry.elf] = [entry]
    return table


@read_entries.register(Path)
def read_entries_from_csvpath(source:Path):
    "produce list of ElfEntry items from a filesystem Path pointing to a CSV file"
    with source.open('r', encoding='utf-8') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', strict=True)
        entries = read_entries(reader)
    return entries


rgx = re.compile(r"(?i)^(?P<c>Cleaned)?[ -_]*ISO-20275[ -_]*(?P<t>\d{4}-\d{2}-\d{2})\.csv$")

def get_csv_paths(newest=None, cleaned=None, timestamp=None) -> Sequence[Path]:
    """get provided csv file paths, optionally just newest and/or
    cleaned only and/or ones with given timestamp"""

    csvpaths = Path(__file__).resolve().parent.glob('*.csv')
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
        elfclass._codes = read_entries(get_csv_paths(newest=True, cleaned=True)[0])
        return elfclass

    def __getitem__(cls, key):
        return ElfEntries(cls._codes[key])

    def __len__(cls):
        return len(cls._codes)

    def __iter__ (self):
        return self


class Elf(object, metaclass=MetaElf):

    @classmethod
    def load(cls, newest=None, cleaned=None, timestamp=None, source:Union[Iterable,Path]=None):
        "load a particular CSV source (newest/cleaned/timestamp) or a custom file"
        if source is None:
            source = get_csv_paths(newest=newest, cleaned=cleaned, timestamp=timestamp)[0]
        cls._codes = read_entries(source)

    @classmethod
    def items(cls):
        return cls._codes.items()