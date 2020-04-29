class Node:

    def __init__(self, value = None, children = []):

        self.value = value
        self.children = []

    def Evaluate(self, st):
        pass

class BinOp(Node):
    
    def Evaluate(self, st):
        
        child_1_result = self.children[0].Evaluate(st)
        child_2_result = self.children[1].Evaluate(st)
        
        if self.value == '+':
            return child_1_result + child_2_result
        elif self.value == '-':
            return child_1_result - child_2_result

        elif self.value == '*':
            return child_1_result * child_2_result

        elif self.value == '/':
            return int(child_1_result / child_2_result)


class UnaryOp(Node):
    
    def Evaluate(self, st):
        
        if self.value == '+':
            return self.children[0].Evaluate(st)
        else:
            return -1 * self.children[0].Evaluate(st)

class IntVal(Node):
    
    def Evaluate(self, st):
        return self.value


class NoOp(Node):
    
    def Evaluate(self, st):
        pass

class Assignment(Node):

    def Evaluate(self, st):
        
        expression = self.children[1].Evaluate(st)

        var_name = self.children[0].value

        st.setter(var_name, expression)

        

class VarName(Node):

    def Evaluate(self, st):
        return st.getter(self.value)

class Echo(Node):

    def Evaluate(self, st):
        
        expression = self.children[0].Evaluate(st)

        print(expression)

class Commands(Node):

    def Evaluate(self, st):
        for cmd in self.children:
            cmd.Evaluate(st)

class LogOp(Node):

    def Evaluate(self, st):
        
        op = self.value

        if op == "<":
            return self.children[0].Evaluate(st) < self.children[1].Evaluate(st)
        elif op == ">":
            return self.children[0].Evaluate(st) > self.children[1].Evaluate(st)
        elif op == "==":
            return self.children[0].Evaluate(st) == self.children[1].Evaluate(st)
        elif op == "!":
            return not self.children[0].Evaluate(st)
        elif op == "or":
            return self.children[0].Evaluate(st) or self.children[1].Evaluate(st)
        elif op == "and":
            return self.children[0].Evaluate(st) and self.children[1].Evaluate(st)


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
        return int(input())