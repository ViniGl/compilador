class Node:

    def __init__(self, value = None, children = []):

        self.value = value
        self.children = []

    def Evaluate(self):
        pass

class BinOp(Node):
    
    def Evaluate(self):
        
        child_1_result = self.children[0].Evaluate()
        child_2_result = self.children[1].Evaluate()
        
        if self.value == '+':
            return child_1_result + child_2_result
        elif self.value == '-':
            return child_1_result - child_2_result

        elif self.value == '*':
            return child_1_result * child_2_result

        elif self.value == '/':
            return int(child_1_result / child_2_result)


class UnaryOp(Node):
    
    def Evaluate(self):
        
        if self.value == '+':
            return self.children[0].Evaluate()
        else:
            return -1 * self.children[0].Evaluate()

class IntVal(Node):
    
    def Evaluate(self):
        return self.value


class NoOp(Node):
    
    def Evaluate(self):
        pass

