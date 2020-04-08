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
        self.reserved_words = ["echo"]

    def select_next(self):

        if self.origin[self.position] == " " or self.origin[self.position] == "\n":
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

        elif self.origin[self.position] == "{":
            self.actual = Token("{", "B_OPEN")
            self.position += 1

        elif self.origin[self.position] == "}":
            self.actual = Token("}", "B_CLOSE")
            self.position += 1

        elif self.origin[self.position] == "=":
            self.actual = Token("=", "ASSIGN")
            self.position += 1

        elif self.origin[self.position] == ";":
            self.actual = Token(";", "ENDL")
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

        elif self.origin[self.position].isalpha():
            alpha = ""
            while(self.origin[self.position].isalpha()):
                alpha += self.origin[self.position]

                if (self.position < len(self.origin) - 1):
                    self.position += 1
                else:
                    break

            self.actual = Token(alpha, "COMMAND")
        
        elif self.origin[self.position] == "$":
            var_name = ""
            self.position += 1

            if(self.origin[self.position].isalpha()):
                var_name += self.origin[self.position]
                self.position += 1

                while(self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == "_"):
                    var_name += self.origin[self.position]

                    if (self.position < len(self.origin) - 1):
                        self.position += 1
                    else:
                        break

                if var_name.lower() not in self.reserved_words:
                    self.actual = Token("$" + var_name, "VARIABLE")
                else:
                    raise Exception("Invalid variable name")

            else:
                raise Exception("Invalid variable name")

        else:
            self.actual = Token("EOF", "EOF")
