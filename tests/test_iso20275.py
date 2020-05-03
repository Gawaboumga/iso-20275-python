from iso20275 import Elf
import unittest


class TestElf(unittest.TestCase):

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
