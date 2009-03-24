from zope import interface

class IOperator(interface.Interface):
    """Defines an operator for the calculator"""
    
    lbp = interface.Attribute('lbp', 'The left binding power')
    
    def nud():
        """The null denotation value
        
        Basically, what the token returns if it's the first token in a chain"""
        
    def led(left):
        """The left denotation value
        
        What it returns when it gets applied the value to the left"""
