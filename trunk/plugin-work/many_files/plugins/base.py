'''Simulated base plugin file; a real one will be used to
    1. find plugins
    2. ensure that their definitions are available to the main program
'''

OPERATORS = {}

def init_plugins(expression):
    '''simulated plugin initializer'''
    from plugins import op_1, op_2
    op_1.expression = expression
    op_2.expression = expression
    OPERATORS['+'] = op_1.operator_add_token
    OPERATORS['-'] = op_1.operator_sub_token
    OPERATORS['*'] = op_1.operator_mul_token
    OPERATORS['/'] = op_1.operator_div_token
    OPERATORS['**'] = op_2.operator_pow_token