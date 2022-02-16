import ply.lex as lex
import re


reserved = {
    "else": "ELSE",
    "elseif": "ELSEIF",
    "if": "IF",
    "while": "WHILE",
    "end": "END",
    "break": "BREAK",
    "continue": "CONTINUE",
    "function": "FUNCTION"
}

tokens = [
    "AND",
    "OR",
    "NEG",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "POW",
    "EQ",
    "EQEQ",
    "GT",
    "GE",
    "LT",
    "LE",
    "RPAREN",
    "LPAREN",
    "SEMI",
    "NUMBER",
    "NEWLINE",
    "COMMA",
    "ID",
    "STRING"
] + list(reserved.values())

t_ignore = " \t"
t_STRING = r"\"([^\\\n]|(\\.))*?\""
t_AND = r"\&"
t_DIV = r"\/"
t_NEG = r"\~|\!"
t_EQ = r"="
t_EQEQ = r"=="
t_GE = r">="
t_GT = r"\>"
t_LE = r"<="
t_LT = r"\<"
t_MINUS = r"\-"
t_MUL = r"\*"
t_POW = r"\^"
t_OR = r"\|"
t_PLUS = r"\+"
t_COMMA = r","


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_LPAREN(t):
    r"\("
    t.lexer.parens += 1
    return t


def t_RPAREN(t):
    r"\)"
    t.lexer.parens -= 1
    return t


@lex.TOKEN(r"\;") 
def t_SEMI(t):
    t.lexer.lineno += t.value.count("\n")
    return t


def t_NUMBER(t):
    r"(0x[0-9A-Fa-f]+)|((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?[ij]?)"
    if t.value[-1] == "i":
        t.value = t.value[:-1] + "j"
    t.value = str(t.value)
    return t


def t_NEWLINE(t):
    r"\n"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex(reflags=re.MULTILINE)
lexer.brackets = 0  
lexer.parens = 0 
lexer.braces = 0 
