class Token:

    def __init__(self, value=None, token_type=None):
        self.value = value
        self.token_type = token_type


class Tokenizer:

    def __init__(self, origin, position=0):
        self.origin = origin + "EOF"
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

        elif self.origin[self.position] == "(":
            self.actual = Token("(", "OPEN")
            self.position += 1

        elif self.origin[self.position] == ")":
            self.actual = Token(")", "CLOSE")
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

