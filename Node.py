from Assembly import *


class Node:

    ide = 0

    def __init__(self, value=None, children=[]):

        self.value = value
        self.children = []
        # self.id = Node.newId()

    @staticmethod
    def newId():
        Node.ide += 1
        return Node.ide

    def Evaluate(self, st):
        pass


class BinOp(Node):

    def Evaluate(self, st):

        child_1_result = self.children[0].Evaluate(st)

        cmd = f"PUSH EBX ;"
        Assembly.MakeString(cmd)

        child_2_result = self.children[1].Evaluate(st)

        if self.value == '+':
            if child_1_result[0] != 'string' and child_2_result != "string":
                cmd = f"POP EAX ;\nADD EAX, EBX ;\nMOV EBX, EAX ;"
                Assembly.MakeString(cmd)
                return ('int', child_1_result[1] + child_2_result[1])
            
            else:
                raise Exception(f'Operacao de "+" invalida')

        elif self.value == '-':
            if child_1_result[0] != 'string' and child_2_result != "string":
                cmd = f"POP EAX ;\nSUB EAX, EBX ;\nMOV EBX, EAX ;"
                Assembly.MakeString(cmd)
                return ('int', child_1_result[1] - child_2_result[1])
            
            else:
                raise Exception(f'Operacao de "-" invalida')
        elif self.value == '*':
            if child_1_result[0] != 'string' and child_2_result != "string":
                cmd = f"POP EAX ;\nIMUL EBX ;\nMOV EBX, EAX ;"
                Assembly.MakeString(cmd)
                return ('int', child_1_result[1] * child_2_result[1])
            
            else:
                raise Exception(f'Operacao de "*" invalida')

        elif self.value == '/':
            if child_1_result[0] != 'string' and child_2_result != "string":
                cmd = f"POP EAX ;\nIDIV EBX ;\nMOV EBX, EAX ;"
                Assembly.MakeString(cmd)
                return ('int', int(child_1_result[1] / child_2_result[1]))
            
            else:
                raise Exception(f'Operacao de "/" invalida')

        elif self.value == '.':
            return ('string', child_1_result[1] + child_2_result[1])


class UnaryOp(Node):

    def Evaluate(self, st):

        value = self.children[0].Evaluate(st)

        if self.value == '+':
            cmd = f"MOV EBX, {value}"
            Assembly.MakeString(cmd)
            return ('int', value)

        else:
            cmd = f"MOV EBX, {-1 * self.children[0].Evaluate(st)}"
            Assembly.MakeString(cmd)

            return ('int', -1 * value)


class IntVal(Node):

    def Evaluate(self, st):

        cmd = f"MOV EBX, {self.value} ;"

        Assembly.MakeString(cmd)

        return ('int', self.value)


class BoolVal(Node):

    def Evaluate(self, st):
        cmd = f"MOV EBX, {self.value}"
        Assembly.MakeString(cmd)

        return ('bool', self.value)


class StringVal(Node):

    def Evaluate(self, st):
        return ('string', self.value)


class NoOp(Node):

    def Evaluate(self, st):
        pass


class Assignment(Node):

    def Evaluate(self, st):
        
        var_name = self.children[0].value
        

        if(st.is_setted(var_name)):
            expression = self.children[1].Evaluate(st)
            value = expression[1]
            ty = expression[0]
            
            st.setter(var_name, value, ty)
            cmd = f"MOV [EBP-{st.getter(var_name)[2]}], EBX;"
            Assembly.MakeString(cmd)
        else:
            cmd = f"PUSH DWORD 0 ;"
            Assembly.MakeString(cmd)
            expression = self.children[1].Evaluate(st)
            value = expression[1]
            ty = expression[0]
        
            st.setter(var_name, value, ty)

            cmd = f"MOV [EBP-{st.shiftState()}], EBX;"
            Assembly.MakeString(cmd)

class VarName(Node):

    def Evaluate(self, st):
        value = st.getter(self.value)
        cmd = f"MOV EBX, [EBP-{value[2]}];"
        Assembly.MakeString(cmd)
        return value


class Echo(Node):

    def Evaluate(self, st):

        expression = self.children[0].Evaluate(st)
        cmd = f"PUSH EBX ;\nCALL PRINT ;\nPOP EBX ;"
        Assembly.MakeString(cmd)

        print(expression[1])


class Commands(Node):

    def Evaluate(self, st):
        for cmd in self.children:
            cmd.Evaluate(st)


class LogOp(Node):

    def Evaluate(self, st):

        op = self.value
        child_1_result = self.children[0].Evaluate(st)

        cmd = f"PUSH EBX ;"
        Assembly.MakeString(cmd)

        child_2_result = self.children[1].Evaluate(st)
        i = Node.newId()
        if op == "<":
            if child_1_result[0] != 'string' and child_2_result != "string":
                
                cmd = f"POP EAX ;\nCMP EAX, EBX;\nJL TRUESTATE_{i} ;\nMOV EBX, False;\n\nTRUESTATE_{i}:\nMOVE EBX, True;\n"
                Assembly.MakeString(cmd)
                return ('bool', child_1_result[1] < child_2_result[1])
            else:
                raise Exception(f'Operacao de "<" invalida')

        elif op == ">":
            if child_1_result[0] != 'string' and child_2_result != "string":
                cmd = f"POP EAX ;\nCMP EAX, EBX;\nJG TRUESTATE_{i} ;\nMOV EBX, False;\n\nTRUESTATE_{i}:\nMOVE EBX, True;\n"
                Assembly.MakeString(cmd)
                return ('bool', child_1_result[1] > child_2_result[1])
            else:
                raise Exception(f'Operacao de ">" invalida')

        elif op == "==":
            if child_1_result[0] != 'string' and child_2_result != "string":
                cmd = f"POP EAX ;\nCMP EAX, EBX;\nJE TRUESTATE_{i} ;\nMOV EBX, False;\n\nTRUESTATE_{i}:\nMOVE EBX, True;\n"
                Assembly.MakeString(cmd)
                return ('bool', child_1_result[1] == child_2_result[1])
            else:
                raise Exception(f'Operacao de "==" invalida')

        elif op == "!":
            if child_1_result[0] != 'string':
                cmd = f"POP EAX ;\nCMP EAX, EBX;\nJNE TRUESTATE_{i} ;\nMOV EBX, False;\n\nTRUESTATE_{i}:\nMOVE EBX, True;\n"
                Assembly.MakeString(cmd)
                return ('bool', not child_1_result[1])
            else:
                raise Exception(f'Operacao de "!" invalida')

        elif op == "or":
            if child_1_result[0] != 'string' and child_2_result != "string":
                cmd = f"POP EAX ;\nOR EAX, EBX ;\nMOV EBX, 0;"
                Assembly.MakeString(cmd)
                return ('bool', child_1_result[1] or child_2_result[1])
            else:
                raise Exception(f'Operacao de "or" invalida')

        elif op == "and":
            if child_1_result[0] != 'string' and child_2_result != "string":
                cmd = f"POP EAX ;\nAND EAX, EBX ;\nMOV EBX, 0;"
                Assembly.MakeString(cmd)

                return ('bool', child_1_result[1] and child_2_result[1])
            else:
                raise Exception(f'Operacao de "and" invalida')


class LoopOp(Node):

    def Evaluate(self, st):

        i = Node.newId()

        cmd = f"LOOP_{i}"
        Assembly.MakeString(cmd)
        
        cond = self.children[0].Evaluate(st)
        cmd = f"CMP EBX, False ;\nJE EXIT_{i} ;\n"
        Assembly.MakeString(cmd)

        while (self.children[0].Evaluate(st)[1]):
            self.children[1].Evaluate(st)
            
        cmd = f"JMP LOOP_{i} ;\nEXIT_{i}:"
        Assembly.MakeString(cmd)


class IfOp(Node):

    def Evaluate(self, st):
        i = Node.newId()

        cmd = f"CMP EBX, False ;\nJE EXIT_{i} ;\n"
        Assembly.MakeString(cmd)

        if (self.children[0].Evaluate(st)[1]):
            self.children[1].Evaluate(st)

        if len(self.children) > 2:
            cmd = f"EXIT_{i}:"
            Assembly.MakeString(cmd)
            self.children[2].Evaluate(st)
        
        
        


class ReadLineOp(Node):

    def Evaluate(self, st):
        return ('int', int(input()))
