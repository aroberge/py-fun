'''number crunching for the 17x17 grid problem'''

import sys

powers_of_two = [2**i for i in range(17)]




levin = """11110000000000000
00001111000000000
10001000000010001
10000100001000100
10000010100001000
10000001010100010
01001000000001010
01000100010000001
01000010001100000
01000001100010100
00101000000100100
00100100100000010
00100010010010000
00100001001001001
00011000111000000
00010100000111000
00010010000000111"""

rows_s = levin.split("\n")
for row in rows_s:
    print(row)

sys.exit()

def count_bits(x):
    '''counts the number of bits
    see http://stackoverflow.com/questions/407587/python-set-bits-count-popcount
    for reference and other alternative'''
    return bin(x).count('1')

def rectangles_for_two_rows(row_1, row_2):
    '''returns 0 if two rows (given colour, encoded as a bit string)
        do not form a rectangle -
        otherwise returns the points in common encoded as a bit string'''
    intersect = row_1 & row_2
    if not intersect:   # no point in common
        return 0
    # perhaps there is only one point in common of the form 000001000000...
    if not(intersect & (intersect-1)):
        return 0
    else:
        return intersect


# Assume that the highest 5 bits are set to 1 for colour 3; how many
# configurations can we have with 4 points of the same colour for
# each of the remaining 3 colours?
# The answer should be  (12!)/(4! 4! 4!) = 34650.
fours=[]
for i in range(2**12):
    if count_bits(i) == 4:
        fours.append(i)

print(len(fours))

configurations = []
for i in fours:
    for j in fours:
        if not (i&j):
            for k in fours:
                if not (i&k):
                    if not (j&k):
                        configurations.append((i, j, k))

assert len(configurations) == 34650

pick = configurations[0]
nb_valid = 0
for conf in configurations:
    rectangle=False
    for i in (0, 1, 2):
        if rectangles_for_two_rows(pick[i], conf[i]):
            rectangle=True
            break
    if not rectangle:
        nb_valid += 1

print(nb_valid)
