class SymbolTable:

    def __init__(self):
        self.symbols = {}
        self.shift = 0

    def shiftState(self):
        return self.shift

    def is_setted(self, key):

        if key in self.symbols:
            return True
        return False
    def setter(self, name, value, typ):
        self.shift += 4
        self.symbols[name] = (typ, value, self.shift)


    def getter(self, name):
        return self.symbols[name]