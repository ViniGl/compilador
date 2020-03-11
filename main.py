import sys
import re
from Parser import Parser


if __name__ == "__main__":

    eq = sys.argv[1]
    resultado = Parser.run(eq)
    # resultado = Parser.run('(2+2)/2')

    print(resultado)
