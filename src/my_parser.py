from nodes import (
    ArgsNode,
    BinOpExprNode,
    ElseIfStmtNode,
    ExprNode,
    FuncCallNode,
    FuncStmtNode,
    IfStmtNode,
    ParenExprNode,
    StatementListNode,
    StatementNode,
    UniExprNode,
    WhileNode,
    ExprStmtNode
)
from ply import yacc
import lexer

tokens = lexer.tokens

precedence = (
    ("right", "EQ"),
    ("left", "EQEQ", "GE", "LE", "GT", "LT"),
    ("left", "OR", "AND"),
    ("left", "PLUS"),
    ("left", "MUL", "DIV"),
    ("right", "NEG"),
    ("right", "POW"),
    ("nonassoc", "LPAREN", "RPAREN"),
)
start = "stmt_list_opt"


def p_while_stmt(p):
    """
    while_stmt : WHILE expr stmt_list END
    """
    p[0] = WhileNode(p[2], p[3])


def p_stmt_list(p):
    """
    stmt_list : stmt
              | stmt_list stmt
    """
    if len(p) == 2:
        p[0] = StatementListNode([p[1]])
    elif len(p) == 3:
        p[0] = StatementListNode(p[1].statements + [p[2]])


def p_stmt(p):
    """
    stmt : expr_stmt
         | if_stmt
         | while_stmt
         | BREAK
         | CONTINUE
         | function_stmt
    """
    p[0] = StatementNode(p[1])

def p_expr_stmt(p):
    """
    expr_stmt : expr SEMI
    """
    p[0] = ExprStmtNode(p[1])
    

def p_function_stmt(p):
    """
    function_stmt : FUNCTION ID EQ function_declr stmt_list END
    """
    p[0] = FuncStmtNode(p[2], p[4], p[5])

def p_function_declr(p):
    """
    function_declr : ID LPAREN args_opt RPAREN
    """
    p[0] = FuncCallNode(p[1], p[3])

def p_args_opt(p):
    """
    args_opt : 
            | args 
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ArgsNode()


def p_args(p):
    """
    args : ID 
        | args COMMA ID
    """
    if len(p) == 2:
        p[0] = ArgsNode([p[1]])
    else:
        p[0] = ArgsNode(p[1].args + [p[3]])

def p_stmt_list_opt(p):
    """
    stmt_list_opt :
                  | stmt_list
    """
    if len(p) == 1:
        p[0] = StatementListNode()
    else:
        p[0] = StatementListNode(p[1].statements)


def p_parens_expr(p):
    """
    expr : LPAREN expr RPAREN
    """
    p[0] = ParenExprNode(p[2])


def p_expr(p):
    """
    expr : function_call
    | ID
    | NUMBER
    | STRING
    | expr1
    | expr2
    """
    p[0] = ExprNode(p[1])

def p_function_call(p):
    """
    function_call : ID LPAREN expr_list_opt RPAREN 
    """
    p[0] = FuncCallNode(p[1], p[3])

def p_expr_args_opt(p):
    """
    expr_list_opt : 
                | expr_list
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ArgsNode()


def p_expr_args(p):
    """
    expr_list : expr
            | expr_list COMMA expr
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ArgsNode()


def p_expr1(p):
    """expr1 : NEG expr"""
    p[0] = UniExprNode(p[2], p[1])


def p_expr2(p):
    """expr2 : expr LT expr
    | expr AND expr
    | expr DIV expr
    | expr POW expr
    | expr GE expr
    | expr GT expr
    | expr LE expr
    | expr MINUS expr
    | expr MUL expr
    | expr OR expr
    | expr PLUS expr
    | expr EQ expr
    | expr EQEQ expr
    """
    p[0] = BinOpExprNode(p[1], p[2], p[3])


def p_if_stmt(p):
    """
    if_stmt : IF expr stmt_list_opt elseif_stmt END
    """
    p[0] = IfStmtNode(p[2], p[3], p[4])


def p_elseif_stmt(p):
    """
    elseif_stmt :
                | ELSE stmt_list_opt
                | ELSEIF expr stmt_list_opt elseif_stmt
    """
    if len(p) == 1:
        p[0] = ElseIfStmtNode()
    elif len(p) == 3:
        p[0] = ElseIfStmtNode(stmt_list=p[2])
    else:
        print(p[:])
        p[0] = ElseIfStmtNode(p[2], p[3], p[4])


def p_error(p):
    if p:
        print(
            "Syntax error at line {0}: {1} , '{2}'!".format(p.lineno, p.type, p.value)
        )
    else:
        print("Unexpected end of data")


parser = yacc.yacc()
