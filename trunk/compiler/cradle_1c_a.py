# Inspired from http://compilers.iecc.com/crenshaw/tutor1.txt

class Stack(object):
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        try:
            return self.items.pop()
        except IndexError:
            print("Attempted to pop element from empty stack.")
            raise

class ParserCompiler(object):

    def __init__(self, program):
        self.program = program
        self.compiled_program = []
        self.current_char = None
        self.current_char_index = 0
        self.stack = Stack()

    def run(self):
        try:
            self.parse_expression()
        except SyntaxError:
            pass  # will simply quit

    def parse_expression(self):
        n = self.get_term()
        if self.next_char() == '+':
            self.get_char()
            self.add()
        elif self.next_char() == '-':
            self.get_char()
            self.sub()
        else:
            self.abort("Operator + or -")

    def get_term(self):
        n = self.get_integer()
        self.stack.push(n)

    def get_integer(self):
        n = self.get_char()
        if n is None or not n.isdigit():
            self.abort(expected="Integer")
        return int(n)

    def get_char(self):
        try:
            self.current_char = self.program[self.current_char_index]
            self.current_char_index += 1
        except (TypeError, IndexError):
            self.current_char = None
        return self.current_char

    def next_char(self):
        try:
           next = self.program[self.current_char_index]
        except (TypeError, IndexError):
            next = None
        return next

    def abort(self, expected=None, err=None):
        print("====== Aborting =======")
        if expected is not None:
            print(expected + " expected.")
        if err is not None:
            print("Error: %s." % err)
        raise SyntaxError

    def add(self):
        self.get_term()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.compiled_program.append(['PUSH', n1])
        self.compiled_program.append(['PUSH', n2])
        self.compiled_program.append(['ADD'])

    def sub(self):
        self.get_term()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.compiled_program.append(['PUSH', n1])
        self.compiled_program.append(['PUSH', n2])
        self.compiled_program.append(['SUB'])

if __name__ == "__main__":
    import sys
    p = ParserCompiler(sys.argv[1])
    p.run()
    for line in p.compiled_program:
        print(line)