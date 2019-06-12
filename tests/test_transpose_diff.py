import difflib
from unittest import TestCase
from webservices.server import transpose_diff

class TestTranspose_diff(TestCase):
    def test_transpose_diff(self):
        string1 = "aaa"
        string2 = "aaa"

        differ = difflib.Differ()
        diff = differ.compare(string1, string2)
        all_lines = transpose_diff(diff)
        assert all_lines is not None

        string1 = ""
        string2 = ""

        differ = difflib.Differ()
        diff = differ.compare(string1, string2)
        all_lines = transpose_diff(diff)
        assert all_lines == "\n\n"
