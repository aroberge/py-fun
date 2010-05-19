# From http://compilers.iecc.com/crenshaw/tutor1.txt

import sys

# program name is not needed in Python
'''
program Cradle;

{--------------------------------------------------------------}
{ Constant Declarations }

const TAB = ^I;

{--------------------------------------------------------------}
{ Variable Declarations }

var Look: char;              { Lookahead Character }
'''
CURRENT_CHAR = None
PROGRAM = None

# Entering relevant function definitions

'''
{--------------------------------------------------------------}
{ Read New Character From Input Stream }

procedure GetChar;
begin
   Read(Look);
end;
'''
def get_char():
    global PROGRAM
    char = PROGRAM[0]
    PROGRAM = PROGRAM[1:]
    return char
'''

{--------------------------------------------------------------}
{ Report an Error }

procedure Error(s: string);
begin
   WriteLn;
   WriteLn(^G, 'Error: ', s, '.');
end;
'''
def report_error(s):
    print("Error %s." % s)


'''

{--------------------------------------------------------------}
{ Report Error and Halt }

procedure Abort(s: string);
begin
   Error(s);
   Halt;
end;
'''

def abort(s):
    report_error(s)
    sys.exit()

'''

{--------------------------------------------------------------}
{ Report What Was Expected }

procedure Expected(s: string);
begin
   Abort(s + ' Expected');
end;
'''
def report_and_quit(s):
    abort(s + ' Expected')

'''
{--------------------------------------------------------------}
{ Match a Specific Input Character }

procedure Match(x: char);
begin
   if Look = x then GetChar
   else Expected('''' + x + '''');
end;
'''
def match_char(c):
    global CURRENT_CHAR
    if CURRENT_CHAR == c:
        get_char()
    else:
        report_and_quit('=== %s ===' % c)

'''

{--------------------------------------------------------------}
{ Recognize an Alpha Character }

function IsAlpha(c: char): boolean;
begin
   IsAlpha := upcase(c) in ['A'..'Z'];
end;

'''
# isalpha and isdigit are builtin string methods
'''
{--------------------------------------------------------------}

{ Recognize a Decimal Digit }

function IsDigit(c: char): boolean;
begin
   IsDigit := c in ['0'..'9'];
end;

{--------------------------------------------------------------}
{ Get an Identifier }

function GetName: char;
begin
   if not IsAlpha(Look) then Expected('Name');
   GetName := UpCase(Look);
   GetChar;
end;
'''
def get_name():
    global CURRENT_CHAR
    if not CURRENT_CHAR.isalpha():
        report_and_quit('Name')
    get_char()


'''
{--------------------------------------------------------------}
{ Get a Number }

function GetNum: char;
begin
   if not IsDigit(Look) then Expected('Integer');
   GetNum := Look;
   GetChar;
end;

'''
def get_number():
    global CURRENT_CHAR
    if not CURRENT_CHAR.isdigit():
        report_and_quit("Integer")
    get_char()

'''
{--------------------------------------------------------------}
{ Output a String with Tab }

procedure Emit(s: string);
begin
   Write(TAB, s);
end;
'''
def emit(s):
    print "\t%s" % s,

'''

{--------------------------------------------------------------}
{ Output a String with Tab and CRLF }

procedure EmitLn(s: string);
begin
   Emit(s);
   WriteLn;
end;
'''
def emit_line(s):
    emit(s)
    print

'''
{--------------------------------------------------------------}
{ Initialize }

procedure Init;
begin
   GetChar;
end;
'''
def init():
    get_char()
'''

{--------------------------------------------------------------}
{ Main Program }

begin
   Init;
end.
{--------------------------------------------------------------}
'''
if __name__ == "__main__":
    PROGRAM = sys.argv[1]
    print PROGRAM
    init()