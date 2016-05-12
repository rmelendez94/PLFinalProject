################ Lispy: Scheme Interpreter in Python

## (c) Peter Norvig, 2010-14; See http://norvig.com/lispy.html

################ Types

from __future__ import division

Symbol = str          # A Lisp Symbol is implemented as a Python str
List   = list         # A Lisp List is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

################ Environments

def standard_env():
    "An environment with some Scheme standard procedures."
    import math, operator as op
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.div, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '==':op.eq,
        'length':  len,
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list),
        'exec':    lambda x: eval(compile(x,'None','single')),
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)

global_env = standard_env()

################ Interaction: A REPL

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None: 
            print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if  isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)

################ Procedures

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))

################ eval
variables = []
operations = global_env.keys()

toReturn = None

def eval(x, env=global_env):
    print("EVAL:"), x
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol) and x in variables:      # variable reference
        print "In Symbol and is variable:", x, env.find(x)[x]
        return env.find(x)[x]
    elif isinstance(x,Symbol) and x in operations:
        print "In Symbol and is operation:", x, env.find(x)[x]
        return env.find(x)[x]
    elif not isinstance(x, List):  # constant literal
        print "In IS_NOT_LIST:", x
        return x
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'let' or x[0] == 'var':         # (let var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
        variables.append(var)
        print "all variables:", variables
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)
    elif x[0] == 'exec':
        proc = eval(x[0], env)
        import re
        exec(proc(re.sub(r"^'|'$", '', x[1])))
        return toReturn
    elif x[0] == 'let':
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'return':
        print "In RETURN:", x[1][0]
        return eval(x[1][0], env)
    elif x[0] == 'print':
        print "In PRINT:", x[1]
        return eval(x[1],env)
    else:                          # (proc arg...)
        print "In ELSE:", x
        if x[0] in operations:
            proc = eval(x[0], env)
            args = [eval(exp, env) for exp in x[1:]]
            return proc(*args)
        #elif isinstance(x, List) and len(x) == 1 and isinstance(x[0], Symbol):
        #    return eval(x[0], env)
        #elif isinstance(x, List) and len(x) == 1 and isinstance(x[0], Number):
        #    return eval(x[0], env)
        else:
            print "I got to toReturn:", x
            toReturn = ""
            for i in x:
                toReturn += str(eval(i,env))
            return toReturn
