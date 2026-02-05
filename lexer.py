import ply.lex as lex

# ----------------------
# List of token names
# ----------------------
tokens = (
    'INT',
    'FLOAT',
    'IF',
    'ELSE',
    'WHILE',
    'PRINT',
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
    'LT',
    'GT',
    'EQ',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON'
)

# ----------------------
# Reserved keywords
# ----------------------
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT'
}

# ----------------------
# Regular Expressions
# ----------------------
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_ASSIGN    = r'='
t_LT        = r'<'
t_GT        = r'>'
t_EQ        = r'=='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'

# ----------------------
# Identifier & keywords
# ----------------------
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# ----------------------
# Number (int & float)
# ----------------------
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# ----------------------
# Ignored characters
# ----------------------
t_ignore = ' \t'

# ----------------------
# Newlines
# ----------------------
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ----------------------
# Error handling
# ----------------------
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# ----------------------
# Build lexer
# ----------------------
lexer = lex.lex()


if __name__ == "__main__":
    data = """
    int x;
    x = 10;
    if (x > 5) {
        print(x);
    }
    """

    lexer.input(data)
    for token in lexer:
        print(token)
