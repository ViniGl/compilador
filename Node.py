from SymbolTable import *


class Node:

    def __init__(self, value=None, children=[]):

        self.value = value
        self.children = []

    def Evaluate(self, st):
        pass


class BinOp(Node):

    def Evaluate(self, st):

        child_1_result = self.children[0].Evaluate(st)
        child_2_result = self.children[1].Evaluate(st)

        if self.value == '+':
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('int', child_1_result[1] + child_2_result[1])
            else:
                raise Exception(f'Operacao de "+" invalida')

        elif self.value == '-':
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('int', child_1_result[1] - child_2_result[1])
            else:
                raise Exception(f'Operacao de "-" invalida')
        elif self.value == '*':
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('int', child_1_result[1] * child_2_result[1])
            else:
                raise Exception(f'Operacao de "*" invalida')

        elif self.value == '/':
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('int', int(child_1_result[1] / child_2_result[1]))
            else:
                raise Exception(f'Operacao de "/" invalida')

        elif self.value == '.':
            return ('string', child_1_result[1] + child_2_result[1])


class UnaryOp(Node):

    def Evaluate(self, st):

        if self.value == '+':
            return ('int', self.children[0].Evaluate(st))
        else:
            return ('int', -1 * self.children[0].Evaluate(st))


class IntVal(Node):

    def Evaluate(self, st):
        return ('int', self.value)


class BoolVal(Node):

    def Evaluate(self, st):
        return ('bool', self.value)

class StringVal(Node):

    def Evaluate(self, st):
        return ('string', self.value)


class NoOp(Node):

    def Evaluate(self, st):
        pass


class Assignment(Node):

    def Evaluate(self, st):

        expression = self.children[1].Evaluate(st)

        value = expression[1]
        ty = expression[0]

        var_name = self.children[0].value

        st.setter(var_name, value, ty)


class VarName(Node):

    def Evaluate(self, st):
        return st.getter(self.value)


class Echo(Node):

    def Evaluate(self, st):

        expression = self.children[0].Evaluate(st)

        print(expression[1])


class Commands(Node):

    def Evaluate(self, st):
        for cmd in self.children:
            cmd.Evaluate(st)


class LogOp(Node):

    def Evaluate(self, st):

        op = self.value
        child_1_result = self.children[0].Evaluate(st)
        child_2_result = self.children[1].Evaluate(st)

        if op == "<":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] < child_2_result[1])
            else:
                raise Exception(f'Operacao de "<" invalida')
        
        elif op == ">":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] > child_2_result[1])
            else:
                raise Exception(f'Operacao de ">" invalida')
        
        elif op == "==":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] == child_2_result[1])
            else:
                raise Exception(f'Operacao de "==" invalida')
        
        elif op == "!":
            if child_1_result[0] != 'string':
                return ('bool', not child_1_result[1])
            else:
                raise Exception(f'Operacao de "!" invalida')
        
        elif op == "or":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] or child_2_result[1])
            else:
                raise Exception(f'Operacao de "or" invalida')
        
        elif op == "and":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] and child_2_result[1])
            else:
                raise Exception(f'Operacao de "and" invalida')


class LoopOp(Node):

    def Evaluate(self, st):
        while (self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)


class IfOp(Node):

    def Evaluate(self, st):

        if (self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)

        else:
            if len(self.children) > 2:
                self.children[2].Evaluate(st)


class ReadLineOp(Node):

    def Evaluate(self, st):
        return ('int', int(input()))

class FuncDec(Node):
    def Evaluate(self, st):
        name = self.value

        args = self.children

        st.setter(name, args, "FuncDec")

class FuncCall(Node):
    """
        TODO: recuperar no da ST_FUNC a partir do nome
        TODO: Criar ST local e salvar argumentos funcdec = valores funccall 
    """
    def Evaluate(self, st):
        
        name = self.value

        args = self.children

        func_dec = st.getter(name)

        args_dec = func_dec[1]

        if len(args_dec[0:-1]) != len(args):
            raise Exception ("Invalid number of arguments") 

        st_local = SymbolTable()

        for i in range(len(args)):
            args_value = args[i].Evaluate(st)
            st_local.setter(args[i].value, args_value[1], args_value[0])
        
        func_call = args_dec[-1]

        func_call.Evaluate(st_local)
        result = st_local.getter("$$RESULT")

        if result != None:
            return result

class ReturnOp(Node):

    def Evaluate(self, st):
        
        result = self.children[0].Evaluate(st)
        st.setter("$$RESULT", result[1], result[0])

