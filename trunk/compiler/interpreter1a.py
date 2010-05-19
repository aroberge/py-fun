
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

program = [['PUSH', 1], ['PUSH', 2], ['ADD']]
interp = Interpreter()
interp.run(program)
interp.final_output()
