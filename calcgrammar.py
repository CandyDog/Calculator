import ply.yacc as yacc
from calctokens import tokens

start = 'calc'

precedence = (
	('left', 'OROR'),
	('left', 'ANDAND'),
	('left', 'EQUEQU'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE', 'MOD'),
	('right', 'NOT'),
	('left', 'POWER'),
)

# calc
def p_calc(p):
	'calc : element calc'
	p[0] = [p[1]] + p[2]
def p_calc_empty(p):
	'calc : '
	p[0] = [ ]

# element
def p_element_function(p):
	'element : FUNCTION IDENTIFIER LPAREN optparams RPAREN compoundstmt'
	p[0] = ("function", p[2], p[4], p[6])
def p_element_sstmt(p):
	'element : sstmt'
	p[0] = ("stmt", p[1])

# optparams
def p_optparams_params(p):
	'optparams : params'
	p[0] = p[1]
def p_optparams_empty(p):
	'optparams : '
	p[0] = [ ]

# params
def p_params(p):
	'params : IDENTIFIER COMMA params'
	p[0] = [p[1]] + p[3]
def p_params_one(p):
	'params : IDENTIFIER'
	p[0] = [p[1]]

# compoundstmt
def p_compoundstmt(p):
	'compoundstmt : LBRACE stmts RBRACE'
	p[0] = p[2]

# stmts
def p_stmts(p):
	'stmts : sstmt stmts'
	p[0] = [p[1]] + p[2]
def p_stmts_empty(p):
	'stmts : '
	p[0] = [ ]

# stmt_or_compound
def p_stmt_or_compound(p):
	'stmt_or_compound : sstmt'
	p[0] = [p[1]]
def p_stmt_or_compound_c(p):
	'stmt_or_compound : compoundstmt'
	p[0] = p[1]

#optsemi
def p_optsemi_none(p):
	'optsemi : '
	p[0] = [ ]
def p_optsemi_semicolon(p):
	'optsemi : SEMICOLON'
	p[0] = p[0]

# sstmt
def p_sstmt_if(p):
	'sstmt : IF exp stmt_or_compound optsemi'
	p[0] = ("if", p[2], p[3])
def p_sstmt_while(p):
	'sstmt : WHILE exp compoundstmt optsemi'
	p[0] = ("while", p[2], p[3])
def p_sstmt_if_else(p):
	'sstmt : IF exp compoundstmt ELSE stmt_or_compound optsemi'
	p[0] = ("if-else", p[2], p[3], p[5])
def p_sstmt_assigment(p):
	'sstmt : IDENTIFIER EQUAL exp SEMICOLON'
	p[0] = ("assign", p[1], p[3])
def p_sstmt_return(p):
	'sstmt : RETURN exp SEMICOLON'
	p[0] = ("return", p[2])
def p_sstmt_define(p):
	'sstmt : DEFINE IDENTIFIER EQUAL exp SEMICOLON'
	p[0] = ("define", p[2], p[4])
def p_sstmt_exp(p):
	'sstmt : exp SEMICOLON'
	p[0] = ("exp", p[1])

# exp
def p_exp_identifier(p):
	'exp : IDENTIFIER'
	p[0] = ("identifier", p[1])
def p_exp_paren(p):
	'exp : LPAREN exp RPAREN'
	p[0] = p[2]
def p_exp_number(p):
	'exp : NUMBER'
	p[0] = ("number", p[1])
def p_exp_true(p):
	'exp : TRUE'
	p[0] = ("true", p[1])
def p_exp_false(p):
	'exp : FALSE'
	p[0] = ("false", p[1])
def p_exp_not(p):
	'exp : NOT exp'
	p[0] = ("not", p[2])
def p_exp_binop(p):
	'''exp : exp PLUS exp
		| exp MINUS exp
		| exp TIMES exp
		| exp MOD exp
		| exp POWER exp
		| exp DIVIDE exp
		| exp EQUEQU exp
		| exp NOTEQU exp
		| exp LE exp
		| exp LT exp
		| exp GE exp
		| exp GT exp
		| exp ANDAND exp
		| exp OROR exp'''
	p[0] = ("binop", p[1], p[2], p[3])
def p_exp_call(p):
	'exp : IDENTIFIER LPAREN optargs RPAREN'
	p[0] = ("call", p[1], p[3])

# optargs
def p_optargs(p):
	'optargs : args'
	p[0] = p[1]
def p_optargs_empty(p):
	'optargs : '
	p[0] = [ ]

# args
def p_args(p):
	'args : exp COMMA args'
	p[0] = [p[1]] + p[3]
def p_args_one(p):
	'args : exp'
	p[0] = [p[1]]

# error
def p_error(p):
	if p:
		print "Syntax error at",
		print p.value,
		print "in line",
		print p.lineno
	else:
		print "Syntax error at EOF"
		exit(1)