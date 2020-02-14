import sys

eq = sys.argv[1:]

def process(a2):
    eq = "".join(a2)
    ops = []
    for i in eq:
        if i == "+":
            ops.append("+")
        elif i == "-":
            ops.append("-")
    eq = eq.replace("+"," ").replace("-"," ").split(" ")
    return eq, ops


p = process(eq)

def calculate(nums, ops):
    soma = int(nums[0])

    opsC = 0
    if len(ops) == 0:
        return
    for i in nums[1:]:
        if ops[opsC] == "+":
            soma += int(i)
        elif ops[opsC] == "-":
            soma -= int(i)
        opsC += 1     
    return soma

print(calculate(p[0],p[1]))

