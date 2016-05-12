import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens

DEBUG = True

# Namespace & built-in functions

variables = []
constants = []

global ast
ast = []

# bnf

def p_statement(p):
    '''statement : declaration
                 | print-call
                 | assignment-call
                 | if-statement'''
    p[0] = p[1]

def p_exp_exec(p):
    'exp : LPAREN EXEC LISP_EXEC RPAREN'
    p[0] = [p[2]] + [str(p[3])]

def p_exp_list_comp(p):
    'exp : LISTCOMP LPAREN IDENTIFIER RPAREN'
    p[0] = [p[1]] + [p[3]]

def p_exp_identifier(p):
    'exp : IDENTIFIER'
    p[0] = ['return'] + [[p[1]]]

def p_if_statement(p):
    'if-statement : IF condition LCURLY statement RCURLY ELSE LCURLY statement RCURLY'
    p[0] = ['if'] + [p[2]] + [p[4]] + [p[8]]

def p_condition_true(p):
    'condition : TRUE'
    p[0] = p[1]

def p_condition_false(p):
    'condition : FALSE'
    p[0] = p[1]

def p_exp_condition(p):
    'condition : exp'
    p[0] = p[1]

def p_exp_relOp(p):
    'exp : exp relation exp'
    p[0] = [p[2]] + [p[1]] + [p[3]]

def p_relOp(p):
    '''relation : EQ_OP
                | NE_OP
                | LE_OP
                | GE_OP
                | LT_OP
                | GT_OP'''
    p[0] = p[1]

def p_exp_addOP(p):
    'exp : exp ADD_OP exp'
    p[0] = ['+'] + [p[1]] + [p[3]]

def p_exp_literal(p):
    'exp : literal'
    p[0] = p[1]

def p_item_string(p):
    '''literal : string-literal
               | NUM'''
    p[0] = p[1]

def p_string_literal(p):
    '''string-literal : static-string-literal
                      | interpolated-string-literal'''
    p[0] = p[1]

def p_static_string_literal_empty(p):
    'static-string-literal : QUOTE QUOTE'
    p[0] = []

def p_static_string_literal(p):
    'static-string-literal : BEGINSTRING QUOTE'
    p[0] = str(p[1])

def p_quoted_text_item(p):
    '''quoted-text-item : BEGINSTRING
                        | ENDSTRING'''
    p[0] = str(p[1])

def p_interpolated_string_literal_beg(p):
    'interpolated-string-literal : interpolated-text QUOTE'
    p[0] = p[1]

def p_interpolated_string_literal_beg_end(p):
    'interpolated-string-literal : interpolated-text'
    p[0] = p[1]

def p_interpolated_string_literal_end(p):
    'interpolated-string-literal : QUOTE interpolated-text'
    p[0] = p[2]

def p_interpolated_text_item_other(p):
    'interpolated-text-item : quoted-text-item'
    p[0] = str(p[1])

def p_interpolated_text_item(p):
    'interpolated-text-item : SLASH LPAREN exp RPAREN'
    p[0] = p[3]

def p_interpolated_text(p):
    'interpolated-text : interpolated-text-item'
    p[0] = [p[1]]

def p_interpolated_text_items(p):
    'interpolated-text : interpolated-text-item interpolated-text'
    p[0] = [p[1]] + p[2]

def p_print_call(p):
    'print-call : PRINT LPAREN exp RPAREN'
    global ast
    if DEBUG: print "Calling", p[1], "with", p[3]
    ast = [p[1]] + [p[3]]
    p[0] = ast
    #p[0] = lisp_eval(p[1], [p[2]]+[p[4]])

def p_let_declaration(p):
    'declaration : LET IDENTIFIER EQUALS exp'
    if DEBUG: print "Calling", p[1], "Declaration with", [p[2]]+[p[4]]
    if p[2] in constants or p[2] in variables:
        print "Error:", p[2], "has been previously declared."
    else:
        global ast
        ast = [p[1]] + [p[2]] + [p[4]]
        constants.append(p[2])
        p[0] = ast
    #p[0] = lisp_eval(p[1], [p[2]]+[p[4]])


def p_var_declaration(p):
    'declaration : VAR IDENTIFIER EQUALS exp'
    if DEBUG: print "Calling", p[1], "Declaration with", [p[2]]+[p[4]]
    if p[2] in constants or p[2] in variables:
        print "Error:", p[2], "has been previously declared."
    else:
        global ast
        ast = [p[1]] + [p[2]] + [p[4]]
        variables.append(p[2])
        p[0] = ast
    #p[0] = lisp_eval(p[1], [p[2]]+[p[4]])

def p_assignment(p):
    'assignment-call : IDENTIFIER EQUALS exp'
    if DEBUG: print "Calling Assignment with", [p[1]]+[p[3]]
    if p[1] in constants:
        print "Error:", p[1], "is a constant and cannot be changed."
    elif p[1] not in variables:
        print "Error:", p[1], "has not been declared yet."
    else:
        global ast
        ast = ['set!'] + [p[1]] + [p[3]]
        p[0] = ast

# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()


