from unittest import TestCase
from webservices.server import compile_program


class TestCompile_program(TestCase):
    msg = {'message': ["2. Program wykonano poprawnie z wynikiem:\naaa\n"]}
    exception_result = 'aaa\n'

    def test_compile_program(self):
        result = compile_program("print ('aaa')")
        self.assertEqual(result,(self.msg,self.exception_result))
        result = compile_program("println('aaa')")
        self.assertNotEqual(result,(self.msg,self.exception_result))
