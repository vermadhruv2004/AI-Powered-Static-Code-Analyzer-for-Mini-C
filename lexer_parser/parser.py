# parser.py
# Syntax Analyzer using PLY (Python Yacc)

import ply.yacc as yacc
from lexer_parser.lexer import tokens

# --------------------------------------------------
# 1. Operator precedence (important!)
# --------------------------------------------------
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ASSIGN'),
)

# --------------------------------------------------
# 2. Grammar rules
# --------------------------------------------------

# Program start
def p_program(p):
    """
    program : statement_list
    """
    p[0] = ('program', p[1])


# List of statements
def p_statement_list(p):
    """
    statement_list : statement_list statement
                   | statement
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


# Statement types
def p_statement(p):
    """
    statement : declaration
              | assignment
              | if_statement
    """
    p[0] = p[1]


# Variable declaration
def p_declaration(p):
    """
    declaration : INT IDENTIFIER SEMICOLON
                | FLOAT IDENTIFIER SEMICOLON
    """
    p[0] = ('declaration', p[1], p[2])


# Assignment
def p_assignment(p):
    """
    assignment : IDENTIFIER ASSIGN expression SEMICOLON
    """
    p[0] = ('assign', p[1], p[3])


# If statement
def p_if_statement(p):
    """
    if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
    """
    p[0] = ('if', p[3], p[6])


# Expression rules
def p_expression_binop(p):
    """
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression GT expression
               | expression LT expression
               | expression GE expression
               | expression LE expression
               | expression EQ expression
               | expression NE expression
    """
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_group(p):
    """
    expression : LPAREN expression RPAREN
    """
    p[0] = p[2]


def p_expression_number(p):
    """
    expression : NUMBER
    """
    p[0] = ('number', p[1])


def p_expression_identifier(p):
    """
    expression : IDENTIFIER
    """
    p[0] = ('identifier', p[1])


# --------------------------------------------------
# 3. Error handling
# --------------------------------------------------
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")


# --------------------------------------------------
# 4. Build the parser
# --------------------------------------------------
parser = yacc.yacc()

# --------------------------------------------------
# 5. Testing the parser
# --------------------------------------------------
if __name__ == "__main__":
    data = """
    int a;
    a = 10;
    if (a > 5) {
        a = a + 1;
    }
    """

    result = parser.parse(data)
    print("Parse Result:")
    print(result)
