import ply.yacc as yacc
from lexer import tokens
from ast_nodes import *

# -------------------------
# Program structure
# -------------------------
def p_program(p):
    '''program : statement_list'''
    p[0] = Program(p[1])


def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


# -------------------------
# Statements
# -------------------------
def p_statement(p):
    '''statement : declaration
                 | assignment
                 | if_statement
                 | while_statement
                 | print_statement'''
    p[0] = p[1]


def p_declaration(p):
    '''declaration : type IDENTIFIER SEMICOLON'''
    p[0] = Declaration(p[1], p[2])


def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expression SEMICOLON'''
    p[0] = Assignment(p[1], p[3])


def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN LBRACE statement_list RBRACE
                    | IF LPAREN condition RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'''
    if len(p) == 8:
        p[0] = IfStatement(p[3], p[6])
    else:
        p[0] = IfStatement(p[3], p[6], p[10])


def p_while_statement(p):
    '''while_statement : WHILE LPAREN condition RPAREN LBRACE statement_list RBRACE'''
    p[0] = WhileStatement(p[3], p[6])


def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN SEMICOLON'''
    p[0] = PrintStatement(p[3])


# -------------------------
# Expressions
# -------------------------
def p_condition(p):
    '''condition : expression LT expression
                 | expression GT expression
                 | expression EQ expression'''
    p[0] = BinaryOp(p[1], p[2], p[3])


def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = BinaryOp(p[1], p[2], p[3])


def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]


def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = BinaryOp(p[1], p[2], p[3])


def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]


def p_factor_number(p):
    '''factor : NUMBER'''
    p[0] = Number(p[1])


def p_factor_identifier(p):
    '''factor : IDENTIFIER'''
    p[0] = Identifier(p[1])


def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]


# -------------------------
# Error handling
# -------------------------
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")


# -------------------------
# Build parser
# -------------------------
parser = yacc.yacc()
