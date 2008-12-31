'''adapted from a function posted as a comment on the recipe at
http://code.activestate.com/recipes/65212/
'''

def base_convert(n, base):
    """convert decimal integer n to equivalent string in another base (2-36)"""
    if base < 2 or base > 36:
        raise NotImplementedError

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    sign = ''

    if n == 0:
        return '0'
    elif n < 0:
        sign = '-'
        n = -n

    s = ''
    while n != 0:
        r = n % base
        s = digits[r] + s
        n = n // base
    return sign + s

if __name__ == "__main__":
    for j in range(2, 37):
        assert base_convert(j, j) == '10'
        assert base_convert(j+1, j) == '11'
        assert base_convert(j*j, j) == '100'
        assert base_convert(j*j + 1, j) == '101'
        assert base_convert(-j, j) == '-10'
    assert base_convert(-8, 2) == '-1000'
    assert base_convert(5, 3) == '12'
    assert base_convert(255, 16) == 'ff'
    assert base_convert(0, 7) == '0'
    print "Done!"