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

    def get_factor(self):
        self.stack.push(self.get_integer())

    def run(self):
        '''parses and compiles the program'''
        try:
            self.expression()
        except SyntaxError:
            pass  # will simply quit

    def expression(self):
        self.get_term()
        while self.get_char() in ['+', '-']:
            if self.current_char == '+':
                self.add()
            elif self.current_char == '-':
                self.subtract()
            else:
                self.abort("Addop")
        if self.current_char is not None:
            self.abort("Addop")

    def get_term(self):
        self.get_factor()
        while self.get_char() in ['*', '/']:
            if self.current_char == '*':
                self.multiply()
            elif self.current_char == '/':
                self.divide()
            else:
                self.abort("Mulop")
        self.put_back_char()

    def add(self):
        self.get_term()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.compiled_program.append(['PUSH', n1])
        self.compiled_program.append(['PUSH', n2])
        self.compiled_program.append(['ADD'])


    def subtract(self):
        self.get_term()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.compiled_program.append(['PUSH', n1])
        self.compiled_program.append(['PUSH', n2])
        self.compiled_program.append(['SUB'])

    def multiply(self):
        self.get_factor()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.compiled_program.append(['PUSH', n1])
        self.compiled_program.append(['PUSH', n2])
        self.compiled_program.append(['MUL'])

    def divide(self):
        self.get_factor()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.compiled_program.append(['PUSH', n1])
        self.compiled_program.append(['PUSH', n2])
        self.compiled_program.append(['DIV'])

    def get_char(self):
        try:
            self.current_char = self.program[0]
            self.program = self.program[1:]
        except (TypeError, IndexError):
            self.current_char = None
            self.program = None
        return self.current_char

    def put_back_char(self):
        if self.current_char is not None:
            self.program = self.current_char + self.program

    def get_integer(self):
        n = self.get_char()
        if n is None or not n.isdigit():
            self.abort(expected="Integer")
        return int(n)

    def abort(self, expected=None, err=None):
        print("====== Aborting =======")
        if expected is not None:
            print(expected + " expected.")
        if err is not None:
            print("Error: %s." % err)
        raise SyntaxError


if __name__ == "__main__":
    import sys
    p = ParserCompiler(sys.argv[1])
    p.run()
    for line in p.compiled_program:
        print(line)