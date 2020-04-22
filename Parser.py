from Pre_pros import Pre_process
from Tokenizer import Tokenizer, Token
from Node import *
import sys


class Parser:

    tokens = ""

    @staticmethod
    def parseTerm():
        resultado_mult = Parser.parseFactor()
        Parser.tokens.select_next()

        while Parser.tokens.actual.value == "*" or Parser.tokens.actual.value == "/":
            if Parser.tokens.actual.value == "*":
                node = BinOp("*", [])
                node.children.append(resultado_mult)
                Parser.tokens.select_next()
                node.children.append(Parser.parseFactor())

            elif Parser.tokens.actual.value == "/":
                node = BinOp("/", [])
                node.children.append(resultado_mult)
                Parser.tokens.select_next()
                node.children.append(Parser.parseFactor())

            resultado_mult = node

            Parser.tokens.select_next()

        return resultado_mult

    @staticmethod
    def parseFactor():
        resultado_factor = 0

        if isinstance(Parser.tokens.actual.value, int):
            resultado_factor = Parser.tokens.actual.value
            node = IntVal(resultado_factor)
            return node

        elif Parser.tokens.actual.value == "+":
            node = UnaryOp("+", [])
            Parser.tokens.select_next()
            node.children.append(Parser.parseFactor())
            return node

        elif Parser.tokens.actual.value == "-":
            node = UnaryOp("-", [])
            Parser.tokens.select_next()
            node.children.append(Parser.parseFactor())
            return node

        elif Parser.tokens.actual.value == '(':
            Parser.tokens.select_next()
            resultado_factor = Parser.parseExpression()
            if Parser.tokens.actual.value == ')':
                return resultado_factor

            else:
                raise Exception("ERRO")
        
        elif "$" in Parser.tokens.actual.value:
            return VarName(Parser.tokens.actual.value)

        else:
            raise Exception("ERRO")

    @staticmethod
    def parseExpression():
        Parser.resultado = Parser.parseTerm()

        while Parser.tokens.actual.value == "+" or Parser.tokens.actual.value == "-":
            if Parser.tokens.actual.value == "+":
                node = BinOp("+", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseTerm())

            elif Parser.tokens.actual.value == "-":
                node = BinOp("-", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseTerm())

            Parser.resultado = node

        return Parser.resultado
    
    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.value == "{":
            Parser.tokens.select_next()
            commands = Commands("Commands")
            commands.children.append(Parser.parseCommand())

            while(Parser.tokens.actual.value != "}"):
                commands.children.append(Parser.parseCommand())

            Parser.tokens.select_next()    
            return commands
        else:
            raise Exception("{ delimiter not found")

    @staticmethod
    def parseCommand(): 

        if Parser.tokens.actual.value == ";":
            pass

        elif Parser.tokens.actual.token_type == "VARIABLE":
            var_name = Parser.tokens.actual.value
            var_node = VarName(var_name, [])

            Parser.tokens.select_next()

            if Parser.tokens.actual.value == "=":
                assign = Assignment("=", [])
                assign.children.append(var_node)
                Parser.tokens.select_next()
                value = Parser.parseExpression()

                assign.children.append(value)
            
            else:
                raise Exception("Invalid Syntax")
            
            
            if Parser.tokens.actual.value != ";":
                raise Exception("; not found")
            
            return assign
        
        elif Parser.tokens.actual.value == "echo":

            echo_node = Echo("echo", [])
            Parser.tokens.select_next()
            echo_value = Parser.parseExpression()

            echo_node.children.append(echo_value)
            
            if Parser.tokens.actual.value != ";":
                raise Exception("; not found")

            Parser.tokens.select_next()
            return echo_node

        else:
            return Parser.parseBlock()

    @staticmethod
    def run(code):

        code = Pre_process.filter(code)
        Parser.tokens = Tokenizer(code)
        resultado = Parser.parseBlock()

        if Parser.tokens.actual.value != 'eof':
            raise Exception("EOF not reached")

        return resultado
