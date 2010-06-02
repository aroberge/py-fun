def on_beeper(tests=[]):
    return tests.pop()

class MockBlockRunner(object):
    def __init__(self, block, fake_tests=None, max_nb_instructions=1000):
        self.block = block
        self.if_branches = False
        self.break_loop = None
        self.max_nb_instructions = max_nb_instructions
        self.nb_instructions = 0
        # fake tests to simulate going through a loop a few times
        if fake_tests is None:
            self.fake_tests = []
        else:
            fake_tests.reverse()
            self.fake_tests = fake_tests
        # fake output stuff
        self.output = []
        self.lines_executed = []
        #
        try:
            self.execute_block(block)
        except RuntimeError:
            self.output.append("Too many instructions.")
        except AttributeError:
            print(self.output)
            print(self.lines_executed)
            raise

    def execute_block(self, block, parent=None):
        for line in block.lines:
            if self.break_loop:    # pop levels until find a loop to break
                if parent is not None:
                    parent.break_loop = True
                break

            if line.type == "empty line":
                continue

            self.highlight(line.line_number)
            if line.type in [ "def block", "assignment"]:
                continue
            elif line.type == "command":
                self.execute_command(line.name)
            elif line.type == "pass":
                pass
            elif line.type == "user method":
                self.execute_block(line.block, parent=self)
            elif line.type == "if block":
                self.handle_if(line)
            elif line.type == "elif block":
                self.handle_if_elif(line)
            elif line.type == "else block":
                if self.if_branches != "done":
                    self.execute_block(line.block, parent=self)
                    self.if_branches = "done"
            elif line.type == "break":
                parent.break_loop = True
                break
            elif line.type == "while block":
                self.handle_while(line)
            else:
                self.output.append("ERROR:" + line.content)


    def handle_if(self, line):
        self.if_branches = "started"
        self.handle_if_elif(line)

    def handle_if_elif(self, line):
        test_result = self.evaluate_condition(line)
        if test_result and self.if_branches != "done":
            self.execute_block(line.block, parent=self)
            self.if_branches = "done"

    def handle_while(self, line):
        while True:
            self.highlight(line.line_number)
            test_result = self.evaluate_condition(line)
            if test_result:
                self.execute_block(line.block, parent=self)
            else:
                break
            if self.break_loop:
                self.break_loop = None
                break

    def evaluate_condition(self, line):
        condition = line.condition
        if line.negate_condition:
            condition = not condition
        if condition == "on_beeper()":
            return on_beeper(self.fake_tests)
        else:
            return condition

    def execute_command(self, cmd):
        self.output.append(cmd+"()")

    def highlight(self, line_number):
        self.nb_instructions += 1
        self.lines_executed.append(line_number)
        if self.nb_instructions > self.max_nb_instructions:
            raise RuntimeError
