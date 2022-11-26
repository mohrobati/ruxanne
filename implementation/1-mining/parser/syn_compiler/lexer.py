from ply import lex


class Lexer:
    tokens = [
        'LRB', 'RRB', 'LSB', 'RSB', 'LCB', 'RCB',
        'ID', 'STRING', 'COLON', 'COMMA'
    ]
    t_COLON = r':'
    t_COMMA = r','
    t_LRB = r'\('
    t_RRB = r'\)'
    t_LSB = r'\['
    t_RSB = r'\]'
    t_LCB = r'\{'
    t_RCB = r'\}'

    # def t_ERROR(self, t):
    #     r"""([-|+]?(\d+)([a-zA-Z_]+))"""
    #     raise Exception('SyntaxError: invalid syntax at ', t)


    def t_STRING(self, t):
        r'r\#(("(\\"|[^\#])*")|(\'(\\\'|[^\#])*\'))\# | r(("\\(\\"|[^"])*\\")|(\'\\(\\\'|[^\'])*\\\')) | (b|r)?(("(\\\\|\\"|[^"])*")|(\'(\\\\|\\\'|[^\'])*\'))'
        # r'r\#(("(\\"|[^\#])*")|(\'(\\\'|[^\#])*\'))\#  | (b|r)?(("(\\"|[^"])*")|(\'(\\\'|[^\'])*\'))'

        return t

    def t_ID(self, t):
        r'[a-zA-Z_0-9\.]+'
        return t


    def t_error(self, t):
        raise Exception('SyntaxError: invalid syntax at ', t.value[0])

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = '\n \t\r\f\v'

    def build(self, **kwargs):
        '''
        build the lexer
        '''
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
