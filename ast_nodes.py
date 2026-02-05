class Node:
    pass


class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class Declaration(Node):
    def __init__(self, var_type, name):
        self.var_type = var_type
        self.name = name


class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class IfStatement(Node):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class WhileStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class PrintStatement(Node):
    def __init__(self, expr):
        self.expr = expr


class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Number(Node):
    def __init__(self, value):
        self.value = value


class Identifier(Node):
    def __init__(self, name):
        self.name = name
