'''Simulated base plugin file; a real one will be used to
    1. find plugins
    2. ensure that their definitions are available to the main program

In this example, we import known objects residing in separate python files
explicitly specified by name.
In a true plugin system, we would import arbitrary objects residing in
arbitrarily named files.

'''

OPERATORS = {}

def init_plugins(expression):
    '''simulated plugin initializer'''
    from plugins import op_1, op_2

    # Note that, in the original single file program, "expression" was used
    # as a globally known object.  Since we simply extracted some classes
    # that used "expression" into separate modules, we need to ensure that
    # "expression" is globally defined there as well
    op_1.expression = expression
    op_2.expression = expression

    OPERATORS['+'] = op_1.operator_add_token
    OPERATORS['-'] = op_1.operator_sub_token
    OPERATORS['*'] = op_1.operator_mul_token
    OPERATORS['/'] = op_1.operator_div_token
    OPERATORS['**'] = op_2.operator_pow_token