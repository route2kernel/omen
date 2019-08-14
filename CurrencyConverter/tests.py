from django.test import TestCase
from django.core.management.base import CommandError
from django.core.management import call_command
from django.utils.six import StringIO
from CurrencyConverter.models import Currency
from CurrencyConverter.modules.ConversionInterpreter import (Interpreter, InterpreterError)


class FetchTestCase(TestCase):
    def test_fetching(self):
        try:
            out = StringIO()
            call_command('fetch_exrates', stdout=out)
        except CommandError as e:
            self.fail("fetch_exrates test raised exception : {}".format(e))
        else:
            self.assertIn('Successfully', out.getvalue())


class InterpreterTestCase(TestCase):
    def setUp(self):
        if not Currency.objects.filter(name='TST'):
            c = Currency(name='TST', exchange_rate=1.123)
            c.save()

    def test_interpreter_valid_string(self):
        try:
            interpreter = Interpreter()
            query = "12.5 EUR en TST"
            result = interpreter.parse(query)
        except InterpreterError:
            self.fail("interpreter test raised an exception")
        else:
            expected_result = "12.5 EUR = {} TST".format(round(12.5 * 1.123, 2))
            self.assertEqual(result, expected_result)

    def test_interpreter_invalid_strings(self):
        try:
            interpreter = Interpreter()
        except InterpreterError:
            self.fail("interpreter test raised an exception")
        else:
            query = "42"
            with self.assertRaises(InterpreterError):
                interpreter.parse(query)

            query = "INVALID EUR en TST"
            with self.assertRaises(InterpreterError):
                interpreter.parse(query)

            query = "12.5 INVALID en TST"
            with self.assertRaises(InterpreterError):
                interpreter.parse(query)

            query = "12.5 EUR INVALID TST"
            with self.assertRaises(InterpreterError):
                interpreter.parse(query)

            query = "12.5 EUR en INVALID"
            with self.assertRaises(InterpreterError):
                interpreter.parse(query)


class ConversionTestCase(TestCase):
    def setUp(self):
        if not Currency.objects.filter(name='TST'):
            c = Currency(name='TST', exchange_rate=1.123)
            c.save()

    def test_accept_post_invalid_json(self):
        response = self.client.post('/money/convert/', data={"42"}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_accept_post_valid_json(self):
        response = self.client.post(
            '/money/convert/',
            content_type='application/json',
            data={"query": "12.5 EUR en TST"}
        )
        self.assertEqual(response.status_code, 200)
