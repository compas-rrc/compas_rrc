"""
expr := <aggregate> | <literal>
literal := <bool_literal>
        | <num_literal>
        | <string_literal>
aggregate := "[" <expr> {"," <expr> } "]"
"""
import decimal

from compas_rrc.parsers import ParserException
from compas_rrc.parsers.ply.lex import lex
from compas_rrc.parsers.ply.yacc import yacc

tokens = (
    "COMMA",
    "LBRACKET",
    "RBRACKET",
    "INTEGER",
    "HEX_INTEGER",
    "OCT_INTEGER",
    "BIN_INTEGER",
    "FLOAT",
    "STRING",
    "BOOL",
    "ZERO",
)
t_COMMA = r"\,"
t_ZERO = r"0"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_INTEGER = r"(\+|-)?[1-9]\d*([Ee][\+-]?\d+)?"
# t_INTEGER = r"(\+|-)?\d+([Ee][\+-]?\d+)?"
t_BIN_INTEGER = r"0(B|b)[01]+"
t_OCT_INTEGER = r"0(O|o)[0-8]+"
t_HEX_INTEGER = r"0(X|x)[0-9A-Fa-f]+"
t_FLOAT = r"(\+|-)?(\d*\.\d+)([Ee][\+-]?\d+)?"
t_STRING = r"\".*?\""
t_BOOL = r"(FALSE|TRUE)"

t_ignore = " \t"


def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


def p_expr(p):
    """expr : literal
    | aggregate"""
    p[0] = p[1]


def p_aggregate(p):
    """aggregate : LBRACKET RBRACKET
    | LBRACKET aggregate_list RBRACKET
    """
    if len(p) == 3:
        p[0] = []  # empty list
    else:
        p[0] = p[2]


def p_aggregate_list(p):
    """aggregate_list : aggregate_list COMMA expr
    | expr
    """
    if len(p) == 4:
        p[0] = list(p[1]) + [p[3]]
    else:
        p[0] = [p[1]]


def p_literal(p):
    """literal : int_literal
    | hex_literal
    | oct_literal
    | bin_literal
    | float_literal
    | bool_literal
    | string_literal"""
    p[0] = p[1]


def p_int_literal(p):
    """int_literal : INTEGER
    | ZERO"""
    p[0] = int(decimal.Decimal(p[1]))


def p_hex_literal(p):
    """hex_literal : HEX_INTEGER"""
    p[0] = int(p[1], 16)


def p_oct_literal(p):
    """oct_literal : OCT_INTEGER"""
    p[0] = int(p[1], 8)


def p_bin_literal(p):
    """bin_literal : BIN_INTEGER"""
    p[0] = int(p[1], 2)


def p_float_literal(p):
    """float_literal : FLOAT"""
    p[0] = float(decimal.Decimal(p[1]))


def p_bool_literal(p):
    """bool_literal : BOOL"""
    p[0] = p[1] == "TRUE"


def p_string_literal(p):
    """string_literal : STRING"""
    p[0] = p[1][1:-1]


def p_error(p):
    if not p:
        raise ParserException("Syntax error at End-of-File")

    raise ParserException("Syntax error at {}".format(p))


lexer = lex()
parser = yacc()
