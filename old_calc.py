import ply.lex as lex
import ply.yacc as yacc


# str_in = '(~((~(A(x)&B(x)))=>(D(c)=>(~G(z)))))'
# str_in = '((~A(x)) & ( B(y) & C(y)))'
# str_in = '(((Alpha(x, y) & Beta(Elephant, x)) & Car(yolo, boy)) | (Egg(x) & Fish(gang)))'
# str_in = 'A(x11,y11,John)'

tokens = (
    'PREDICATE',
    'IMPLIES',
    'RPAREN',
    'LPAREN',
    'OR',
    'AND',
    'NOT'
    )

# Tokens
t_PREDICATE = r'[A-Z][a-z]*\([a-zA-Z, ]*\)'
t_IMPLIES = r'=>'
t_RPAREN = r'\)'
t_LPAREN = r'\('
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'
t_ignore = " \t"

#
# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lex.lex()
data = '(A(c) => ((C(x)=>D(y))&(S(x) | ~(Y(f))))'
data = data.replace(" ", "")
#
# # Give the lexer some input
# lex.input(data)
#
# # # Tokenize
# while True:
#     tok = lex.token()
#     if not tok:
#         break      # No more input
#     print(tok)


# Parsing rules

precedence = (
    ('left', 'OR', 'AND'),
    ('left', 'IMPLIES', 'NOT'),
    ('left', 'LPAREN', 'RPAREN')
    )

# precedence = (
#     ('left','+','-'),
#     ('left','*','/'),
#     ('right','UMINUS'),
#     )
#
# dictionary of names
# names = { }


# def p_statement_assign(p):
#     'statement : NAME "=" expression'
#     names[p[1]] = p[3]


# def p_statement_expr(p):
#     'statement : expression'
#     print p[1]

def p_expression_predicate(p):
    "expression : PREDICATE"
    p[0] = p[1]


def p_expr_expr(p):
    'expression : expression IMPLIES expression'
    if p[2] == "=>":
        p[0] = '~(' + p[1] + ')|' + p[3]


def p_expression_paren(p):
    '''expression : LPAREN expression RPAREN'''
    if p[2][0] == '(' and p[2][-1] == ')':  # to remove unnecessary parenthesis
        p[0] = p[2]
    else:
        p[0] = p[1] + p[2] + p[3]


def p_expression_general(p):
    '''expression : LPAREN expression OR expression RPAREN
                  | LPAREN expression AND expression RPAREN
                  | LPAREN NOT expression RPAREN'''
    if p[2] == '~':
        p[0] = p[1] + p[2] + p[3] + p[4]
    else:
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5]



# def p_expression_binop(p):
#     '''expression : expression '+' expression
#                   | expression '-' expression
#                   | expression '*' expression
#                   | expression '/' expression'''
#     if p[2] == '+'  : p[0] = p[1] + p[3]
#     elif p[2] == '-': p[0] = p[1] - p[3]
#     elif p[2] == '*': p[0] = p[1] * p[3]
#     elif p[2] == '/': p[0] = p      [1] / p[3]
#
#
# def p_expression_uminus(p):
#     "expression : '-' expression %prec UMINUS"
#     p[0] = -p[2]
#
#


# def p_expression_paren(p):
#     "expression : LPAREN expression ')'"
#     p[0] = p[2]

# def p_expression_or(p):
#     "expression : LPAREN expression RPAREN OR expression"
#     p[0] = '(' + p[2] + '|' + p[5] + ')'

# def p_operand_predicate(p):
#     "operand : '(' PREDICATE ')'"
#     p[0] = p[1] + p[2] + p[3]
#
#
# def p_expression_operand(p):
#     "expression : operand"
#     p[0] = p[1]





# def p_expression_number(p):
#     "expression : NUMBER"
#     p[0] = p[1]
#
#
# def p_expression_name(p):
#     "expression : NAME"
#     try:
#         p[0] = names[p[1]]
#     except LookupError:
#         print "Undefined name '%s'" % p[1]
#         p[0] = 0
#
#

def p_error(p):
    print "Syntax error at '%s'" % p.value

yacc.yacc()
result = yacc.parse(data)
print(result)
#
# while True:
#    try:
#        s = raw_input('calc > ')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print(result)


# ----------------------------------------------------------------------------------------------------------------------




# def p_operator_general(p):
#     '''operator : OR
#                 | AND
#                 | NOT
#                 | IMPLIES'''
#     p[0] = p[1]


# def p_expression_general(p):
#     '''expression : LPAREN operand operator operand RPAREN
#                   | LPAREN operator operand RPAREN'''
#     if p[2] == '~':
#         p[0] = p[1] + p[2] + p[3] + p[4]
#     else:
#         p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
#
#

# def p_expression_general(p):
#     '''expression : LPAREN PREDICATE OR PREDICATE RPAREN
#                   | LPAREN PREDICATE AND PREDICATE RPAREN
#                   | LPAREN PREDICATE IMPLIES PREDICATE RPAREN
#                   | LPAREN NOT PREDICATE RPAREN'''
#     if p[1] == '~':
#         p[0] = p[1] + p[2] + p[3] + p[4]
#     else:
#         p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

# def p_expression_paren(p):
#     '''expression : LPAREN expression RPAREN'''
#     if p[2][0] == '(' and p[2][-1] == ')':  # to remove unnecessary parenthesis
#         p[0] = p[2]
#     else:
#         p[0] = p[1] + p[2] + p[3]
#
# def p_expression_predicate(p):
#     "expression : PREDICATE"
#     p[0] = p[1]
#
# def p_expr_expr(p):
#     'expression : expression IMPLIES expression'
#     if p[2] == "=>":
#         p[0] = '~(' + p[1] + ')|' + p[3]
#
#
# def p_expression_general(p):
#     '''expression : LPAREN expression OR expression RPAREN
#                   | LPAREN expression AND expression RPAREN
#                   | LPAREN NOT expression RPAREN'''
#     if p[2] == '~':
#         p[0] = p[1] + p[2] + p[3] + p[4]
#     else:
#         p[0] = p[1] + p[2] + p[3] + p[4] + p[5]