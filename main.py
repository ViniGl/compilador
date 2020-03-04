import sys


class Token:

    def __init__(self, value=None, token_type=None):
        self.value = value
        self.token_type = token_type


class Tokenizer:

    def __init__(self, origin, position=0):
        origin.append("EOF")
        self.origin = " ".join(origin)
        self.position = position
        self.actual = Token(None, None)
        self.select_next()

    def select_next(self):

        if self.origin[self.position] == " ":
            self.position += 1
            self.select_next()

        elif self.origin[self.position] == "+":
            self.actual = Token("+", "PLUS")
            self.position += 1
        
        elif self.origin[self.position] == "-":
            self.actual = Token("-", "MINUS")
            self.position += 1

        elif self.origin[self.position] == "*":
            self.actual = Token("*", "MULT")
            self.position += 1

        elif self.origin[self.position] == "/":
            self.actual = Token("/", "DIV")
            self.position += 1
        
        elif self.origin[self.position].isdigit():
            number = ""
            while(self.origin[self.position].isdigit()):
                number += self.origin[self.position]

                if (self.position < len(self.origin) - 1):
                    self.position += 1
                else:
                    break

            self.actual = Token(int(number), "NUMBER")
        else:
            self.actual = Token("EOF", "EOF")



class Parser:

    tokens = ""

    @staticmethod
    def parseExpression():
        resultado = 0
        if isinstance(Parser.tokens.actual.value, int):
            resultado += int(Parser.tokens.actual.value)
            Parser.tokens.select_next()

            while Parser.tokens.actual.value == "+" or Parser.tokens.actual.value == "-" or Parser.tokens.actual.value == "*" or Parser.tokens.actual.value == "/":
                if Parser.tokens.actual.value == "+":
                    Parser.tokens.select_next()
                    if (isinstance(int(Parser.tokens.actual.value), int)):
                        resultado += int(Parser.tokens.actual.value)
                    else:
                        raise Exception("ERRO")
                elif Parser.tokens.actual.value == "-":
                    Parser.tokens.select_next()
                    if (isinstance(int(Parser.tokens.actual.value), int)):
                        resultado -= int(Parser.tokens.actual.value)
                    else:
                        raise Exception("ERRO")

                elif Parser.tokens.actual.value == "*":
                    Parser.tokens.select_next()
                    if (isinstance(int(Parser.tokens.actual.value), int)):
                        resultado *= int(Parser.tokens.actual.value)
                    else:
                        raise Exception("ERRO")

                elif Parser.tokens.actual.value == "/":
                    Parser.tokens.select_next()
                    if (isinstance(int(Parser.tokens.actual.value), int)):
                        resultado /= int(Parser.tokens.actual.value)
                    else:
                        raise Exception("ERRO")

                Parser.tokens.select_next()

            return resultado
        else:
            raise Exception("ERRO")

    @staticmethod
    def run(code):

        Parser.tokens = Tokenizer(code)
        resultado = Parser.parseExpression()

        if Parser.tokens.actual.value != 'EOF':
            return "EOF"

        return resultado


if __name__ == "__main__":

    # eq = "".join(sys.argv[1:])
    # print(eq)
    eq = sys.argv[1:]
    resultado = Parser.run(eq)
    

    print(resultado)
