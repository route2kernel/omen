from rest_framework.decorators import api_view
from rest_framework.response import Response
from CurrencyConverter.modules.ConversionInterpreter import (Interpreter, InterpreterError)


@api_view(['POST'])
def Conversion(request):
    fail_msg = "I'm sorry Dave, i'm afraid i can't do that"
    try:
        query = request.data['query']
    except (KeyError, TypeError):
        return Response({"answer": fail_msg}, status=500)

    try:
        interpreter = Interpreter()
        result = interpreter.parse(query)
    except InterpreterError:
        return Response({"answer": fail_msg}, status=500)
    else:
        return Response({"answer": result}, status=200)
