# From http://compilers.iecc.com/crenshaw/tutor1.txt

import sys

# program name is not needed in Python

class Stack(object):
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def last(self):
        return self.items[-1]

class Parser(object):

    def __init__(self, program):
        self.program = program
        print self.program
        self.current_char = None
        self.stack = Stack()

    def get_factor(self):
        self.stack.push(int(self.get_number()))

    def expression(self):
        self.get_term()
        while self.get_char() in ['+', '-']:
            if self.current_char == '+':
                self.add()
            elif self.current_char == '-':
                self.subtract()
            else:
                self.report_and_quit("Addop")
        if self.current_char is not None:
            self.report_and_quit("Addop")
        print self.stack.pop()

    def get_term(self):
        self.get_factor()
        while self.get_char() in ['*', '/']:
            if self.current_char == '*':
                self.multiply()
            elif self.current_char == '/':
                self.divide()
            else:
                self.report_and_quit("Mulop")
        self.put_back_char()

    def add(self):
        self.get_term()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.stack.push(n1+n2)

    def subtract(self):
        self.get_term()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.stack.push(n2-n1)

    def multiply(self):
        self.get_factor()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.stack.push(n1*n2)

    def divide(self):
        self.get_factor()
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        self.stack.push(n2/n1)

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

    def abort(self, err):
        '''report error and quit'''
        print "=====Aborting======"
        print("Error: %s." % err)
        sys.exit()

    def report_and_quit(self, err):
        self.abort(err + " expected")

    def get_name(self):
        n = self.get_char()
        if n is None or not n.isalpha():
            self.report_and_quit('Name')

    def get_number(self):
        n = self.get_char()
        if n is None or not n.isdigit():
            self.report_and_quit("Integer")
        return n

    def emit(self, s):
        print "\t%s" % s,

    def emit_line(self, s):
        self.emit(s)
        print

if __name__ == "__main__":
    parser = Parser(sys.argv[1])
    parser.expression()