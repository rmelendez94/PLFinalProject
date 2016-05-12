import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens

DEBUG = True

# Namespace & built-in functions

variables = []
constants = []

global ast
ast = []

"""
def cons(l):
    return [l[0]] + l[1]

name['cons'] = cons

def concat(l):
    return l[0] + l[1]

name['concat'] = concat

def listar(l):
    return l

name['list'] = listar

def car(l):
    return l[0][0]

name['car'] = car

def cdr(l):
    return l[0][1:]

name['cdr'] = cdr

def eq(l):
    return l[0] == l[1]

name['eq'] = eq
name['='] = eq

def _and(l):
    return not False in l

name['and'] = _and

def _or(l):
    return True in l

name['or'] = _or

def cond(l):
    if l[0]:
        return l[1]

name['cond'] = cond

def add(l):
    return sum(l)

name['+'] = add

def minus(l):
    '''Unary minus'''
    return -l[0]

name['-'] = minus

def _print(l):
    print lisp_str(l[0])

name['print'] = _print

#  Evaluation functions


# BNF

def p_exp_atom(p):
    'exp : atom'
    p[0] = p[1]

def p_exp_qlist(p):
    'exp : quoted_list'
    p[0] = p[1]

def p_exp_call(p):
    'exp : call'
    p[0] = p[1]

def p_list(p):
    'list : LBRACKET items RBRACKET'
    p[0] = p[2]

def p_items(p):
    'items : item items'
    p[0] = [p[1]] + p[2]

def p_items_empty(p):
    'items : empty'
    p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_item_atom(p):
    'item : atom'
    p[0] = p[1]

def p_item_list(p):
    'item : list'
    p[0] = p[1]

def p_item_list(p):
    'item : quoted_list'
    p[0] = p[1]
        
def p_item_call(p):
    'item : call'
    p[0] = p[1]

def p_item_empty(p):
    'item : empty'
    p[0] = p[1]

def p_call(p):
    'call : LPAREN SIMB items RPAREN'
    if DEBUG: print "Calling", p[2], "with", p[3] 
    p[0] = lisp_eval(p[2], p[3])   

def p_atom_simbol(p):
    'atom : SIMB'
    p[0] = p[1]

def p_atom_bool(p):
    'atom : bool'
    p[0] = p[1]

def p_atom_num(p):
    'atom : NUM'
    p[0] = p[1]

def p_atom_word(p):
    'atom : TEXT'
    p[0] = p[1]

def p_atom_empty(p): 
    'atom :'
    pass

def p_true(p):
    'bool : TRUE'
    p[0] = True

def p_false(p):
    'bool : FALSE'
    p[0] = False

def p_nil(p):
    'atom : NIL'
    p[0] = None


def let(l):
    print "in let function with", l
    constants[l[0]] = l[1]
    return

name['let'] = let

def lisp_eval(simb, items):
    if simb in name:
        return call(name[simb], eval_lists(items))
    else:
        return [simb] + items

def call(f, l):
    try:
        print "in call function with function and list", f, l
        return f(eval_lists(l))
    except TypeError:
        return f

def eval_lists(l):
    r = []
    for i in l:
        if is_list(i):
            if i:
                r.append(lisp_eval(i[0], i[1:]))
            else:
                r.append(i)
        else:
            r.append(i)
    print "in eval_lists with", r
    return r

# Utilities functions

def is_list(l):
    return type(l) == type([])

def lisp_str(l):
    if type(l) == type([]):
        if not l:
            return "()"
        r = "("
        for i in l[:-1]:
            r += lisp_str(i) + " "
        r += lisp_str(l[-1]) + ")"
        return r
    elif l is True:
        return "#t"
    elif l is False:
        return "#f"
    elif l is None:
        return 'nil'
    else:
        return str(l)
"""
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

def p_exp_identifier(p):
    'exp : IDENTIFIER'
    p[0] = ['return'] + [[p[1]]]
    print "EXP_IDENTIFER:", p[0]

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
    print "Found static-string-literal:", p[0]

def p_quoted_text_item(p):
    '''quoted-text-item : BEGINSTRING
                        | ENDSTRING'''
    p[0] = str(p[1])
    print "Found quoted-text-item:", p[0]

def p_interpolated_string_literal_beg(p):
    'interpolated-string-literal : interpolated-text QUOTE'
    print "Found interpolated-string-literal-beg"
    p[0] = p[1]

def p_interpolated_string_literal_beg_end(p):
    'interpolated-string-literal : interpolated-text'
    print "Found interpolated-string-literal-begandend"
    p[0] = p[1]

def p_interpolated_string_literal_end(p):
    'interpolated-string-literal : QUOTE interpolated-text'
    print "Found interpolated-string-literal-end"
    p[0] = p[2]

def p_interpolated_text_item_other(p):
    'interpolated-text-item : quoted-text-item'
    p[0] = str(p[1])
    print "Found interpolated-text-item:", p[1]

def p_interpolated_text_item(p):
    'interpolated-text-item : SLASH LPAREN exp RPAREN'
    p[0] = p[3]
    print "Found interpolated-text-item:", p[0]

def p_interpolated_text(p):
    'interpolated-text : interpolated-text-item'
    p[0] = [p[1]]
    print "Found interpolated-text:", p[0]

def p_interpolated_text_items(p):
    'interpolated-text : interpolated-text-item interpolated-text'
    p[0] = [p[1]] + p[2]
    print "Found interpolated-text:", p[0]

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


#====================================================================
#===============Our Code=============================================

"""
def p_program(p):
    '''program : declarations
               | functions
               | declarations functions'''
    print "Saw:", p[1]

def p_constant_declaration(p):
    '''declaration : LET identifier EQUALS expression'''
    print "Calling", p[1], "with", [p[2]]+[p[4]]
    p[0] = lisp_eval(p[1], [p[2]]+[p[4]])

def p_variable_declaration(p):
    '''variable-declaration : VAR identifier COLON type EQUALS expression
                            | VAR identifier EQUALS expression'''

def p_assignment_operator(p):
    '''assignment-operation : identifier EQUALS value'''
    # identifier should already be declared as a variable
    if p[1] in variables:
        variables[p[1]] = p[3]
    else:
        print "Do not recognize", p[1] + ". Variable should have been declared beforehand."

def p_ternary_conditional_operator(p):
    '''ternary-conditional-operation : condition QMARK expression COLON expression'''
    if evaluate_condition(p[1]):
        p[0] = p[3]
    else:
        p[0] = p[5]



def p_identifier(p):
    '''identifier : IDENTIFIER'''
    # add identifier to variable list
    p[0] = p[1]

def p_literal(p):
    '''literal : numeric-literal
               | string-literal
               | boolean-literal
               | nil-literal'''
    p[0] = p[1]

def p_numeric_literal_integer(p):
    '''numeric-literal : integer-literal
                       | "-" integer-literal
                       | floating-point-literal
                       | "-" floating-point-literal'''
    if len(p) == 3:
        p[0] = -p[2]
    else:
        p[0] = p[1]

def p_string_literal(p):
    '''string-literal : QUOTE STRING QUOTE
                      | interpolated-string-literal'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_interpolated_string_literal(p):
    '''interpolated-string-literal : QUOTE interpolated-text QUOTE
    '''
    p[0] = str(p[2])

def p_interpolated_text(p):
    '''interpolated-text : interpolated-text-item
                         | interpolated-text-item interpolated-text'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_interpolated_text_item(p):
    '''interpolated-text-item : "\" LPAREN expression RPAREN
                              | STRING'''
    if len(p) == 5:
        # convert expression to string by finding it in a variables dictionary
        if p[3] in variables:
            p[0] = p[1] + p[2] + variables[p[3]] + p[4]
        else:
            print "Error: " + p[3] + " does not exist."
            p[0] = ""
    else:
        p[0] = p[1]

def p_boolean_literal(p):
    '''boolean-literal: TRUE
                      | FALSE'''
    if p[1] == 'true':
        p[0] = True
    else:
        p[0] = False

def p_nil_literal(p):
    '''nil-literal : NIL'''
    p[0] = None

def p_integer_literal(p):
    '''integer-literal : binary-literal
                       | octal-literal
                       | decimal-literal
                       | hexadecimal-literal'''
    if p[1][:2] == "0b":
        p[0] = int(p[1][2:],2)
    elif p[1][:2] == "0o":
        p[0] = int(p[1][2:],8)
    elif p[1][:2] == "0x":
        p[0] = int(p[1][2:],16)
    else:
        p[0] = int(p[1])

def p_binary_literal(p):
    '''binary-literal : '0b' BINDIG
                      | 'Ob' BINDIG binary-literal-characters'''
    if len(p) == 4:
        p[0] = p[1] + str(p[2]) + p[3]
    else:
        p[0] = p[1] + str(p[2])

def p_binary_literal_characters(p):
    '''binary-literal-characters : binary-literal-character binary-literal-characters'''
    p[0] = p[1] + p[2]

def p_binary_literal_character(p):
    '''binary-literal-character : BINDIG'''
    p[0] = str(p[1])

def p_binary_literal_characters_empty(p):
    '''binary-literal-characters : empty'''
    p[0] = ""

def p_octal_literal(p):
    '''octal-literal : '0o' OCTDIG
                     | '0o' OCTDIG octal-literal-characters'''
    if len(p) == 4:
        p[0] = p[1] + str(p[2]) + p[3]
    else:
        p[0] = p[1] + str(p[2])

def p_octal_literal_characters(p):
    '''octal-literal-characters : octal-literal-character octal-literal-characters'''
    p[0] = p[1] + p[2]

def p_octal_literal_character(p):
    '''octal-literal-character : OCTDIG'''
    p[0] = str(p[1])

def p_octal_literal_characters_empty(p):
    '''octal-literal-characters : empty'''
    p[0] = ""

def p_decimal_literal(p):
    '''decimal-literal : DECDIG
                       | DECDIG decimal-literal-characters'''
    if len(p) == 3:
        p[0] = str(p[1]) + p[2]
    else:
        p[0] = str(p[1])

def p_decimal_literal_characters(p):
    '''decimal-literal-characters : decimal-literal-character decimal-literal-characters'''
    p[0] = p[1] + p[2]

def p_decimal_literal_character(p):
    '''decimal-literal-character : DECDIG'''
    p[0] = str(p[1])

def p_decimal_literal_characters_empty(p):
    '''decimal-literal-characters : empty'''
    p[0] = ""

def p_hexadecimal_literal(p):
    '''hexadecimal-literal : '0x' HEXDIG
                           | '0x' HEXDIG hexadecimal-literal-characters'''
    if len(p) == 4:
        p[0] = p[1] + str(p[2]) + p[3]
    else:
        p[0] = p[1] + str(p[2])

def p_hexadecimal_literal_characters(p):
    '''hexadecimal-literal-characters : hexadecimal-literal-character hexadecimal-literal-characters'''
    p[0] = p[1] + p[2]

def p_hexadecimal_literal_character(p):
    '''hexadecimal-literal-character : HEXDIG'''
    p[0] = str(p[1])

def p_hexadecimal_literal_characters_empty(p):
    '''hexadecimal-literal-characters : empty'''
    p[0] = ""
"""
#===================================================================
#======= TO BE IMPLEMENTED =========================================

"""

def p_statement(p):
    '''statement : expression
                 | expression ";"
                 | declaration
                 | declaration ";"
                 | if-statement
                 | if-statement ";"
                 | return-statement
                 | return-statement ";"'''


def p_if_statement(p):
    '''if-statement : IF condition-clause code-block
                    | IF condition-clause code-block else-clause'''
    if evaluate_condition(p[2]):
        p[0] = p[3]
    else:
        if len(p) == 5:
            p[0] = p[4]

def p_else_clause(p):
    '''else-clause : ELSE code-block
                   | ELSE if-statement'''
    p[0] = p[2]

def p_return_statement(p):
    '''return-statement : RETURN
                        | RETURN expression'''

def p_code_block(p):
    '''code-block : LCURLY statements RCURLY
                  | LCURLY empty RCURLY'''


"""

# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()


