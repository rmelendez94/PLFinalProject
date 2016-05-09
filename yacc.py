import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens

DEBUG = True

# Namespace & built-in functions

name = {}
variables = {}


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

def lisp_eval(simb, items):
    if simb in name:
        return call(name[simb], eval_lists(items))
    else:
       return [simb] + items

def call(f, l):
    try:
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


#====================================================================
#===============Our Code=============================================
def p_code_block(p):
    '''code-block : LCURLY statements RCURLY
                  | LCURLY empty RCURLY'''

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

def p_return_statement(p):
    '''return-statement : RETURN
                        | RETURN expression'''

def p_constant_declaration(p):
    '''constant-declaration : LET identifier COLON type EQUALS expression'''

def p_variable_declaration(p):
    '''variable-declaration : VAR identifier COLON type EQUALS expression'''

def p_assignment_operator(p):
    '''assignment-operation : identifier EQUALS value'''

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

#===================================================================
#===================================================================

# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()


