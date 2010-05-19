# Inspired from http://compilers.iecc.com/crenshaw/tutor1.txt

class ReadSingleCharacter(object):

    def __init__(self, program):
        self.program = program
        self.current_char_index = 0

    def translate(self):
        try:
            char = self.get_char()
            print("The program is: %s" % char)
        except SyntaxError:
            print("This program has a syntax error.")

    def get_char(self):
        try:
            self.current_char = self.program[self.current_char_index]
        except IndexError:
            self.abort("Attempted to read a non-existent character.")
        self.current_char_index += 1
        return self.current_char

    def abort(self, message):
        print(message)
        raise SyntaxError



if __name__ == "__main__":
    import sys
    p = ReadSingleCharacter(sys.argv[1])
    p.run()