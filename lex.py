#------------------------------------------------------------
# lex.py
#
# tokenizer
# ------------------------------------------------------------

import ply.lex as lex

# Reserved words
reserved = {
    'LET'   : 'let',
    'VAR'   : 'var',
    'IF'    : 'if',
    'ELSE'  : 'else',
    'TRUE'  : 'true',
    'FALSE' : 'false',
    'PRINT' : 'print',
    'EXEC'  : 'exec'
}

# List of token names.   
tokens = ['LISP_EXEC', 'IDENTIFIER', 'EQUALS', 'NUM', 'LPAREN', 'RPAREN', 'QUOTE', 'SLASH', 'BEGINSTRING', 'ENDSTRING', \
          'ADD_OP', 'EQ_OP', 'NE_OP', 'LE_OP', 'GE_OP', 'LT_OP', 'GT_OP', 'LCURLY', 'RCURLY'] + list(reserved.keys())

"""'BINDIG', 'OCTDIG', 'HEXDIG', 'DECDIG','STRING', \
          'LBRACKET', 'RBRACKET', 'QMARK', 'XMARK', \
          'COLON', 'EQUALS', 'DPOINT', 'COMMENT'] + list(reserved.keys())
"""
# Regular expression rules for simple tokens
"""
t_BINDIG = r'[01]'
t_OCTDIG = r'[0-7]'
t_HEXDIG = r'[0-9a-fA-F]'
t_DECDIG = r'[0-9]'

t_LBRACKET = r'\['
t_RBRACKET = r']'
t_QMARK = r'?'
t_XMARK = r'!'
t_COLON = r':'
"""
t_LCURLY = r'{'
t_RCURLY = r'}'
t_QUOTE = r'"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ADD_OP = r'\+'
t_EQUALS = r'='
t_EQ_OP  = r'=='
t_NE_OP  = r'!='
t_LE_OP  = r'<='
t_GE_OP  = r'>='
t_LT_OP  = r'<'
t_GT_OP  = r'>'

def t_LISP_EXEC(t):
    r"'.*'"
    print "Saw LISP_EXEC:", t.value
    return t

"""
t_DPOINT = r'.'
t_COMMENT = r'//'
"""

def t_SLASH(t):
    r'\\'
    return t

def t_BEGINSTRING(t):
    r'\"[\w\s\.]+'
    t.value = t.value[1:]
    return t

def t_ENDSTRING(t):
    r'[\w\s\.]+\"'
    t.value = " " + t.value[:-1]
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in reserved:
        # print "In t_IDENTIFIER, saw reserved:", t.value
        t.type = t.value.upper()
    return t

def t_NUM(t):
    r'\d+'
    try:
        t.value = int(t.value)    
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lex.lex()

if __name__ == '__main__':
    lex.runmain()
