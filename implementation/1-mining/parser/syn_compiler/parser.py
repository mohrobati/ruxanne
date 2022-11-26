from cmath import pi
from ply import yacc
from .lexer import Lexer
from .nonTerminal import NonTerminal


class Parser:
    tokens = Lexer().tokens

    def __init__(self):
        self.dictTree_string = None
        self.dictTree = None

    def p_program(self, p):
        """program : arr_list_root"""
        p[0] = NonTerminal()
        p[0].value = p[1].value
        self.dictTree_string = p[0].__str__()
        self.dictTree = p[0].value

    def p_arr_list_root_with_id(self, p):
        """arr_list_root : ID LSB obj_list RSB"""
        p[0] = NonTerminal()
        p[0].value = {p[1]: p[3].value}

    def p_arr_list_root_without_id(self, p):
        """arr_list_root : LSB obj_list RSB"""
        p[0] = NonTerminal()
        p[0].value = p[2].value

    def p_obj_list_root(self, p):
        """obj_list_root : ID LRB obj_list RRB"""
        p[0] = NonTerminal()
        p[0].value = {p[1]: p[3].value}

    def p_obj_list_obj_list(self, p):
        """obj_list : obj_list obj_element COMMA"""
        p[0] = NonTerminal()
        if p[1].value:
            if type(p[1].value) is not list:
                p[1].value = [p[1].value]
            if type(p[2].value) is not list:
                p[2].value = [p[2].value]
            p[0].value = p[1].value + p[2].value
        else:
            p[0].value = p[2].value

    def p_obj_list_lambda(self, p):
        """obj_list : """
        p[0] = NonTerminal()

    def p_obj_list_paran(self, p):
        """obj_list : LRB obj_list RRB COMMA"""
        p[0] = NonTerminal()
        p[0].value = p[2].value

    def p_obj_element_atomic(self, p):
        """obj_element : atomic"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_dic_list_root(self, p):
        """dic_list_root : ID LCB dic_list RCB"""
        p[0] = NonTerminal()
        p[0].value = {p[1]: p[3].value}

    def p_dic_list_dic_list(self, p):
        """dic_list : dic_list dic_element COMMA"""
        p[0] = NonTerminal()
        if p[1].value:
            p[1].value.update(p[2].value)
            p[0].value = p[1].value
        else:
            p[0].value = p[2].value

    def p_dic_list_lambda(self, p):
        """dic_list : """
        p[0] = NonTerminal()

    def p_dic_element(self, p):
        """dic_element : ID COLON dic_value"""
        p[0] = NonTerminal()
        p[0].value = {p[1]: p[3].value}

    def p_dic_value_id(self, p):
        """dic_value : atomic"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_dic_value_string(self, p):
        """dic_value : STRING"""
        p[0] = NonTerminal()
        p[0].value = p[1]

    def p_dic_value_arr_list_root(self, p):
        """dic_value : arr_list_root"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_dic_value_obj_list_root(self, p):
        """dic_value : obj_list_root"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_dic_value_dic_list_root(self, p):
        """dic_value : dic_list_root"""
        p[0] = NonTerminal()
        p[0].value = p[1].value

    def p_obj_element_arr_list_root(self, p):
        """obj_element : arr_list_root"""
        p[0] = NonTerminal()
        p[0].value = [p[1].value]

    def p_obj_element_obj_list_root(self, p):
        """obj_element : obj_list_root"""
        p[0] = NonTerminal()
        p[0].value = [p[1].value]

    def p_obj_element_dic_list_root(self, p):
        """obj_element : dic_list_root"""
        p[0] = NonTerminal()
        p[0].value = [p[1].value]

    def p_atomic(self, p):
        """atomic : ID"""
        p[0] = NonTerminal()
        p[0].value = p[1]

    def p_error(self, p):
        raise Exception('ParsingError: invalid grammar at ', p)

    precedence = (

    )

    def build(self, **kwargs):
        """build the parser"""
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
