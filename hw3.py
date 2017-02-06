import ply.lex as lex
import ply.yacc as yacc
import re


def pass1():  # eliminate implications

    def p_fin_exp(p):
        '''final : BLPAREN expression ERPAREN'''
        p[0] = p[1] + p[2] + p[3]

    def p_expr_implies(p):
        '''expression : LPAREN expression IMPLIES expression RPAREN'''
        p[0] = '((~' + p[2] + ')|' + p[4] + ')'

    def p_expr_general(p):
        '''expression : LPAREN expression OR expression RPAREN
                      | LPAREN expression AND expression RPAREN
                      | LPAREN NOT expression RPAREN'''
        if p[2] == '~':
            p[0] = p[1] + p[2] + p[3] + p[4]
        else:
            p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

    def p_expr_pred(p):
        '''expression : predicate'''
        p[0] = p[1]

    def p_pred_paren(p):
        '''predicate : LPAREN predicate RPAREN'''
        p[0] = p[2]

    def p_pred_pred(p):
        '''predicate : PREDICATE'''
        p[0] = p[1]

    def p_error(p):
        print "Syntax error at '%s'" % p.value

    yacc.yacc()
    result = yacc.parse(data)
    return result


def pass2():  # move ~ inside

    def p_fin_exp2(p):
        '''final : BLPAREN expression ERPAREN'''
        p[0] = p[1] + p[2] + p[3]

    def p_expr_not2(p):
        '''expression : LPAREN NOT LPAREN NOT expression RPAREN RPAREN'''
        p[0] = p[5]

    def p_expr_general2(p):
        '''expression : LPAREN expression OR expression RPAREN
                      | LPAREN expression IMPLIES expression RPAREN
                      | LPAREN expression AND expression RPAREN
                      | LPAREN LPAREN NOT expression RPAREN AND expression RPAREN
                      | LPAREN LPAREN NOT expression RPAREN OR expression RPAREN
                      | LPAREN LPAREN NOT expression RPAREN OR LPAREN NOT expression RPAREN RPAREN
                      | LPAREN LPAREN NOT expression RPAREN AND LPAREN NOT expression RPAREN RPAREN
                      | LPAREN expression AND LPAREN NOT expression RPAREN RPAREN
                      | LPAREN expression OR LPAREN NOT expression RPAREN RPAREN'''
        if p[3] == '~' and p[8] == '~':
            p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8] + p[9] + p[10] + p[11]
        elif p[3] == '~' or p[5] == '~':
            p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8]
        else:
            p[0] = p[1] + p[2] + p[3] + p[4] + p[5]


    def p_expr_or_not2(p):
        '''expression : LPAREN NOT LPAREN expression OR expression RPAREN RPAREN'''
        p[0] = '((~' + p[4] + ')&(~' + p[6] + '))'

    def p_expr_and_not2(p):
        '''expression : LPAREN NOT LPAREN expression AND expression RPAREN RPAREN'''
        p[0] = '((~' + p[4] + ')|(~' + p[6] + '))'

    def p_expr_pred2(p):
        '''expression : predicate'''
        p[0] = p[1]

    def p_expr_not_paren2(p):
        '''expression : LPAREN NOT predicate RPAREN'''
        p[0] = p[1] + p[2] + p[3] + p[4]

    def p_expr_expr2(p):
        '''expression : LPAREN expression RPAREN'''
        p[0] = p[1] + p[2] + p[3]

    def p_pred_not2(p):
        '''predicate : LPAREN NOT LPAREN NOT predicate RPAREN RPAREN'''
        p[0] = p[5]

    # (((~A(x)) | (~B(x))) & (D(c) & G(z)))
    def p_pred_paren2(p):
        '''predicate : LPAREN predicate RPAREN'''
        p[0] = p[2]

    def p_pred_pred2(p):
        '''predicate : PREDICATE'''
        p[0] = p[1]

    def p_error(p):
        print "Syntax error at '%s'" % p.value

    yacc.yacc()
    result = yacc.parse(data)
    return result


def pass3():

    def p_fin_exp3(p):
        '''final : BLPAREN expression ERPAREN'''
        p[0] = p[1] + p[2] + p[3]

    def p_distr_or_and_slhs3(p):
        '''expression : LPAREN expression OR LPAREN expression AND expression RPAREN RPAREN'''
        p[0] = '((' + p[2] + '|' + p[5] + ')' + '&' '(' + p[2] + '|' + p[7] + '))'

    def p_distr_or_srhs3(p):
        '''expression : LPAREN LPAREN expression AND expression RPAREN OR  expression RPAREN'''
        p[0] = '((' + p[3] + '|' + p[8] + ')' + '&' '(' + p[5] + '|' + p[8] + '))'

    def p_expr_general3(p):
        '''expression : LPAREN NOT expression RPAREN
                      | LPAREN expression IMPLIES expression RPAREN
                      | LPAREN expression OR expression RPAREN
                      | LPAREN expression AND expression RPAREN'''
        if p[2] == '~':
            p[0] = p[1] + p[2] + p[3] + p[4]
        else:
            p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

    def p_expr_pred3(p):
        '''expression : predicate'''
        p[0] = p[1]

    def p_pred_pred3(p):
        '''predicate : PREDICATE'''
        p[0] = p[1]

    def p_error(p):
        print "Syntax error at '%s'" % p.value

    yacc.yacc()
    result = yacc.parse(data)
    return result


def split_conj(in_str):
    out_list = []
    out_list = out_list + pass4(in_str)

    if len(out_list) == 1:
        output.append(out_list.pop())
        return
    else: # split conjuncts recursively
        for item in out_list:
            split_conj(item)
    return


def pass4(data1):

    conj_list = []
    def p_fin_exp4(p):
        '''final : expression'''
        p[0] = p[1]

    def p_fin_pred4(p):
        '''final : BLPAREN expression ERPAREN'''
        p[0] = p[1] + p[2] + p[3]

    def p_expr_general4(p):
        '''expression : LPAREN NOT expression RPAREN
                      | LPAREN expression IMPLIES expression RPAREN
                      | LPAREN expression OR expression RPAREN
                      | LPAREN expression AND expression RPAREN'''
        if p[2] == '~':
            p[0] = p[1] + p[2] + p[3] + p[4]
        else:
            p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

    def p_distr_or_srhs4(p):
        '''expression :  BLPAREN LPAREN expression AND expression RPAREN ERPAREN'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]
        conj_list.append('('+p[3]+')')
        conj_list.append('('+p[5]+')')

    def p_expr_pred4(p):
        '''expression : predicate'''
        p[0] = p[1]

    def p_pred_pred4(p):
        '''predicate : PREDICATE'''
        p[0] = p[1]

    def p_error(p):
        print "Syntax error at '%s'" % p.value

    yacc.yacc()
    res = yacc.parse(data1)
    if len(conj_list) > 1:
        return conj_list
    else:
        return [res]


# ---------------------------------------------Execution Starts Here----------------------------------------------------
# -----------------------------------------------------Lex--------------------------------------------------------------
tokens = (
    'PREDICATE',
    'IMPLIES',
    'RPAREN',
    'LPAREN',
    'ERPAREN',
    'BLPAREN',
    'OR',
    'AND',
    'NOT'
)

# Tokens
t_PREDICATE = r'[A-Z][a-z]*\((([a-z]|[A-Z])[a-z]*[0-9]*,?)+\)'
t_IMPLIES = r'=>'
t_RPAREN = r'\)'
t_LPAREN = r'\('
t_ERPAREN = r'\)$'
t_BLPAREN = r'^\('
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'
t_ignore = " \t"


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lex.lex()

# --------------------------------------------------End of Lex----------------------------------------------------------

query_list = []
orig_sentence_list = []
output = []
line_num = 1
std_output = []
cnf_sentence_list = []
answer_list = []

# ----------------------------------------------------Fetch input-------------------------------------------------------
# Fetch input from the file
gv_fh_input = open("input.txt", "r")
# read the file and set the global vars

# ---Get query list---
n = int(gv_fh_input.readline())

while n > 0:
    temp_line = gv_fh_input.readline().rstrip()
    if temp_line[0] == "~":
        temp_line = "(" + temp_line + ")"
    query_list.append(temp_line)
    n -= 1

#  --- Get sentence list---
n = int(gv_fh_input.readline())

while n > 0:
    temp_line = gv_fh_input.readline().rstrip()
    orig_sentence_list.append(temp_line)
    n -= 1

gv_fh_input.close()

# ----------------------------------------------------Convert to CNF----------------------------------------------------
for line in orig_sentence_list:
    str_in = line
    str_in = str_in.replace(" ", "")
    str_in = '(' + str_in + ')'
    data = str_in
    # print "Input " + str(line_num) + " : " + data
    # line_num += line_num

    # eliminate implications
    res1 = pass1()
    # print res1
    data = res1
    prev_res = ""

    # recursively move ~ inside
    while 1:
        res2 = pass2()
        data = res2
        # print res2

        if prev_res == res2:
            break
        prev_res = res2

    # apply distributivity rule
    while 1:
        res2 = pass3()
        # print res2
        data = res2
        if prev_res == res2:
            break
        prev_res = res2

    split_conj(data)

for item in output:
    item = item[1:-1]
    std_output.append(item)

# line_num = 1
for item in std_output:
    std_str = "\\1a" + str(line_num)
    line_num += 1
    item = re.sub(r'(\([a-z])', std_str, item)
    item = re.sub(r'(,[a-z])', std_str, item)
    cnf_sentence_list.append(item)

for x in cnf_sentence_list:
    print "-----------------------------------------------------"
    print x
    print "-----------------------------------------------------"
    lex.input(x)

    # # Tokenize
    while True:
        tok = lex.token()
        if not tok:
            break  # No more input
        print(tok)





# # -----------------------------------------------Generate output file-------------------------------------------------
# gv_fh_output = open("output.txt", "w")
# answer_list.append("TRUE")
# answer_list.append("FALSE")
#
# for ans in answer_list:
#     ans += "\n"
#     gv_fh_output.write(ans)
# gv_fh_output.close()
#
# exit()
