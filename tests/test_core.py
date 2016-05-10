import unittest

from sox import core
from sox.core import SoxError
from sox.core import SoxiError

INPUT_FILE = 'data/input.wav'
INPUT_FILE_INVALID = 'data/input.xyz'
INPUT_FILE_CORRUPT = 'data/empty.aiff'
OUTPUT_FILE = 'data/output.wav'


class TestSox(unittest.TestCase):

    def test_base_case(self):
        args = ['sox', INPUT_FILE, OUTPUT_FILE]
        expected = True
        actual = core.sox(args)
        self.assertEqual(expected, actual)

    def test_base_case2(self):
        args = [INPUT_FILE, OUTPUT_FILE]
        expected = True
        actual = core.sox(args)
        self.assertEqual(expected, actual)

    def test_sox_fail_bad_args(self):
        args = ['-asdf']
        expected = False
        actual = core.sox(args)
        self.assertEqual(expected, actual)

    def test_sox_fail_bad_files(self):
        args = ['asdf.wav', 'flululu.wav']
        expected = False
        actual = core.sox(args)
        self.assertEqual(expected, actual)

    def test_sox_fail_bad_ext(self):
        args = ['input.wav', 'output.xyz']
        expected = False
        actual = core.sox(args)
        self.assertEqual(expected, actual)

    def test_sox_fail_corrupt_file(self):
        args = [INPUT_FILE_CORRUPT, OUTPUT_FILE]
        expected = False
        actual = core.sox(args)
        self.assertEqual(expected, actual)


class TestGetValidFormats(unittest.TestCase):

    def setUp(self):
        self.formats = core._get_valid_formats()

    def test_wav(self):
        self.assertIn('wav', self.formats)

    def test_aiff(self):
        self.assertIn('aiff', self.formats)

    def test_notin(self):
        self.assertNotIn('AUDIO', self.formats)
        self.assertNotIn('FILE', self.formats)
        self.assertNotIn('FORMATS', self.formats)
        self.assertNotIn('AUDIO FILE FORMATS', self.formats)


class TestValidFormats(unittest.TestCase):

    def test_wav(self):
        self.assertIn('wav', core.VALID_FORMATS)

    def test_aiff(self):
        self.assertIn('aiff', core.VALID_FORMATS)

    def test_notin(self):
        self.assertNotIn('AUDIO', core.VALID_FORMATS)
        self.assertNotIn('FILE', core.VALID_FORMATS)
        self.assertNotIn('FORMATS', core.VALID_FORMATS)
        self.assertNotIn('AUDIO FILE FORMATS', core.VALID_FORMATS)


class TestSoxi(unittest.TestCase):

    def test_base_case(self):
        actual = core.soxi(INPUT_FILE, 's')
        expected = '441000'
        self.assertEqual(expected, actual)

    def test_invalid_argument(self):
        with self.assertRaises(ValueError):
            core.soxi(INPUT_FILE, None)

    def test_nonexistent_file(self):
        with self.assertRaises(SoxiError):
            core.soxi('data/asdf.wav', 's')

    def test_invalid_filetype(self):
        with self.assertRaises(SoxiError):
            core.soxi(INPUT_FILE_INVALID, 's')

    def test_soxi_error(self):
        with self.assertRaises(SoxiError):
            core.soxi(INPUT_FILE_CORRUPT, 's')


class TestIsNumber(unittest.TestCase):

    def test_numeric(self):
        actual = core.is_number(0)
        expected = True
        self.assertEqual(expected, actual)

    def test_numeric2(self):
        actual = core.is_number(1.213215)
        expected = True
        self.assertEqual(expected, actual)

    def test_numeric3(self):
        actual = core.is_number(-100)
        expected = True
        self.assertEqual(expected, actual)

    def test_numeric4(self):
        actual = core.is_number('13.54')
        expected = True
        self.assertEqual(expected, actual)

    def test_nonnumeric(self):
        actual = core.is_number('a')
        expected = False
        self.assertEqual(expected, actual)

    def test_nonnumeric2(self):
        actual = core.is_number('-f')
        expected = False
        self.assertEqual(expected, actual)

    def test_nonnumeric3(self):
        actual = core.is_number([1])
        expected = False
        self.assertEqual(expected, actual)


class TestAllEqual(unittest.TestCase):

    def test_true(self):
        actual = core.all_equal([2, 2, 2, 2, 2])
        expected = True
        self.assertEqual(expected, actual)

    def test_true2(self):
        actual = core.all_equal(['a'])
        expected = True
        self.assertEqual(expected, actual)

    def test_true3(self):
        actual = core.all_equal([])
        expected = True
        self.assertEqual(expected, actual)

    def test_false(self):
        actual = core.all_equal([1, 2, 1, 2])
        expected = False
        self.assertEqual(expected, actual)

    def test_false2(self):
        actual = core.all_equal([1, 1, '1', 1])
        expected = False
        self.assertEqual(expected, actual)

    def test_false3(self):
        actual = core.all_equal(['ab', 'a', 'b'])
        expected = False
        self.assertEqual(expected, actual)