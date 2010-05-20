# -*- coding: utf-8 -*-

import re

_builtins = {
    "en": {"move()": "move",
           "turn_left()": "turn_left",
           },
    "fr": {"avance()": "move",
           "tourne_a_gauche()": "turn_left"
           },
}

_conditions = {
    "on_beeper()": "on_beeper()",
    "True": True,
    "False": False
}

_messages = {
    "en": {"Unknown command": "Unknown command: %s",
           "Indentation error": "Indentation error",
           "Attempt to redefine": "Attempt to redefine '%s'",
           "Syntax error": "Syntax error: '%s'",
           "Invalid test condition": "Invalid test condition: '%s'",
           "Missing if": "'elif' or 'else' without matching 'if'",
           "break outside loop": "SyntaxError: 'break' outside loop",
           "def syntax error": "Syntax error: bad method name or missing colon."
           },
    "fr": {"Unknown command": "Commande inconnue: %s",
           "Indentation error": "Erreur d'indentation",
           "Attempt to redefine": "Tentative de redéfinir '%s'",
           "Syntax error": "Erreur de syntaxe: '%s'",
           "Invalid test condition": "Condition non valide: '%s'",
           "Missing if": "'elif' ou 'else' sans le 'if' correspondant",
           "break outside loop": "Erreur de syntaxe: 'break' à l'extérieur d'une boucle",
           "def syntax error": "Erreur de syntaxe: mauvais nom de méthode ou 'deux points'."
           },
}

assignment_pattern = re.compile("^(\w*)\s*=\s*(\w*)\s*$")
comment_pattern = re.compile("(?!(\'|\")*#.*(\'|\")\s*)#.*")
def_pattern = re.compile("def \s*(.*)\(\s*\)\s*:\s*")
elif_pattern = re.compile("elif (.*):\s*")
if_pattern = re.compile("if (.*):\s*")
indentation_pattern = re.compile("( *)(.*)")
while_pattern = re.compile("while (.*):\s*")

def remove_spaces(text):
    ''' removes all spurious spaces in text so that something like
       "move  (  \t  )  "   can be correctly interpreted as
       "move()"
    '''
    return text.replace(" ", '').replace("\t",'')

# A program can be thought as a series of blocks; each block is composed
# of one or more lines that have the same indentation.
# Each line has a line number, an indentation, and it may have a meaningful
# content and/or contain a comment.
# A comment starts with "#" and includes everything until the end of the line.

class LineOfCode(object):
    '''single line of code in user's program'''
    def __init__(self, raw_content, line_number):
        self.line_number = line_number
        if "#" in raw_content:   # strip comment
            raw_content = comment_pattern.sub('', raw_content)
        match = indentation_pattern.search(raw_content)
        self.indentation = len(match.group(1))
        self.content = match.group(2)
        self.stripped_content = remove_spaces(self.content)
        # The following will be initialized by the parser
        self.name = None
        self.block = None
        self.type = None
        self.condition = None

    def __eq__(self, other):
        '''equality defined to simplify some tests'''
        return ( (self.line_number == other.line_number) and
                 (self.indentation == other.indentation) and
                 (self.content == other.content))

class UserProgram(object):
    def __init__(self, program, language="en"):
        lines = program.split("\n")
        self.lines = []
        self.nb_lines = len(lines)
        self.language = language
        self.index = 0
        for index, line in enumerate(lines):
            self.lines.append(LineOfCode(line, index))
        self.builtins = _builtins[language]
        #
        self.syntax_error = None
        self.user_methods = {}

    def next_line(self):
        if self.index >= self.nb_lines:
            return None
        self.current_line = self.lines[self.index]
        self.index += 1
        return self.current_line

    def previous_line(self):
        self.index -= 1

    def abort_parsing(self, msg):
        self.syntax_error = [self.index-1, msg]


class Block(object):
    def __init__(self, program, min_indentation=-1, inside_loop=False):
        self.lines = []
        self.program = program
        self.min_indentation = min_indentation
        self.block_indentation = None
        self.inside_loop = inside_loop
        self.parse()

    def parse(self):
        self.previous_line_content = None
        while self.program.syntax_error is None:
            self.current_line = self.program.next_line()
            if self.current_line is None:      # end of program
                break
            if not self.handle_indentation():
                break

            self.block_indentation = self.current_line.indentation
            if self.current_line.stripped_content in self.program.builtins:
                self.current_line.name = self.program.builtins[self.current_line.stripped_content]
                self.current_line.type = "command"
            elif self.current_line.content in self.program.user_methods:
                self.current_line.type = "user method"
                method_def_line = self.program.user_methods[self.current_line.content]
                self.current_line.name = method_def_line.method_name
                self.current_line.block = method_def_line.block
            elif self.current_line.stripped_content == "pass":
                self.current_line.type = "pass"
            elif self.current_line.content.startswith("def "):
                self.parse_def()
            elif self.current_line.content.startswith("if "):
                self.parse_if()
            elif self.current_line.content.startswith("elif "):
                self.parse_elif()
            elif self.current_line.stripped_content == "else:":
                self.parse_else()
            elif self.current_line.content.startswith("while"):
                self.parse_while()
            elif self.current_line.stripped_content == "break":
                if self.inside_loop:
                    self.current_line.type = "break"
                else:
                    self.program.abort_parsing(_messages[self.program.language
                                                    ]["break outside loop"])
            elif "=" in self.current_line.content:
                self.parse_assignment()
            elif not self.current_line.content: # empty line
                self.current_line.type = "empty line"
            else:
                self.program.abort_parsing(_messages[self.program.language
                                                     ]["Unknown command"
                                                       ] % self.current_line.content)
                break
            self.lines.append(self.current_line)
            self.previous_line_content = self.current_line.content

    def handle_indentation(self):
        if self.block_indentation is None:   # begin new block
            return self.set_indentation()
        elif self.current_line.indentation <= self.min_indentation:  # end block
            self.program.previous_line()
            return False
        elif self.current_line.indentation != self.block_indentation:
            self.program.abort_parsing(_messages[self.program.language
                                             ]["Indentation error"])
            return False
        return True

    def set_indentation(self):
        if self.current_line.indentation <= self.min_indentation:
            self.program.abort_parsing(_messages[self.program.language
                                                 ]["Indentation error"])
            return False
        elif self.min_indentation == -1 and self.current_line.indentation != 0:
            self.program.abort_parsing(_messages[self.program.language
                                                 ]["Indentation error"])
        else:
            self.block_indentation = self.current_line.indentation
            return True

    def parse_def(self):
        self.current_line.type = "def block"
        match = def_pattern.search(self.current_line.content)
        try:
            name = match.group(1)
        except AttributeError:
            self.program.abort_parsing(_messages[self.program.language
                                                 ]["def syntax error"])
            return
        if (name+"()" in self.program.builtins or
            name+"()" in self.program.user_methods):
            self.program.abort_parsing(_messages[self.program.language
                                                 ]["Attempt to redefine"]% name)
        self.current_line.method_name = name
        self.program.user_methods[name+"()"] = self.current_line
        self.current_line.block = Block(self.program,
                                         min_indentation=self.current_line.indentation)

    def normalize_condition(self, condition):
        '''ensures that the test condition is a valid one'''
        if condition.startswith("not "):
            self.current_line.negate_condition = True
            condition = condition[4:]
        else:
            self.current_line.negate_condition = False

        if condition in _conditions:
            self.current_line.condition = _conditions[condition]
            return condition

        stripped_condition = remove_spaces(condition)
        if stripped_condition in _conditions:
            self.current_line.condition = _conditions[stripped_condition]
            return stripped_condition

        self.program.abort_parsing(_messages[self.program.language][
                                          "Invalid test condition"]% condition)
        return None

    def parse_if(self):
        self.current_line.type = "if block"
        match = if_pattern.search(self.current_line.content)
        condition = match.group(1).strip()
        condition = self.normalize_condition(condition)
        if condition is not None:
            self.current_line.block = Block(self.program,
                                    min_indentation=self.current_line.indentation,
                                    inside_loop=self.inside_loop)

    def parse_elif(self):
        if not (self.previous_line_content is not None and
                    (self.previous_line_content.startswith("if ") or
                    self.previous_line_content.startswith("elif "))):
            self.program.abort_parsing(_messages[self.program.language
                                            ]["Missing if"])
            return
        self.current_line.type = "elif block"
        match = elif_pattern.search(self.current_line.content)
        condition = match.group(1).strip()
        condition = self.normalize_condition(condition)
        if condition is not None:
            self.current_line.block = Block(self.program,
                                    min_indentation=self.current_line.indentation,
                                    inside_loop=self.inside_loop)

    def parse_else(self):
        if not (self.previous_line_content.startswith("if ") or
                self.previous_line_content.startswith("elif ")):
            self.program.abort_parsing(_messages[self.program.language
                                            ]["Missing if"])
            return
        self.current_line.type = "else block"
        content = self.current_line.content.replace(" ", "")
        self.current_line.block = Block(self.program,
                                    min_indentation=self.current_line.indentation,
                                    inside_loop=self.inside_loop)

    def parse_while(self):
        self.current_line.type = "while block"
        match = while_pattern.search(self.current_line.content)
        condition = match.group(1).strip()

        condition = self.normalize_condition(condition)
        if condition is not None:
            self.current_line.block = Block(self.program,
                                    min_indentation=self.current_line.indentation,
                                    inside_loop=True)

    def parse_assignment(self):
        '''parses a statement like "a = b" '''
        match = assignment_pattern.search(self.current_line.content)
        if match is None:
            self.program.abort_parsing(_messages[self.program.language
                                                 ]["Syntax error"
                                                   ]%self.current_line.content)
            return
        left = match.group(1)
        right = match.group(2)
        self.current_line.type = "assignment"
        if (left+"()" in self.program.builtins  or
            left+"()" in self.program.user_methods):
            self.program.abort_parsing(_messages[self.program.language
                                                 ]["Attempt to redefine"]% left)
        elif right+"()" in self.program.builtins:
            self.program.builtins[left+"()"] = self.program.builtins[right+"()"]
        elif right+"()" in self.program.user_methods:
            self.program.user_methods[left+"()"] = self.program.user_methods[right+"()"]
        else:
            self.program.abort_parsing(_messages[self.program.language
                                                     ]["Unknown command"
                                                       ] % right+"()")
