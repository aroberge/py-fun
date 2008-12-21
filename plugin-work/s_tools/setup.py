''' run with python setup.py develop '''

from setuptools import setup, find_packages

setup(
    name="Calculator_s_tools",
    version="1.0",
    packages=['plugins'],
    entry_points="""
        [plugin_tutorial.s_tools]
        add = plugins.op_1:operator_add_token
        sub = plugins.op_1:operator_sub_token
        mul = plugins.op_1:operator_mul_token
        div = plugins.op_1:operator_div_token
        pow = plugins.op_2:operator_pow_token"""
    )