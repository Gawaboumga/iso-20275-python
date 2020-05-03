from iso20275 import Elf, get_csv_paths
import unittest
import csv


class TestElf(unittest.TestCase):

    def setUp(self):
        Elf.load(newest=True, cleaned=True)

    def test_dispatched_readers_work_same(self):
        "make sure single-dispatched implementation works"

        # items from default reading
        items1 = Elf.items()

        # construct & use a reader & get items from it
        path = get_csv_paths(newest=True, cleaned=True)[0]
        with path.open('r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"', strict=True)
            next(reader)
            Elf.load(source=reader)
        items2 = Elf.items()

        # check results are same
        i1 = dict(items1)
        i2 = dict(items2)
        self.assertEqual(i1.keys(), i2.keys())
        for code in i1:
            names1 = [e.local_name for e in i1[code]]
            names2 = [e.local_name for e in i2[code]]
            self.assertEqual(names1, names2)

    def test_member_name_must_be_equal_to_elf_code(self):
        for elf, values in Elf.items():
            for value in values:
                self.assertEqual(elf, getattr(value, 'elf'))

    def test_number_of_elf(self):
        self.assertEqual(len(Elf), 2082)

    def test_254M_multiple_values(self):
        self.assertEqual(len(Elf['254M']), 2)

        self.assertEqual(Elf['254M'][0].local_name, '私人股份有限公司')
        self.assertEqual(Elf['254M'][0].alpha2, 'HK')
        self.assertEqual(Elf['254M'][0].transliterated_name, 'Si ren gu fen you xian gong si')

        self.assertEqual(Elf['254M'][1].local_name, 'Private company limited by shares')
        self.assertEqual(Elf['254M'][1].alpha2, 'HK')
        self.assertEqual(Elf['254M'][1].transliterated_name, 'Private company limited by shares')

    def test_str(self):
        self.assertEqual(str(Elf['254M'][0]), '254M: 私人股份有限公司')
        self.assertEqual(str(Elf['254M'][0].local_name), '私人股份有限公司')

    def test_repr(self):
        self.assertEqual(repr(Elf['254M'][0]), "<iso20275.Elf.254M '私人股份有限公司'>")
        self.assertEqual(repr(Elf['J4JC'][0]), "<iso20275.Elf.J4JC 'Limited Partnership'>")

    def test_difference_cleaned_and_original(self):
        self.assertEqual(Elf['6W6X'][0].local_abbreviations, 'Co-operative Limited;Cooperative Limited;Co-op Limited;Coop Limited;Co-operative Ltd.;Cooperative Ltd.;Co-op Ltd.;Coop Ltd.;Co-operative;Cooperative;Co-op;Coop')
        Elf.load(newest=True, cleaned=False)
        self.assertEqual(Elf['6W6X'][0].local_abbreviations, 'Co-operative Limited;Cooperative Limited;Co-op Limited;Coop Limited;Co-operative Ltd.;Cooperative Ltd.;Co-opLtd.;Coop Ltd.;Co-operative;Cooperative;Co-op;Coop')

    def test_correct_csv_parsing(self):
        self.assertEqual(Elf['C7TI'][0].local_name, 'Ассоциации (союзы) садоводческих, огороднических и дачных некоммерческих объединений')
        self.assertEqual(Elf['C7TI'][0].transliterated_name, 'Assotsiatsii (soyuzy) sadovodcheskikh, ogorodnicheskikh i dachnykh nekommercheskikh ob"yedineniy')


if __name__ == '__main__':
    unittest.main()
