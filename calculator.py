# Calculator
#
# This is the main function of our calculator.
#
import ply.lex as lex
import ply.yacc as yacc
import calctokens
import calcgrammar
import calcinterp
from functools import partial       # Handle input

while True:
    prompt = partial(raw_input, ">>> ")
    stopword = ''
    content = ''
    for line in iter(prompt, stopword):
        content += line + '\n'

    calclexer = lex.lex(module=calctokens)
    # print "Lexical Analyzer:"
    # calclexer.input(content)
    # lexerout = []
    # while True:
    #     tok = calclexer.token()
    #     if not tok:
    #         break
    #     lexerout = lexerout + [(tok.type, tok.value)]
    # print lexerout

    calcparser = yacc.yacc(module=calcgrammar, tabmodule='parsetab')
    ast = calcparser.parse(content, lexer=calclexer)
    # print "Abstract Syntax Tree: "
    # print ast
    print calcinterp.interpret(ast)
