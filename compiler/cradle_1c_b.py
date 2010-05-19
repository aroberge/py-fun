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

class Interpreter(object):
    def __init__(self):
        self.dispatch = {'ADD': self.add,
                         'SUB': self.subtract,
                         'MUL': self.multiply,
                         'DIV': self.divide,
                         'POP': self.pop,
                         'PUSH': self.push}
        self.aborted = True

    def add(self):
        '''removes top two items from stack, adds them and leaves the
        results as new top item on stack'''
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.push(a+b)

    def subtract(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.push(a-b)

    def multiply(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.push(a*b)

    def divide(self):
        '''integer division'''
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.push(a//b)

    def pop(self):
        self.stack.pop()

    def push(self, item):
        self.stack.push(item[0])

    def run(self, program):
        self.stack = Stack()
        self.aborted = False
        try:
            for line in program:
                instruction = line[0]
                args = line[1:]
                if args:
                    self.dispatch[instruction](args)
                else:
                    self.dispatch[instruction]()
        except IndexError:
            self.abort("Program terminated due to corrupted memory.")
        except KeyError:
            self.abort("Program terminated due to invalid "+
                       "program instruction: %s." % instruction)

    def abort(self, message):
        print(message)
        self.aborted = True

    def final_output(self):
        '''displays the result of the final calculation'''
        if self.aborted:
            return
        try:
            print("Result from program: %s" % self.stack.pop())
        except MemoryError, TypeError:
            print("Program has no output value.")

if __name__ == "__main__":
    import sys
    p = ParserCompiler(sys.argv[1])
    p.run()

    interp = Interpreter()
    interp.run(p.compiled_program)
    interp.final_output()
