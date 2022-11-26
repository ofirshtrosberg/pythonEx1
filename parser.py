from abc import ABC
from numpy import double
from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def calc(self) -> double:
        pass


class Num(Expression):
    def __init__(self, x) -> None:
        self.x = x

    def calc(self) -> double:
        return double(self.x)


class BinExp(Expression):
    @abstractmethod
    def __init__(self, left, right) -> None:
        pass

    @abstractmethod
    def calc(self) -> double:
        pass


class Plus(BinExp):
    def __init__(self, left, right) -> None:
        self.left = left.calc()
        self.right = right.calc()

    def calc(self) -> double:
        return double(self.left) + double(self.right)


class Minus(BinExp):
    def __init__(self, left, right) -> None:
        self.left = left.calc()
        self.right = right.calc()

    def calc(self) -> double:
        return self.left - self.right


class Mul(BinExp):
    def __init__(self, left, right) -> None:
        self.left = left.calc()
        self.right = right.calc()

    def calc(self) -> double:
        return self.left * self.right


class Div(BinExp):
    def __init__(self, left, right) -> None:
        self.left = left.calc()
        self.right = right.calc()

    def calc(self) -> double:
        return self.left / self.right


def opPriority(op):
    if op == ')':
        return 3
    elif op == '*' or op == '/':
        return 2
    elif op == '+' or op == '-':
        return 1
    else:
        return 0


def isOp(expChar):
    op = ['(', ')', '+', '-', '*', '/']
    return expChar in op


def isDigit(expChar):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return expChar in digits


def negNumbersReplaceMinusChar(expression):
    mightBeNegNumber = False
    expressionCopy = expression
    index = -1
    for i in range(0, len(expression)):
        if expression[i] == '(':
            mightBeNegNumber = True
            index = i
            continue
        elif mightBeNegNumber == True and expression[i] == '-' and index+1 == i:
            expressionCopy = expressionCopy[:i] + "&" + expressionCopy[i+1:]
            mightBeNegNumber == False
        else:
            mightBeNegNumber == False
    return expressionCopy


def parser(expression) -> double:
    # replace all '-' of negative numbers with '&'
    newExp = negNumbersReplaceMinusChar(expression)
    numbersQueue = []
    opStack = []
    currNumber = ""

    for expChar in newExp:
        if isDigit(expChar) or expChar == '.' or expChar == '&':
            currNumber += expChar
        elif isOp(expChar):
            if currNumber != "":
                if currNumber.startswith('&'):
                    currNumber = currNumber[1:]
                    numbersQueue.append((-1)*double(currNumber))
                else:
                    numbersQueue.append(double(currNumber))
                currNumber = ""
        # shunting yard algo
            if expChar == '+' or expChar == '-':
                while len(opStack) != 0 and (opPriority(opStack[len(opStack)-1]) == 1 or opPriority(opStack[len(opStack)-1]) == 2):
                    currOp = opStack.pop()
                    numbersQueue.append(currOp)
                opStack.append(expChar)
            if expChar == '(':
                opStack.append(expChar)
            if expChar == '*' or expChar == '/':
                while len(opStack) != 0 and opPriority(opStack[len(opStack)-1]) == 2:
                    currOp = opStack.pop()
                    numbersQueue.append(currOp)
                opStack.append(expChar)
            if expChar == ')':
                while len(opStack) != 0 and opStack[len(opStack)-1] != '(':
                    currOp = opStack.pop()
                    numbersQueue.append(currOp)
                if len(opStack) != 0 and opStack[len(opStack)-1] == '(':
                    currOp = opStack.pop()
    if currNumber != "":
        numbersQueue.append(double(currNumber))
        currNumber = ""
    while len(opStack) != 0:
        currOp = opStack.pop()
        numbersQueue.append(currOp)

    # calculate result
    result = 0.0
    right = 0.0
    left = 0.0
    for element in numbersQueue:
        if isOp(element) == False:
            opStack.append(element)
        if isOp(element):
            if len(opStack) >= 2:
                right = opStack.pop()
                left = opStack.pop()
                if element == '+':
                    result = Plus(Num(left), Num(right)).calc()
                elif element == '-':
                    result = Minus(Num(left), Num(right)).calc()
                elif element == '*':
                    result = Mul(Num(left), Num(right)).calc()
                else:
                    result = Div(Num(left), Num(right)).calc()
                opStack.append(result)
    return result
