class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def setter(self, name, value):
        self.symbols[name] = value

    def getter(self, name):
        return self.symbols[name]