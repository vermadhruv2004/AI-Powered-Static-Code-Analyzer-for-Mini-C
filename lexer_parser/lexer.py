# lexer.py
# Lexical Analyzer using PLY (Python Lex-Yacc)

import ply.lex as lex

# --------------------------------------------------
# 1. List of token names
# --------------------------------------------------
tokens = (
    'IDENTIFIER',
    'NUMBER',

    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN',

    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON',

    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'
)

# --------------------------------------------------
# 2. Reserved keywords
# --------------------------------------------------
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN'
}

tokens = tokens + tuple(reserved.values())

# --------------------------------------------------
# 3. Regular expression rules for simple tokens
# --------------------------------------------------
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_ASSIGN    = r'='

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'

t_LE        = r'<='
t_GE        = r'>='
t_EQ        = r'=='
t_NE        = r'!='
t_LT        = r'<'
t_GT        = r'>'

# --------------------------------------------------
# 4. Identifier rule (variables, function names)
# --------------------------------------------------
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# --------------------------------------------------
# 5. Number rule (integers only for now)
# --------------------------------------------------
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# --------------------------------------------------
# 6. Ignore spaces and tabs
# --------------------------------------------------
t_ignore = ' \t'

# --------------------------------------------------
# 7. Newline handling
# --------------------------------------------------
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# --------------------------------------------------
# 8. Error handling
# --------------------------------------------------
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# --------------------------------------------------
# 9. Build the lexer
# --------------------------------------------------
lexer = lex.lex()

# --------------------------------------------------
# 10. Testing the lexer (run this file directly)
# --------------------------------------------------
if __name__ == "__main__":
    data = """
    int a = 10;
    if (a > 5) {
        a = a + 1;
    }
    """

    lexer.input(data)

    print("Tokens:")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
