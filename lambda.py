from lark import Lark, Transformer


class ToDictTransformer(Transformer):
    def programm(self, s):
        return s

    def expr(self, s):
        return s
    
    def infix(self, s):
        return {'infix': s[1], 'arguments': [s[0], s[2]]}

    def infix_operator(self, s):
        return str(s[0])

    def OPERATOR(self, s):
        return {'operator': str(s)}

    def bracket_expr(self, s):
        return s[0]

    def lambd(self, s):
        return {'lambda': {'arguments': s[0], 'body': s[1]}}

    def body(self, s):
        return s

    def assign(self, s):
        return {'assign': {'variable': s[0], 'arguments': s[1], 'expr': s[2]}}

    def arguments(self, s):
        return list(s)

    def NAME(self, s):
        return {'name': str(s)}

    def var_name(self, s):
        return {'var_name': s[0]}

    def number(self, s):
        return {'number': float(str(s[0]))}

    def value(self, s):
        return {'value': s[0]}

    def strict_varname(self, s):
        return str(s[0])

    def dotted_varname(self, s):
        if len(s) == 1:
            return {'dotted_varname': [s[0]]}
        return {'dotted_varname': [s[0]] + s[1]['dotted_varname']}

    def import_(self, s):
        return {'import': s[0]}


def main() -> None:
    parser = Lark.open('lambda.lark', parser='lalr', start='programm', rel_to=__file__)

    with open('programm.l', 'r') as file:
        programm = file.read()

    tree = parser.parse(programm)

    print(tree.pretty())
    print('---')
    
    new_tree = ToDictTransformer().transform(tree)
    [print(t, '\n') for t in new_tree]

    print('\n', new_tree[5])


if __name__ == '__main__':
    main()
