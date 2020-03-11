from Pre_pros import Pre_process
from Tokenizer import Tokenizer, Token


class Parser:

    tokens = ""
    resultado = 0

    @staticmethod
    def parseTerm():
        resultado_mult = Parser.parseFactor()
        Parser.tokens.select_next()

        while Parser.tokens.actual.value == "*" or Parser.tokens.actual.value == "/":
            if Parser.tokens.actual.value == "*":
                Parser.tokens.select_next()
                resultado_mult *= Parser.parseFactor()

            elif Parser.tokens.actual.value == "/":
                Parser.tokens.select_next()
                resultado_mult /= Parser.parseFactor()

            Parser.tokens.select_next()

        return resultado_mult

    @staticmethod
    def parseFactor():
        resultado_factor = 0

        if isinstance(Parser.tokens.actual.value, int):
            resultado_factor = Parser.tokens.actual.value
            return resultado_factor

        elif Parser.tokens.actual.value == "+":
            Parser.tokens.select_next()
            resultado_factor += Parser.parseFactor()
            return resultado_factor

        elif Parser.tokens.actual.value == "-":
            Parser.tokens.select_next()
            resultado_factor -= Parser.parseFactor()
            return resultado_factor

        elif Parser.tokens.actual.value == '(':
            Parser.tokens.select_next()
            resultado_factor = Parser.parseExpression()
            if Parser.tokens.actual.value == ')':
                return resultado_factor

            else:
                raise Exception("ERRO")

        else:
            raise Exception("ERRO")

    @staticmethod
    def parseExpression():
        Parser.resultado = Parser.parseTerm()

        while Parser.tokens.actual.value == "+" or Parser.tokens.actual.value == "-":
            if Parser.tokens.actual.value == "+":
                Parser.tokens.select_next()
                Parser.resultado += Parser.parseTerm()

            elif Parser.tokens.actual.value == "-":
                Parser.tokens.select_next()
                Parser.resultado -= Parser.parseTerm()

        return Parser.resultado

    @staticmethod
    def run(code):

        code = Pre_process.filter(code)
        Parser.tokens = Tokenizer(code)
        resultado = Parser.parseExpression()

        if Parser.tokens.actual.value != 'EOF':
            raise Exception("ERRO")

        return int(resultado)
