#!/usr/bin/python3

import collections  # for named tuple && Counter (multisets)
import re  # for regex
from enum import IntEnum # for enumerations (enum from C)
import logging # for logging functions

##########################################################################
# auxiliary definitions
class OperatorType(IntEnum):

    """Enumeration of operator types, ordered by precedence in calculus"""

    left_brace   = 1
    # right brace is never added to the postfix stack
    add          = 2
    subtract     = 3
    multiply     = 4
    divide       = 5
    power        = 6

# end class OperatorType

# tuple used to describe parsed data
Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

##########################################################################
# class definitions

class NumericalPsystem():

    """Numerical P systems class"""

    def __init__(self):
        self.H = [] # array of strings (names of membranes)
        self.membranes = {} # map (dictioanry) between String membrane_name: Membrane object
        self.structureString = "" # [1 [2 ]2 ]1

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
        self.prodFunction = None # ProductionFunction object
        self.distribFunction = None # DistributionFunction object

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

class ProductionFunction():

    """Production function class that stores expressions using the postfix (reversed polish) form"""

    def __init__(self):
        self.postfixStack = [] # stack of operands and operators (auxiliary for postfix form)
        self.items = [] # list of operands and operators written in postfix (reverse polish) form

# end class ProductionFunction

class DistributionFunction(list):

    """Distribution function class (list of distribution rules)"""

    def __init__(self):
        """Initialize the underling list used to store rules"""
        list.__init__(self)
# end class DistributionFunction

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

    def __init__(self, name = '', value = 0):
        self.name = name
        self.value = value
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
        ('NUMBER_FLOAT',  r'\d+\.\d+'),    # Float number
        ('NUMBER',        r'\d+'),         # Integer number
        ('ASSIGN',        r'='),           # Assignment operator '='
        ('END',           r';'),           # Statement terminator ';'
        ('ID',            r'[\w]+'),       # Identifiers
        ('L_BRACE',       r'\('),          # Left brace '('
        ('R_BRACE',       r'\)'),          # Right brace ')'
        ('L_CURLY_BRACE', r'{'),           # Left curly brace '{'
        ('R_CURLY_BRACE', r'}'),           # Right curly brace '}'
        ('L_BRACKET', r'\['),              # Left bracket (straight brace) '['
        ('R_BRACKET', r'\]'),              # Right bracket (straight brace) ']'
        ('COLUMN',        r','),           # column ','

        ('PROD_DISTRIB_SEPARATOR', r'->'), # Program production and distribution component separator sign '->'
        ('OPERATOR_ADD', r'\+'),          # Addition operator (+)
        ('OPERATOR_SUBTRACT', r'\-'),         # Subtraction operator (-)
        ('OPERATOR_MULTIPLY', r'\*'),      # Multiplication operator (*)
        ('OPERATOR_DIVIDE', r'\/'),        # Division operator (/)
        ('OPERATOR_POWER', r'\^'),         # Power operator (^)
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

def process_tokens(tokens, parent, index):
    """Process tokens recurently and return a P system structure (or a subcomponent of the same type as parent)

    :tokens: the list of tokens to be processed
    :parent: an object that represents the type of the result
    :index: the start index in the list of tokens
    :returns: index - the current index in the token list (after finishing this component)
    :returns: result - an object that is the result of processing the input parent and tokens """

    logging.debug("process_tokens (parent_type = %s, index = %d)" % (type(parent), index))
    result = parent # construct the result of specified type
    prev_token = tokens[index]
    # for processing distribution rules
    distribRule = None

    while (index < len(tokens)):
        token = tokens[index]
        logging.debug("token = '%s'" % token.value)

        if (type(parent) == NumericalPsystem):
            logging.debug("processing as NumericalPsystem")

            if (token.type == 'ASSIGN'):
                if (prev_token.value == 'H'):
                    logging.info("building membrane list");
                    index, result.H = process_tokens(tokens, list(), index + 1);
                    print(result.H)

                # if the prev_token is the name of a membrane
                elif (prev_token.value in result.H):
                    logging.info("building Membrane");
                    index, result.membranes[prev_token.value] = process_tokens(tokens, Membrane(), index + 1);

                else:
                    raise RuntimeError("Unexpected token '%s' on line %d" % (prev_token.value, prev_token.line))
        # end if parent == NumericalPsystem

        elif (type(parent) == Membrane):
            logging.debug("processing as Membrane")

            if (token.type == 'ASSIGN'):
                if (prev_token.value == 'var'):
                    logging.info("building variable list");
                    index, variables = process_tokens(tokens, list(), index + 1);
                    for var in variables:
                        result.variables.append(Pobject(name = var))

                elif (prev_token.value == 'pr'):
                    logging.info("building Program");
                    index, program = process_tokens(tokens, Program(), index + 1);
                    result.programs.append(program)

                elif (prev_token.value == 'var0'):
                    logging.info("building var0 list");
                    index, variables = process_tokens(tokens, list(), index + 1);
                    for i, var in enumerate(variables):
                        result.variables[i].value = var

                else:
                    raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))
        # end if parent == Membrane

        elif (type(parent) == Program):
            logging.debug("processing as Program")

            if (token.type == 'L_CURLY_BRACE'):
                logging.info("building production function");
                index, prodFunction = process_tokens(tokens, ProductionFunction(), index + 1);
                result.prodFunction = prodFunction

            elif (token.type == 'PROD_DISTRIB_SEPARATOR'):
                logging.info("building distribution rule");
                index, result.distribFunction = process_tokens(tokens, DistributionFunction(), index + 1);

            elif (token.type == 'R_CURLY_BRACE'):
                logging.info("finished this Program with result = %s" % result)
                return index, result;

            elif (token.type == 'END'):
                logging.info("finished this block with result = %s" % result)
                return index, result;

            else:
                raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))
        # end if parent == Program

        elif (type(parent) == ProductionFunction):
            logging.debug("processing as ProductionFunction")

            if (token.type == 'NUMBER'):
                logging.debug("processing integer number")
                result.items.append(int(token.value))

            elif (token.type == 'NUMBER_FLOAT'):
                logging.debug("processing float number")
                result.items.append(float(token.value))

            elif (token.type == 'ID'):
                logging.debug("processing variable")
                result.items.append(token.value) # store as string for now, reference to real P object later

            elif (token.type == 'L_BRACE'):
                logging.debug("processing operator %s" % token.value)
                # add the current operator to the postfix transformation
                result.postfixStack.append(OperatorType.left_brace)

            elif (token.type == 'R_BRACE'):
                logging.debug("processing operator %s" % token.value)
                # pop all elements in the stack up until the left brace and add them to the postfix form
                while (OperatorType.left_brace in result.postfixStack):
                    op = result.postfixStack.pop()
                    # append all popped operators except of left_brace
                    if (op != OperatorType.left_brace):
                        result.items.append(op)

            elif (token.type == 'OPERATOR_ADD'):
                logging.debug("processing operator %s" % token.value)
                # if there is an operator with precedence >= to that of the current operator, then pop the stack and insert it into the postfix transformation
                if (len(result.postfixStack) > 0 and result.postfixStack[-1] >= OperatorType.add):
                    result.items.append(result.postfixStack.pop())
                # add the current operator to the postfix transformation
                result.postfixStack.append(OperatorType.add)

            elif (token.type == 'OPERATOR_SUBTRACT'):
                logging.debug("processing operator %s" % token.value)
                # if there is an operator with precedence >= to that of the current operator, then pop the stack and insert it into the postfix transformation
                if (len(result.postfixStack) > 0 and result.postfixStack[-1] >= OperatorType.add):
                    result.items.append(result.postfixStack.pop())
                # add the current operator to the postfix transformation
                result.postfixStack.append(OperatorType.subtract)

            elif (token.type == 'OPERATOR_MULTIPLY'):
                logging.debug("processing operator %s" % token.value)
                # if there is an operator with precedence >= to that of the current operator, then pop the stack and insert it into the postfix transformation
                if (len(result.postfixStack) > 0 and result.postfixStack[-1] >= OperatorType.multiply):
                    result.items.append(result.postfixStack.pop())
                # add the current operator to the postfix transformation
                result.postfixStack.append(OperatorType.multiply)

            elif (token.type == 'OPERATOR_DIVIDE'):
                logging.debug("processing operator %s" % token.value)
                # if there is an operator with precedence >= to that of the current operator, then pop the stack and insert it into the postfix transformation
                if (len(result.postfixStack) > 0 and result.postfixStack[-1] >= OperatorType.multiply):
                    result.items.append(result.postfixStack.pop())
                # add the current operator to the postfix transformation
                result.postfixStack.append(OperatorType.divide)

            elif (token.type == 'OPERATOR_POWER'):
                logging.debug("processing operator %s" % token.value)
                # if there is an operator with precedence >= to that of the current operator, then pop the stack and insert it into the postfix transformation
                if (len(result.postfixStack) > 0 and result.postfixStack[-1] >= OperatorType.power):
                    result.items.append(result.postfixStack.pop())
                # add the current operator to the postfix transformation
                result.postfixStack.append(OperatorType.power)

            elif (token.type == 'PROD_DISTRIB_SEPARATOR'):
                logging.debug("production function end; emptying stack")
                # pop all elements in the stack
                while (len(result.postfixStack) > 0):
                    result.items.append(result.postfixStack.pop())
                logging.info("finished the production function with result = %s" % result.items)
                # the Program should also see PROD_DISTRIB_SEPARATOR in order to trigger the build of a distribution function
                return index-1, result;

            elif (token.type == 'L_CURLY_BRACE'):
                logging.debug("skipped left curly brace")
                # continue to next token
                prev_token = token;
                index += 1
                continue

            else:
                raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))
        # end if parent == ProductionFunction

        elif (type(parent) == DistributionFunction):
            logging.debug("processing as DistributionFunction")

            if (token.type == 'NUMBER'):
                # construct a new distribution rule
                distribRule = DistributionRule()
                distribRule.proportion = int(token.value)

            elif (token.type == 'ID' and prev_token.type == "DISTRIBUTION_SIGN"):
                # finalize the distribution rule
                distribRule.variable = token.value # store as string for now, reference later
                result.append(distribRule) # store the new distribution rule

            # is used to separate rules, not needed
            elif (token.type == 'OPERATOR_ADD' or token.type == "DISTRIBUTION_SIGN"):
                logging.debug("skipped '+' or '|'")
                # continue to next token
                prev_token = token;
                index += 1
                continue

            elif (token.type == 'R_CURLY_BRACE'):
                logging.info("finished this DistributionFunction with result = %s" % result)
                return index, result;

            else:
                raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))
        # end if parent == DistributionFunction

        elif (type(parent) == DistributionRule):
            logging.debug("processing as DistributionRule")

            if (token.type == 'R_CURLY_BRACE'):
                logging.info("finished this DistributionRule with result = %s" % result)
                return index, result;
        # end if parent == DistributionRule

        elif (type(parent) == list):
            logging.debug("processing as List")
            if (token.type == 'ID' or token.type == 'NUMBER'):
                result.append(token.value);

        elif (type(parent) == str):
            logging.debug("processing as Str")
            if (token.type == 'ID'):
                result = token.value;

        elif (type(parent) == int):
            logging.debug("processing as Int")
            if (token.type == 'NUMBER'):
                result = int(token.value);

        else:
            logging.debug("processing as GENERAL")
            # process the token generally
            if (token.type == 'ASSIGN'):
                logging.info("building NumericalPsystem")
                index, result = process_tokens(tokens, NumericalPsystem(), index + 1);

        if (token.type == 'END'):
            logging.info("finished this block with result = %s" % result)
            return index, result;

        prev_token = token;
        index += 1
    return index, result
#end process_tokens
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

    index, end_result = process_tokens(tokens, None, 0)

    #if (loglevel <= logging.warning):
        #print("\n\n");
        #if (type(end_result) == pswarm):
            #end_result.print_swarm_components(printdetails=true)
        #elif (type(end_result == pcolony)):
            #end_result.print_colony_components(printdetails=true)
        #print("\n\n");

    return end_result
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
