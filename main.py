import sys
import re
from Parser import Parser
from SymbolTable import *
from Assembly import *

if __name__ == "__main__":

    eq = sys.argv[1]
    
    if(".php" in eq):
        f = open(eq)
        code = f.read()
        resultado = Parser.run(code)
        st = SymbolTable()
        resultado = resultado.Evaluate(st)
        Assembly.CreateFile("code.asm")
    else:
        raise Exception("ERRO")
    

