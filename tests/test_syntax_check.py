from unittest import TestCase
from webservices.server import syntax_check


class TestSyntax_check(TestCase):
    program_codes_correct = (("print('aaa')", "{'message': ['1. Poprawna skladnia']}"),
                             ("print('aaa')////", "{'message': ['1. Niepoprawna skladnia']}"))

    def test_syntax_check(self):
        result = syntax_check("print('aaa')")
        self.assertEqual(str("{'message': ['1. Poprawna skladnia']}"), str(result))
