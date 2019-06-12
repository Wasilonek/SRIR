from unittest import TestCase
from webservices.server import check_difference
from webservices.models import Result


class TestCheck_difference(TestCase):
    prog1 = Result(program_result='aaa',
                    program_code="print('aaa')")
    prog2 = Result(program_result='bbb',
                    program_code="print('bbb')")
    programs = (prog1,
                prog2)
    code = "print('aaa')"
    reslut = ({'message': ['3. Porownanie z poprzednimi programami:',
             'Diff Program: None',
             "print('aaa')\n            \n",
             'Diff Program: None',
             "print('bbbaaa')\n       ---+++  \n"]})
    def test_check_difference(self):
        result = check_difference(self.programs, self.code)
        self.assertEqual(result, self.reslut)