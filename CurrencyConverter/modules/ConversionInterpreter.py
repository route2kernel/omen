from ply import (yacc, lex)
from django.conf import settings
from CurrencyConverter.models import Currency
if not settings.configured:
    settings.configure(DEBUG=True)


class InterpreterError(Exception):
    pass


class Lexer():
    tokens = (
        'AMOUNT', 'LINKWORD', 'ORIGINALCURR', 'CONVERTCURR'
    )

    t_LINKWORD = r'en'
    t_ORIGINALCURR = r'EUR'
    t_ignore = r" "

    def t_AMOUNT(self, t):
        r'[0-9]*\.?[0-9]{1,2}'
        t.value = float(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise lex.LexError("lex error caught", "")

    def __init__(self):
        currencies_name = list(Currency.objects.all().values_list('name', flat=True))
        self.t_CONVERTCURR = r"|".join(currencies_name)
        self.lexer = lex.lex(module=self)


class Interpreter():
    tokens = Lexer.tokens

    def p_conversion(self, t):
        'conversion : AMOUNT ORIGINALCURR LINKWORD CONVERTCURR'
        amount = t[1]
        originalcurr = t[2]
        convertcurr = t[4]
        try:
            exchange_rate = float(Currency.objects.get(name=convertcurr).exchange_rate)
        except Currency.DoesNotExist:
            raise yacc.YaccError
        converted_amount = round(amount * exchange_rate, 2)
        t[0] = "{} {} = {} {}".format(amount, originalcurr, converted_amount, convertcurr)

    def p_error(self, t):
        raise yacc.YaccError("yacc error caught")

    def parse(self, query):
        try:
            result = self.parser.parse(query)
        except (lex.LexError, yacc.YaccError):
            raise InterpreterError
        else:
            return result

    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
