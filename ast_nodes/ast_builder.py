# ast_builder.py
# Builds an Abstract Syntax Tree (AST) from parser output

# --------------------------------------------------
# 1. AST Node Base Class
# --------------------------------------------------

class ASTNode:
    def __init__(self, nodetype):
        self.nodetype = nodetype

    def __repr__(self):
        return self.__str__()


# --------------------------------------------------
# 2. Specific AST Node Classes
# --------------------------------------------------

class ProgramNode(ASTNode):
    def __init__(self, statements):
        super().__init__("Program")
        self.statements = statements

    def __str__(self):
        return f"Program({self.statements})"


class DeclarationNode(ASTNode):
    def __init__(self, datatype, identifier):
        super().__init__("Declaration")
        self.datatype = datatype
        self.identifier = identifier

    def __str__(self):
        return f"Declaration(type={self.datatype}, name={self.identifier})"


class AssignmentNode(ASTNode):
    def __init__(self, identifier, expression):
        super().__init__("Assignment")
        self.identifier = identifier
        self.expression = expression

    def __str__(self):
        return f"Assign({self.identifier} = {self.expression})"


class IfNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__("If")
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"If(condition={self.condition}, body={self.body})"


class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("BinaryOp")
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"


class NumberNode(ASTNode):
    def __init__(self, value):
        super().__init__("Number")
        self.value = value

    def __str__(self):
        return str(self.value)


class IdentifierNode(ASTNode):
    def __init__(self, name):
        super().__init__("Identifier")
        self.name = name

    def __str__(self):
        return self.name


# --------------------------------------------------
# 3. AST Builder Function
# --------------------------------------------------

def build_ast(parse_tree):
    """
    Converts parser tuple output into AST nodes
    """

    node_type = parse_tree[0]

    # Program
    if node_type == 'program':
        statements = [build_ast(stmt) for stmt in parse_tree[1]]
        return ProgramNode(statements)

    # Declaration
    elif node_type == 'declaration':
        _, datatype, identifier = parse_tree
        return DeclarationNode(datatype, identifier)

    # Assignment
    elif node_type == 'assign':
        _, identifier, expression = parse_tree
        return AssignmentNode(identifier, build_ast(expression))

    # If statement
    elif node_type == 'if':
        _, condition, body = parse_tree
        condition_node = build_ast(condition)
        body_nodes = [build_ast(stmt) for stmt in body]
        return IfNode(condition_node, body_nodes)

    # Binary operation
    elif node_type == 'binop':
        _, operator, left, right = parse_tree
        return BinaryOpNode(
            operator,
            build_ast(left),
            build_ast(right)
        )

    # Number
    elif node_type == 'number':
        return NumberNode(parse_tree[1])

    # Identifier
    elif node_type == 'identifier':
        return IdentifierNode(parse_tree[1])

    else:
        raise Exception(f"Unknown parse tree node: {node_type}")


# --------------------------------------------------
# 4. Testing AST Builder
# --------------------------------------------------
if __name__ == "__main__":
    # Sample parse tree (from parser.py)
    parse_tree = (
        'program',
        [
            ('declaration', 'int', 'a'),
            ('assign', 'a', ('number', 10)),
            ('if',
             ('binop', '>', ('identifier', 'a'), ('number', 5)),
             [
                 ('assign', 'a',
                  ('binop', '+', ('identifier', 'a'), ('number', 1)))
             ])
        ]
    )

    ast = build_ast(parse_tree)
    print("AST Output:")
    print(ast)
