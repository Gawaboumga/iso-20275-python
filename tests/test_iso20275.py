from iso20275 import Elf, OriginalElf
import unittest


class TestElf(unittest.TestCase):

    def test_member_name_must_be_equal_to_elf_code(self):
        for elf, values in Elf.items():
            for value in values:
                self.assertEqual(elf, getattr(value, 'elf'))

    def test_number_of_elf(self):
        self.assertEqual(len(Elf), 1600)

    def test_254M_multiple_values(self):
        self.assertEqual(len(Elf['254M']), 2)

        self.assertEqual(Elf['254M'][0].local_name, 'Private company limited by shares')
        self.assertEqual(Elf['254M'][0].alpha2, 'HK')
        self.assertEqual(Elf['254M'][0].transliterated_name, 'Private company limited by shares')

        self.assertEqual(Elf['254M'][1].local_name, '私人股份有限公司')
        self.assertEqual(Elf['254M'][1].alpha2, 'HK')
        self.assertEqual(Elf['254M'][1].transliterated_name, 'Si ren gu fen you xian gong si')

    def test_str(self):
        self.assertEqual(str(Elf['254M'][1]), '254M: 私人股份有限公司')
        self.assertEqual(str(Elf['254M'][1].local_name), '私人股份有限公司')

    def test_repr(self):
        self.assertEqual(repr(Elf['254M'][1]), "<iso20275.Elf.254M '私人股份有限公司'>")
        self.assertEqual(repr(Elf['J4JC'][0]), "<iso20275.Elf.J4JC 'Limited Partnership'>")

    def test_difference_cleaned_and_original(self):
        self.assertEqual(Elf['358I'][0].local_abbreviations, "corp.;inc.;co.;ltd. Incorporated;company;limited;corporation")
        self.assertEqual(OriginalElf['358I'][0].local_abbreviations, "corp., inc., co., ltd. Incorporated, company, limited, corporation, or no abbreviation")


if __name__ == '__main__':
    unittest.main()
