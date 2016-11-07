#!/usr/bin/python3

import collections  # for named tuple && Counter (multisets)
import re  # for regex
from enum import Enum # for enumerations (enum from C)
import logging # for logging functions
import random # for stochastic chosing of programs

##########################################################################
# auxiliary definitions

# tuple used to describe parsed data
Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

##########################################################################
# class definitions

class NumericalPsystem():

    """Numerical P systems class"""

    def __init__(self):
        membraneNames = [] # array of strings
        membranes = {} # map (dictioanry) between String membrane_name: Membrane object
        structureString = "" # [1 [2 ]2 ]1

# end class NumericalPsystem

class Membrane():

    """Membrane class, that can contain other membranes or be part of another membrane"""

    def __init__(self, parentMembrane = None):
        self.variables = [] # array of P objects
        self.programs = [] # list of Program objects

        self.enzymes = [] # array of P objects
        self.parent = parentMembrane # parent membrane (Membrane object)
        self.children = {} # map (dictioanry) between String membrane_name: Membrane object
# end class Membrane

class Program():

    """Program class"""

    def __init__(self):
        self.prodFunction = [] # list of ProductionRule objects
        self.distribFunction = [] # list of DistributionRule objects

    def print(self, indentSpaces = 2, toString = False) :
        """Print a program with a given indentation level

        :indentSpaces: number of spaces used for indentation
        :toString: write to a string instead of stdout
        :returns: string print of the rule if toString = True otherwise returns None """

        result = " " * indentSpaces

        # production section
        for prod in self.prodFunction:
            result += " " + prod.print(toString = True)

        result += " -> "

        # distribution section
        for i, distrib in enumerate(self.distribFunction):
            if (i == 0):
                result += distrib.print(toString = True)
            else:
                result += " + " + distrib.print(toString = True)

        if (toString):
            return result
        else:
            print(result)
    # end print()
# end class Program

class ProductionRule():

    """Class for the production rules that make up a program, together with the distribution rules
    The rules allow the use of the +, -, *, /"""

    def __init__(self):
        self.quantity = 0 # float value, used for 3x rules or 0.5x rules. The sign is also specified here
        self.exp = 1 # integer value, used for x^5 rules
        self.variable = None # P object

    def print(self, indentSpaces = 2, toString = False) :
        """Print a production rule with a given indentation level

        :indentSpaces: number of spaces used for indentation
        :toString: write to a string instead of stdout
        :returns: string print of the rule if toString = True otherwise returns None """

        # SIGN QUANTITY VAR_NAME EXP
        result = " " * indentSpaces + "%s%02f%s%s" % (
                "+" if self.quantity >= 0 else "-", # almost C style conditional ( value_if_true if CONDITION else value_if_false)
                self.quantity,
                self.variable.name,
                "^%d" % self.exp if self.exp != 1 else "" ) # almost C style conditional ( value_if_true if CONDITION else value_if_false)

        if (toString):
            return result
        else:
            print(result)
    # end print()
# end class ProductionRule

class DistributionRule():

    """Class for the distribution rules that make up a program, together with the production rules"""

    def __init__(self):
        self.proportion = 0 # integer number
        self.variable = None # P object

    def print(self, indentSpaces = 2, toString = False) :
        """Print a distribution rule with a given indentation level

        :indentSpaces: number of spaces used for indentation
        :toString: write to a string instead of stdout
        :returns: string print of the rule if toString = True otherwise returns None """

        # PROPORTION | VAR_NAME
        result = " " * indentSpaces + "%d|%s" % (
                self.proportion,
                self.variable.name)

        if (toString):
            return result
        else:
            print(result)
    # end print()
# end class DistributionRule

class Pobject():

    """Mutable objects that are needed in order to allow all membranes that use the P object to globally modify the object"""

    def __init__(self):
        self.name = ''
        self.value = 0
# end class Pobject


##########################################################################
# global variables

logLevel = logging.INFO

##########################################################################
# auxiliary functions

def tokenize(code):
    """ generate a token list of input text
        adapted from https://docs.python.org/3/library/re.html#writing-a-tokenizer"""
    token_specification = [
        ('NUMBER',        r'\d+'),         # Integer number
        ('ASSIGN',        r'='),           # Assignment operator '='
        ('END',           r';'),           # Statement terminator ';'
        ('ID',            r'[\w\.]+'),     # Identifiers
        ('L_BRACE',       r'\('),          # Left brace '('
        ('R_BRACE',       r'\)'),          # Right brace ')'
        ('L_CURLY_BRACE', r'{'),           # Left curly brace '{'
        ('R_CURLY_BRACE', r'}'),           # Right curly brace '}'
        ('L_BRACKET', r'\['),              # Left bracket (straight brace) '['
        ('R_BRACKET', r'\]'),              # Right bracket (straight brace) ']'
        ('COLUMN',        r','),           # column ','

        #order counts here (the more complex rules go first)
        ('PROD_DISTRIB_SEPARATOR', r'->'), # Program production and distribution component separator sign '->'
        ('MATH_OPERATOR', r'[\*\^\+\-]'),  # Math operators (+, -, *, ^)
        ('DISTRIBUTION_SIGN',    r'\|'),   # Distribution rule sign '|'

        ('NEWLINE',       r'\n'),          # Line endings
        ('COMMENT',       r'#'),           # Comment (anything after #, up to the end of the line is discarded)
        ('SKIP',          r'[ \t]+'),      # Skip over spaces and tabs
        ('MISMATCH',      r'.'),           # Any other character
    ]
    # join all groups into one regex expr; ex:?P<NUMBER>\d+(\.\d*)?) | ...
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    in_comment = False
    # iteratively search and return each match (for any of the groups)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup # last group name matched
        value = mo.group(kind) # the last matched string (for group kind)
        print("kind = %s, value = %s" % (kind, value))
        if kind == 'COMMENT':
            in_comment = True
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            in_comment = False # reset in_comment state
        elif kind == 'SKIP':
            pass
        elif (kind == 'MISMATCH') and (not in_comment):
            raise RuntimeError('%r unexpected on line %d' % (value, line_num))
        else:
            # skip normal tokens if in comment (cleared at the end of the line)
            if in_comment:
                continue
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)
#end tokenize()

def print_token_by_line(v):
    """Prints tokens separated by spaces on their original line (with line numbering)"""
    line_num = 0;
    for token in v:
        if (token.line > line_num):
            line_num = token.line;
            print('\n%d  ' % line_num, end='');

        print(token.value, end=" ");
# end print_token_by_line()

def readInputFile(filename, printTokens = False):
    """parses the given input file and produces a P system object

    :filename: string path to the file that will be parsed
    :returns: P system object"""

    logging.info("reading input file")

    with open(filename) as file_in:
        lines = "".join(file_in.readlines());

    # construct array of tokens for later use
    tokens = [token for token in tokenize(lines)];

    if (printTokens):
        print_token_by_line(tokens);
        print("\n\n");

    #index, end_result = process_tokens(tokens, none, 0)

    #if (loglevel <= logging.warning):
        #print("\n\n");
        #if (type(end_result) == pswarm):
            #end_result.print_swarm_components(printdetails=true)
        #elif (type(end_result == pcolony)):
            #end_result.print_colony_components(printdetails=true)
        #print("\n\n");

    #return end_result
# end readinputfile()

##########################################################################
#   MAIN

if (__name__ == "__main__"):
    import sys # for argv

    if ('--debug' in sys.argv or '-v' in sys.argv):
        logLevel = logging.DEBUG
    elif ('--error' in sys.argv or '-v0' in sys.argv):
        logLevel = logging.ERROR

    try:
        import colorlog # colors log output

        formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(levelname)-8s %(message)s %(reset)s",
                datefmt=None,
                reset=True,
                log_colors={
                        'DEBUG':    'cyan',
                        'INFO':     'green',
                        'WARNING':  'yellow',
                        'ERROR':    'red',
                        'CRITICAL': 'red,bg_white',
                },
                secondary_log_colors={},
                style='%'
        )

        colorlog.basicConfig(stream = sys.stdout, level = logLevel)
        stream = colorlog.root.handlers[0]
        stream.setFormatter(formatter);

    # colorlog not available
    except ImportError:
        logging.basicConfig(format='%(levelname)s:%(message)s', level = logLevel)

    if (len(sys.argv) < 2):
        logging.error("Expected input file path as parameter")
        exit(1)

    # step by step simulation
    step = False
    if ('--step' in sys.argv):
        step = True

    system = readInputFile(sys.argv[1], True)

    print("\n\n");
