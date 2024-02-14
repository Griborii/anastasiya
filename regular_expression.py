from abc import abstractmethod
from enum import Enum

class Visitor:
    def __init__(self):
        pass
    def visit(self, node):
        pass


class RegexOperations(Enum):
    CONCAT = "x"
    CLOSURE = "*"
    UNITE = "+"


class AbstractRegexNode:
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

    def __hash__(self):
        return str(self).__hash__()

    def __eq__(self, second):
        return str(self) == str(second)


class NonTerminalNode(AbstractRegexNode):
    def __init__(self, left: AbstractRegexNode, right, operation: RegexOperations):
        self.left = left
        self.right = right
        self.operation = operation

    def __str__(self):
        if self.operation == RegexOperations.CONCAT:
            return f"{self.left}{self.right}"
        elif self.operation == RegexOperations.CLOSURE:
            return f"({self.left})*"
        elif self.operation == RegexOperations.UNITE:
            return f"({self.left} + {self.right})"

    def accept(self, visitor: Visitor):
        return visitor.visit(self)


class TerminalNode(AbstractRegexNode):
    def __init__(self, letter: str = None):
        self.letter = letter

    def __str__(self):
        return self.letter

    def accept(self, visitor: Visitor):
        return visitor.visit(self)

def Index(string: str):
    cnt = 0
    for i in range(0, len(string)):
        item = string[i]
        if item == "(":
            cnt += 1
        elif item == ")":
            cnt -= 1
        elif cnt == 0 and item in "+-*.":
            return i
    return 0

def Build(st):
    print(st)
    if st[-1] == ')':
        st = st[1 : len(st) - 1]
    index = Index(st)
    if len(st) == 1:
        return TerminalNode(st[0])

    if st[index] == '*':
        return NonTerminalNode(Build(st[0: index]), None, RegexOperations.CLOSURE)
    if st[index] == '+':
        return NonTerminalNode(Build(st[0: index]), Build(st[index + 1: len(st)]), RegexOperations.UNITE)
    if st[index] == '.':
        return NonTerminalNode(Build(st[0: index]), Build(st[index + 1: len(st)]), RegexOperations.UNITE)
