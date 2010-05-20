import unittest
import reeborg
import mock

class TestLineOfCode(unittest.TestCase):

    def test_line_of_code(self):
        line = reeborg.LineOfCode('a', 0)
        self.assertEqual(line.line_number, 0)
        self.assertEqual(line.indentation,  0)
        self.assertEqual(line.content, "a")

    def test_line_of_code_remove_commments(self):
        line = reeborg.LineOfCode(' ab#cd', 3)
        self.assertEqual(line.line_number, 3)
        self.assertEqual(line.indentation, 1)
        self.assertEqual(line.content, "ab")

        line = reeborg.LineOfCode('   #cd', 2)
        self.assertEqual(line.indentation, 3)
        self.assertEqual(line.content, "")

        line = reeborg.LineOfCode('# #  ', 0)
        self.assertEqual(line.indentation, 0)
        self.assertEqual(line.content, "")

        line = reeborg.LineOfCode('"#" #  ', 0)
        self.assertEqual(line.indentation, 0)
        self.assertEqual(line.content, '"#" ')

        line = reeborg.LineOfCode('says("# aren\'t #") # numbers are not numbers', 0)
        self.assertEqual(line.indentation, 0)
        self.assertEqual(line.content, 'says("# aren\'t #") ')

class TestUserProgram(unittest.TestCase):

    def test_next_line(self):
        program = reeborg.UserProgram("a")
        line = reeborg.LineOfCode("a", 0)
        self.assertEqual(program.next_line(), line)
        program.previous_line()
        self.assertEqual(program.next_line(), line)

        program = reeborg.UserProgram("b\na #ignore\nc")
        line = reeborg.LineOfCode("a ", 1)
        program.next_line()
        self.assertEqual(program.next_line(), line)


class TestBlock(unittest.TestCase):

    def test_single_line(self):
        program = reeborg.UserProgram("move()")
        block = reeborg.Block(program)
        self.assertEqual(block.lines[0].name, "move")
        self.assertEqual(block.lines[0].type, "command")
        self.assertEqual(program.syntax_error, None)

        program = reeborg.UserProgram("wrong")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "Unknown command: wrong"])

    def test_single_line_french(self):
        program = reeborg.UserProgram("avance()", language="fr")
        block = reeborg.Block(program)
        self.assertEqual(block.lines[0].name, "move")
        self.assertEqual(program.syntax_error, None)

        program = reeborg.UserProgram("wrong", language="fr")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "Commande inconnue: wrong"])

    def test_two_lines(self):
        program = reeborg.UserProgram("move()\nturn_left()")
        block = reeborg.Block(program)
        self.assertEqual(block.lines[0].name, "move")
        self.assertEqual(block.lines[1].name, "turn_left")
        self.assertEqual(block.lines[0].type, "command")
        self.assertEqual(block.lines[1].type, "command")
        self.assertEqual(program.syntax_error, None)

        program = reeborg.UserProgram("move()\nwrong")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [1, "Unknown command: wrong"])

    def test_allow_spaces_with_command_parentheses(self):
        program = reeborg.UserProgram("move (  \t)  ")
        block = reeborg.Block(program)
        self.assertEqual(block.lines[0].name, "move")
        self.assertEqual(block.lines[0].type, "command")
        self.assertEqual(program.syntax_error, None)

    def test_two_lines_french(self):
        program = reeborg.UserProgram("avance()\ntourne_a_gauche()", language="fr")
        block = reeborg.Block(program)
        self.assertEqual(block.lines[0].name, "move")
        self.assertEqual(block.lines[1].name, "turn_left")
        self.assertEqual(program.syntax_error, None)

        program = reeborg.UserProgram("avance()\nwrong", language="fr")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [1, "Commande inconnue: wrong"])

    def test_indentation(self):
        program = reeborg.UserProgram("move()\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [1, "Indentation error"])

        program = reeborg.UserProgram("  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "Indentation error"])

        program = reeborg.UserProgram("def a():\nmove()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [1, "Indentation error"])

    def test_blank_line(self):
        program = reeborg.UserProgram("move()\n\nmove()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

### TODO  add test with space between parentheses for method def i.e. def m(  )

    def test_def(self):
        p = "def turn_around():\n  turn_left()\n  turn_left()\nturn_around()"
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

        self.assertEqual(block.lines[0].method_name, "turn_around")
        self.assertEqual(block.lines[0].type, "def block")

        self.assertEqual(block.lines[1].name, "turn_around")

        sub_block = block.lines[0].block
        self.assertEqual(sub_block.lines[0].name, "turn_left")
        self.assertEqual(sub_block.lines[1].name, "turn_left")

        p = "def    mm()    :\n  move()\n  move()\nmm()"
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

        program = reeborg.UserProgram("def :\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, 'Syntax error: bad method name or missing colon.'])

        program = reeborg.UserProgram("def m()\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, 'Syntax error: bad method name or missing colon.'])

    def test_def_not_allowed(self):
        program = reeborg.UserProgram("def move():\n  turn_left()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "Attempt to redefine 'move'"])

        program = reeborg.UserProgram("def m():\n  move()\ndef m():\n move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [2, "Attempt to redefine 'm'"])

    def test_assignment_builtin(self):
        program = reeborg.UserProgram("mo = move\nmo()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

        program = reeborg.UserProgram("m = move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "Syntax error: 'm = move()'"])

        program = reeborg.UserProgram("move = turn_left")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "Attempt to redefine 'move'"])

        program = reeborg.UserProgram("m() = move")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "Syntax error: 'm() = move'"])

        program = reeborg.UserProgram("m = a")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "Unknown command: a()"])

    def test_assignment_method(self):
        program = reeborg.UserProgram("def m2():\n move()\n move()\nmm=m2\nmm()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

        program = reeborg.UserProgram("def m2():\n move()\n move()\nm2 = move")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [3, "Attempt to redefine 'm2'"])

    def test_assignment_true(self):
        program = reeborg.UserProgram("t = True")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_assignment_true_if_with_not(self):
        program = reeborg.UserProgram("vrai = True\nif not vrai:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        self.assertEqual(block.lines[1].type, "if block")
        self.assertEqual(block.lines[1].condition, True)

    def test_assignment_false(self):
        program = reeborg.UserProgram("t = False")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_assignment_condition(self):
        program = reeborg.UserProgram("t = on_beeper")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_assignment_condition_if_with_not(self):
        program = reeborg.UserProgram("t=on_beeper\nif not t():\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        self.assertEqual(block.lines[1].type, "if block")
        self.assertEqual(block.lines[1].condition, "on_beeper()")
        self.assertEqual(block.lines[1].negate_condition, True)

    def test_if_true(self):
        program = reeborg.UserProgram("if True:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        self.assertEqual(block.lines[0].type, "if block")
        self.assertEqual(block.lines[0].condition, True)

        program = reeborg.UserProgram("if     True     :    \n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        self.assertEqual(block.lines[0].type, "if block")
        self.assertEqual(block.lines[0].condition, True)

    def test_if_false(self):
        program = reeborg.UserProgram("if False:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        self.assertEqual(block.lines[0].type, "if block")
        self.assertEqual(block.lines[0].condition, False)

    def test_if_on_beeper(self):
        program = reeborg.UserProgram("if on_beeper():\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        self.assertEqual(block.lines[0].type, "if block")
        self.assertEqual(block.lines[0].condition, "on_beeper()")

    def test_if_on_beeper_with_spaces(self):
        program = reeborg.UserProgram("if on_beeper ( \t ) : \n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        self.assertEqual(block.lines[0].type, "if block")
        self.assertEqual(block.lines[0].condition, "on_beeper()")
        self.assertEqual(block.lines[0].negate_condition, False)

    def test_if_not_on_beeper(self):
        program = reeborg.UserProgram("if not on_beeper():\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        self.assertEqual(block.lines[0].type, "if block")
        self.assertEqual(block.lines[0].condition, "on_beeper()")
        self.assertEqual(block.lines[0].negate_condition, True)

    def test_if_invalid(self):
        program = reeborg.UserProgram("if invalid:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error,
                         [0, "Invalid test condition: 'invalid'"])

    def test_elif_true(self):
        program = reeborg.UserProgram("if True:\n move()\nelif True:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_if_true_else(self):
        program = reeborg.UserProgram("if True:\n move()\nelse:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_elif_missing_if(self):
        program = reeborg.UserProgram("elif True:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "'elif' or 'else' without matching 'if'"])

    def test_elif_false(self):
        program = reeborg.UserProgram("if True:\n move()\nelif False:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

        program = reeborg.UserProgram("if True:\n move()\nelif True:\n  move()\nelif     False     :    \n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

        p = """if False:
    turn_left()
elif False:
    turn_left()
elif True:
    move()"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_elif_invalid(self):
        program = reeborg.UserProgram("if True:\n move()\nelif invalid:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error,
                         [2, "Invalid test condition: 'invalid'"])

    def test_if_else_syntax_error(self):
        p = """\
if True:
    turn_left()
else: move()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [2, 'Unknown command: else: move()'])

    def test_while(self):
        program = reeborg.UserProgram("while True:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_while_on_beeper(self):
        program = reeborg.UserProgram("while on_beeper():\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_while_on_beeper_with_spaces(self):
        program = reeborg.UserProgram("while on_beeper ( ) :\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_while_invalid(self):
        program = reeborg.UserProgram("while invalid:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error,
                         [0, "Invalid test condition: 'invalid'"])

    def test_break(self):
        program = reeborg.UserProgram("break")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [0, "SyntaxError: 'break' outside loop"] )

    def test_while_break(self):
        program = reeborg.UserProgram("while True:\n  break")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_break_outside_while(self):
        program = reeborg.UserProgram("if True:\n  break")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, [1, "SyntaxError: 'break' outside loop"])

    def test_while_if_break(self):
        program = reeborg.UserProgram("while True:\n  if True:\n     break")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_while_if_elif_break(self):
        p = """\
while True:
    if False:
        move()
    elif True:
        break
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_while_if_else_break(self):
        p = """\
while True:
    if False:
        move()
    else:
        break
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

    def test_pass(self):
        program = reeborg.UserProgram("pass")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)

class TestMockBlockRunner(unittest.TestCase):

    def test_move(self):
        program = reeborg.UserProgram("move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0])

    def test_pass(self):
        program = reeborg.UserProgram("pass")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, [])
        self.assertEqual(runner.lines_executed, [0])

    def test_method(self):
        p = "def turn_around():\n  turn_left()\n  turn_left()\nturn_around()"
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["turn_left()", "turn_left()"])
        self.assertEqual(runner.lines_executed, [0, 3, 1, 2])

        p = "def t2():\n  turn_left()\n  turn_left()\nt2()\nt2()"
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["turn_left()", "turn_left()",
                                         "turn_left()", "turn_left()"])
        self.assertEqual(runner.lines_executed, [0, 3, 1, 2, 4, 1, 2])

    def test_assignment_builtin(self):
        program = reeborg.UserProgram("m=move\nm()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0, 1])

    def test_assignment_method(self):
        program = reeborg.UserProgram("def m2():\n move()\n move()\nmm=m2\nmm()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()", "move()"])
        self.assertEqual(runner.lines_executed, [0, 3, 4, 1, 2])

    def test_blank_line(self):
        program = reeborg.UserProgram("move()\n\nmove()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()", "move()"])
        self.assertEqual(runner.lines_executed, [0, 2])

    def test_if_true(self):
        program = reeborg.UserProgram("if True:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0, 1])

    def test_if_not_true(self):
        program = reeborg.UserProgram("if not True:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, [])
        self.assertEqual(runner.lines_executed, [0])

    def test_if_true_twice(self):
        program = reeborg.UserProgram("if True:\n  move()\nif True:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()", "move()"])
        self.assertEqual(runner.lines_executed, [0, 1, 2, 3])

    def test_if_true_if_false(self):
        program = reeborg.UserProgram("if True:\n  move()\nif False:\n  turn_left()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0, 1, 2])

    def test_if_false(self):
        program = reeborg.UserProgram("if False:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, [])
        self.assertEqual(runner.lines_executed, [0])

    def test_if_not_false(self):
        program = reeborg.UserProgram("if not False:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0, 1])

    def test_if_on_beeper_true(self):
        program = reeborg.UserProgram("if on_beeper():\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, [True])
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0, 1])

    def test_if_on_beeper_with_spaces_true(self):
        program = reeborg.UserProgram("if on_beeper (\t ) \t :\n  move(\t  )")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, [True])
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0, 1])

    def test_if_on_beeper_true_false(self):
        p = """\
if on_beeper():
    move()
if on_beeper():
    turn_left()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, [True, False])
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0, 1, 2])

    def test_if_on_beeper_false(self):
        program = reeborg.UserProgram("if on_beeper():\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, [False])
        self.assertEqual(runner.output, [])
        self.assertEqual(runner.lines_executed, [0])

    def test_if_false_elif_true(self):
        program = reeborg.UserProgram("if False:\n  move()\nelif True:\n turn_left()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["turn_left()"])
        self.assertEqual(runner.lines_executed, [0, 2, 3])

    def test_if_false_elif_on_beeper_true(self):
        program = reeborg.UserProgram("if False:\n  move()\nelif on_beeper():\n turn_left()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, [True])
        self.assertEqual(runner.output, ["turn_left()"])
        self.assertEqual(runner.lines_executed, [0, 2, 3])

    def test_if_false_elif_on_beeper_false(self):
        program = reeborg.UserProgram("if False:\n  move()\nelif on_beeper():\n turn_left()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, [False])
        self.assertEqual(runner.output, [])
        self.assertEqual(runner.lines_executed, [0, 2])

    def test_if_false_elif_false(self):
        program = reeborg.UserProgram("if False:\n  move()\nelif False:\n turn_left()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, [])
        self.assertEqual(runner.lines_executed, [0, 2])

    def test_if_true_elif_true(self):
        program = reeborg.UserProgram("if True:\n  move()\nelif True:\n turn_left()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()"])
        self.assertEqual(runner.lines_executed, [0, 1, 2])

    def test_if_false_elif_false_then_true(self):
        p = """\
if False:
    turn_left()
elif False:
    turn_left()
elif True:
    move()"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.lines_executed, [0, 2, 4, 5])
        self.assertEqual(runner.output, ["move()"])

    def test_if_true_else(self):
        p="""\
if True:
    move()
else:
    turn_left()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.lines_executed, [0, 1, 2])
        self.assertEqual(runner.output, ["move()"])

    def test_if_false_else(self):
        p="""\
if False:
    move()
else:
    turn_left()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.lines_executed, [0, 2, 3])
        self.assertEqual(runner.output, ["turn_left()"])

    def test_if_false_elif_false_else(self):
        p = """\
if False:
    turn_left()
elif False:
    turn_left()
else:
    move()"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.lines_executed, [0, 2, 4, 5])
        self.assertEqual(runner.output, ["move()"])

    def test_while_on_beeper(self):
        program = reeborg.UserProgram("while on_beeper():\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, fake_tests=[True, True, False])
        self.assertEqual(runner.output, ["move()", "move()"])
        self.assertEqual(runner.lines_executed, [0, 0, 1, 0, 1, 0])

    def test_while_on_beeper_with_spaces(self):
        program = reeborg.UserProgram("while on_beeper ( )  :\n  move(\t)")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, fake_tests=[True, True, False])
        self.assertEqual(runner.output, ["move()", "move()"])
        self.assertEqual(runner.lines_executed, [0, 0, 1, 0, 1, 0])

    def test_break(self):
        p = """\
while True:
    move()
    move()
    break
    turn_left()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.lines_executed, [0, 0, 1, 2, 3])
        self.assertEqual(runner.output, ["move()", "move()"])

    def test_break_with_if(self):
        p = """\
while True:
    move()
    if True:
        move()
        break
    turn_left()
    move()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.lines_executed, [0, 0, 1, 2, 3, 4])
        self.assertEqual(runner.output, ["move()", "move()"])

    def test_break_with_many_levels(self):
        p = """\
while True:
    move()
    if True:
        move()
        if True:
            move()
            break
    turn_left()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()", "move()", "move()"])
        self.assertEqual(runner.lines_executed, [0, 0, 1, 2, 3, 4, 5, 6])

    def test_break_with_many_levels_2(self):
        p = """\
while True:
    move()
    if True:
        move()
        if True:
            move()
            if True:
                break
    turn_left()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()", "move()", "move()"])
        self.assertEqual(runner.lines_executed, [0, 0, 1, 2, 3, 4, 5, 6, 7])

    def test_embedded_while(self):
        p = """\
while True:
    move()
    while True:
        move()
        break
        turn_left()
    move()
    break
    turn_left()
"""
        program = reeborg.UserProgram(p)
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block)
        self.assertEqual(runner.output, ["move()", "move()", "move()"])
        self.assertEqual(runner.lines_executed, [0, 0, 1, 2, 2, 3, 4, 6, 7])

    def test_max_instructions(self):
        program = reeborg.UserProgram("while True:\n  move()")
        block = reeborg.Block(program)
        self.assertEqual(program.syntax_error, None)
        runner = mock.MockBlockRunner(block, [], 7)
        self.assertEqual(runner.output, ['move()', 'move()', 'move()', 'Too many instructions.'])
        self.assertEqual(runner.lines_executed, [0, 0, 1, 0, 1, 0, 1, 0])

if __name__ == '__main__':
    unittest.main()