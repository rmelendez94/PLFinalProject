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
    'NIL'   : 'nil',
    'TRUE'  : 'true',
    'FALSE' : 'false',
    'RETURN': 'return',
}

# List of token names.   
tokens = ['IDENTIFIER', 'BINDIG', 'OCTDIG', 'HEXDIG', 'DECDIG', \
          'STRING', 'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY', 'QMARK', 'XMARK', \
          'COLON', 'EQUALS', 'DPOINT', 'SLASH', 'COMMENT', 'ADD_OP', \
          'EQ_OP', 'NE_OP', 'LE_OP', 'GE_OP', 'LT_OP', 'GT_OP'] + list(reserved.keys())

# Regular expression rules for simple tokens

t_BINDIG = r'[01]'
t_OCTDIG = r'[0-7]'
t_HEXDIG = r'[0-9a-fA-F]'
t_DECDIG = r'[0-9]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_QMARK = r'?'
t_XMARK = r'!'
t_COLON = r':'
t_EQUALS = r'='
t_DPOINT = r'.'
t_SLASH = r'\\'
t_COMMENT = r'//'
t_ADD_OP = r'+'
t_EQ_OP  = r'=='
t_NE_OP  = r'!='
t_LE_OP  = r'<='
t_GE_OP  = r'>='
t_LT_OP  = r'<'
t_GT_OP  = r'>'


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in reserved:
        # print "In t_IDENTIFIER, saw: ", t.value
        t.type = t.value.upper()
    return t


def t_STRING(t):
    r'"[a-zA-Z0-9_+\*\- :,]*"'
    return t


"""
def t_NUM(t):
    r'\d+'
    try:
        t.value = int(t.value)    
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t

def t_SIMB(t):
    r'[a-zA-Z_+=\*\-][a-zA-Z0-9_+\*\-]*'
    t.type = reserved.get(t.value,'SIMB')    # Check for reserved words
    return t

def t_TEXT(t):
    r'\'[a-zA-Z0-9_+\*\- :,]*\''
    t.type = reserved.get(t.value,'TEXT')    # Check for reserved words
    return t

"""

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
