import csv
import os


__version__ = 0, 0, 4
__all__ = 'Elf', 'OriginalElf',


class ElfEntry:
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

    @classmethod
    def labels(cls):
        return tuple((k for k, v in cls.__dict__.items() if isinstance(v, property)))

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


def read_from_csv(filename, sep=','):
    table = {}
    columns = ElfEntry.labels()
    with open(filename, 'r', encoding='utf-8') as csvfile:
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


original_codes = read_from_csv(os.path.join(os.path.dirname(__file__), 'ISO-20275 - 2019-11-06.csv'))
codes = read_from_csv(os.path.join(os.path.dirname(__file__), 'Cleaned - ISO-20275 - 2019-11-06.csv'))


class MetaA(type):
    def __getitem__(cls, key):
        return ElfEntries(codes[key])

    def __len__(cls):
        return len(codes)

    def items(cls):
        return codes.items()


class Elf(object, metaclass=MetaA):
    pass


class MetaB(type):
    def __getitem__(cls, key):
        return ElfEntries(original_codes[key])

    def __len__(cls):
        return len(original_codes)

    def items(cls):
        return original_codes.items()


class OriginalElf(object, metaclass=MetaB):
    pass
