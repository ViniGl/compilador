import sys
import re
from Parser import Parser


if __name__ == "__main__":

    eq = sys.argv[1]
    
    if(".php" in eq):
        f = open(eq)
        code = "".join([x.strip() for x in f.readlines()]) 
        resultado = Parser.run(code)
        resultado = resultado.Evaluate()
        print(resultado)
    else:
        raise Exception("ERRO")
    

