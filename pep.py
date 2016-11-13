#!/usr/bin/python3

import collections  # for named tuple && Counter (multisets)
import re  # for regex
from enum import IntEnum # for enumerations (enum from C)
import logging # for logging functions
import random # for stochastic chosing of programs
import time # for time.time()

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

dictOperatorTypes = {
        'OPERATOR_ADD': OperatorType.add,
        'OPERATOR_SUBTRACT': OperatorType.subtract,
        'OPERATOR_MULTIPLY': OperatorType.multiply,
        'OPERATOR_DIVIDE': OperatorType.divide,
        'OPERATOR_POWER': OperatorType.power}

# tuple used to describe parsed data
Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

##########################################################################
# class definitions

class NumericalPsystem():

    """Numerical P systems class"""

    def __init__(self):
        self.H = [] # array of strings (names of membranes)
        self.membranes = {} # map (dictioanry) between String membrane_name: Membrane object
        self.structure = None # MembraneStructure object (list of structural elements) [1 [2 ]2 ]1
        self.variables = [] # list of Pobjects that appear throughtout the P system

    def runSimulationStep(self):
        """Runs 1 simulation step consisting of executing one program (production & dispersion functions) for all membranes that have programs
        If a membrane has more than one program, one is chosen randomly for execution"""

        # production phase for all membranes
        for membraneName in self.H:
            membrane = self.membranes[membraneName]
            if (len(membrane.programs) < 1):
                continue
            logging.debug("Production for membrane %s" % membraneName)

            membrane.chosenProgramNr = 0 if len(membrane.programs) == 1 else random.randint(0, len(membrane.programs) - 1)
            try:
                # produce a new value
                membrane.newValue = membrane.programs[membrane.chosenProgramNr].prodFunction.evaluate()
            except RuntimeError:
                logging.error("Error encountered during production function of membrane %s, program %d" % (membraneName, membrane.chosenProgramNr))
                # re-raise the exception to stop the simulator
                raise

        ## reset variable phase
        logging.debug("Resetting all variables that are part of production functions to 0")
        for variable in self.variables:
            if (variable.isPartOfProductionFunction):
                variable.value = 0

        # distribution phase for all membranes
        for membraneName in self.H:
            membrane = self.membranes[membraneName]
            if (len(membrane.programs) < 1):
                continue
            logging.debug("Distribution for membrane %s of unitary value %.02f" % (
                membraneName,
                membrane.newValue / membrane.programs[membrane.chosenProgramNr].distribFunction.proportionTotal))
            # distribute the previously produced value
            membrane.programs[membrane.chosenProgramNr].distribFunction.distribute(membrane.newValue)
        logging.info("Simulation step finished succesfully")
    # end runSimulationStep()

    def simulate(self, stepByStepConfirm = False, printEachSystemState = True, maxSteps = -1, maxTime = -1):
        """Simulates the numericP system until one of the imposed limits is reached

        :stepByStepConfirm: True / False - whether or not to wait for confirmation before starting the next simulation step
        :printEachSystemState: True / False - whether or not to print the P system state after the execution ofeach simulation step
        :maxSteps: The maximmum number of simulation steps to run
        :maxTime: The maximum time span that the entire simulation can last"""

        currentStep = 0;
         # time.time() == time in seconds since the Epoch
        startTime = currentTime = time.time();
        finalTime = currentTime + maxTime

        while (True):
            logging.info("Starting simulation step %d", currentStep)

            self.runSimulationStep()
            currentTime = time.time()

            if (printEachSystemState):
                self.print()

            if (stepByStepConfirm):
                input("Press ENTER to continue")

            # if there is a maximum time limit set and it was exceded
            if ((currentTime >= finalTime) and (maxTime > 0)):
                logging.warning("Maximum time limit exceeded; Simulation stopped")
                break # stop the simulation

            # if there is a maximum step limit set and it was exceded
            if ((currentStep >= maxSteps) and (maxSteps > 0)):
                logging.warning("Maximum number of simulation steps exceeded; Simulation stopped")
                break # stop the simulation

            currentStep += 1
        #end while loop

        logging.info("Simulation finished succesfully after %d steps and %f seconds; End state below:" % (currentStep, currentTime - startTime))
        self.print()

    # end simulate()

    def print(self, indentSpaces = 2, toString = False, withPrograms = False) :
        """Print the entire Numerical P system with a given indentation level

        :indentSpaces: number of spaces used for indentation
        :toString: write to a string instead of stdout
        :withPrograms: print out the programs from each membrane, along with the membrane variables
        :returns: string print of the membrane if toString = True otherwise returns None """

        result = ""

        result += "var = {\n"
        for membraneName in self.H:
            membrane = self.membranes[membraneName]
            result += " " * indentSpaces + "%s:\n%s" % (membraneName, membrane.print(indentSpaces * 2, toString=True, withPrograms=withPrograms))
        result += "}\n"

        if (toString):
            return result
        else:
            print(result)
    # end print()
# end class NumericalPsystem

class MembraneStructure(list):

    """P system membrane structure (list of structural elements)"""

    def __init__(self):
        list.__init__(self)
# end class MembraneStructure

class Membrane():

    """Membrane class, that can contain other membranes or be part of another membrane"""

    def __init__(self, parentMembrane = None):
        self.variables = [] # array of P objects
        self.programs = [] # list of Program objects
        self.chosenProgramNr = 0 # the program nr that was chosen for execution
        self.newValue = 0 # the value that was produced during the previous production phase
        self.enzymes = [] # array of P objects
        self.parent = parentMembrane # parent membrane (Membrane object)
        self.children = {} # map (dictioanry) between String membrane_name: Membrane object


    def print(self, indentSpaces = 2, toString = False, withPrograms = False) :
        """Print a membrane with a given indentation level

        :indentSpaces: number of spaces used for indentation
        :toString: write to a string instead of stdout
        :withPrograms: print out the programs from each membrane, along with the membrane variables
        :returns: string print of the membrane if toString = True otherwise returns None """

        result = " " * indentSpaces

        result += "var = {"
        for var in self.variables:
            result += " %s: %s, " % (var.name, var.value)
        result += "}\n"

        if (withPrograms):
            for i, program in enumerate(self.programs):
                result += " " * indentSpaces + "pr_%d = { %s }\n" % (i, program.print(indentSpaces = 0, toString=True))

        if (toString):
            return result
        else:
            print(result)
    # end print()
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

        result = " " * indentSpaces + self.prodFunction.infixExpression + "  ->  " + self.distribFunction.expression

        if (toString):
            return result
        else:
            print(result)
    # end print()

# end class Program

class ProductionFunction():

    """Production function class that stores expressions using the postfix (reversed polish) form"""

    def __init__(self):
        self.infixExpression = "" # string representation of the original expression from the input file (written in infix form)
        self.postfixStack = [] # stack of operands and operators (auxiliary for postfix form)
        self.items = [] # list of operands and operators written in postfix (reverse polish) form

    def evaluate(self):
        """Evaluates the postfix form of a production function and returns the computed value.
        During the evaluation, Pobject references are replaced with their value.
        :returns: the computed value of the production function, as a numeric value"""

        self.postfixStack = []
        for item in self.items:
            # numeric values get added on the stack
            if (type(item) == int or type(item) == float):
                self.postfixStack.append(item)

            # the value of Pobjects is added to the stack
            elif (type(item) == Pobject):
                self.postfixStack.append(item.value)

            # (binary) operators require that two values are popped and the result is added back to the stack
            elif (item == OperatorType.add):
                # apply the operator
                self.postfixStack.append(self.postfixStack.pop() + self.postfixStack.pop())

            elif (item == OperatorType.multiply):
                # apply the operator
                self.postfixStack.append(self.postfixStack.pop() * self.postfixStack.pop())

            # order-dependent operators (-, /, ^) require that the operand order be opposite from that of the stack pop operation
            elif (item == OperatorType.subtract):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(op1 - op2)

            elif (item == OperatorType.divide):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(op1 / op2)

            elif (item == OperatorType.power):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(op1 ** op2)

            logging.debug("postfixStack = %s" % self.postfixStack)

        if (len(self.postfixStack) > 1):
            raise RuntimeError('evaluation error / wrong number of operands or operators')
        return self.postfixStack[0]
    # end evaluate()

# end class ProductionFunction

class DistributionFunction(list):

    """Distribution function class (list of distribution rules)"""

    def __init__(self):
        """Initialize the underling list used to store rules"""
        list.__init__(self)
        self.proportionTotal = 0
        self.expression = "" # string representation of the distribution function

    def distribute(self, newValue):
        """Update the variables referenced in the distribution rules according to the specified proportions
        :newValue: a value that has to be distributed to the variables based on the proportions specified in the distribution rules"""

        for distribRule in self:
            distribRule.variable.value += (distribRule.proportion / self.proportionTotal) * newValue
    # end distribute()
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
        # variables that are part of a production function are reset to 0 before distribution phase
        self.isPartOfProductionFunction = False
# end class Pobject


##########################################################################
# global variables

logLevel = logging.INFO

##########################################################################
# auxiliary functions

def processPostfixOperator(postfixStack, operator):
    """Compares the provided operator with a postfix stack to determine where to place a new operator (output list or stack)

    :postfixStack: stack used for operators
    :operator: OperatorType variable
    :returns: postfixStack, outputList - outputList == array of OperatorType elements that have been popped from the stack"""

    outputList = []

    # if the operator has a higher precedence than the symbol at the top of the stack,
    if (len(postfixStack) > 0 and operator > postfixStack[-1]):
        # operator is pushed onto the stack
        postfixStack.append(operator)
    # If the precedence of the symbol being scanned is lower than or equal to the precedence of the symbol at the top of the stack,
    elif (len(postfixStack) > 0 and operator <= postfixStack[-1]):
        # one element of the stack is popped to the output;
        outputList.append(postfixStack.pop())
        # the scan pointer is not advanced. Instead, the symbol being scanned will be compared with the new top element on the stack.
        newPostfixStack, newOutputList = processPostfixOperator(postfixStack, operator)

        postfixStack = newPostfixStack
        outputList.extend(newOutputList)
    # if the stack is empty
    elif (len(postfixStack) == 0):
        postfixStack.append(operator)

    return postfixStack, outputList
# end processPostfixOperator()

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

                # if the prev_token is the name of a membrane
                elif (prev_token.value in result.H):
                    logging.info("building Membrane");
                    index, result.membranes[prev_token.value] = process_tokens(tokens, Membrane(), index + 1);

                elif (prev_token.value == 'structure'):
                    logging.info("building membrane structure");
                    index, result.structure = process_tokens(tokens, MembraneStructure(), index + 1);

                else:
                    raise RuntimeError("Unexpected token '%s' on line %d" % (prev_token.value, prev_token.line))
        # end if parent == NumericalPsystem

        elif (type(parent) == MembraneStructure):
            logging.debug("processing as MembraneStructure")
            if (token.type in ('ID', 'NUMBER', 'L_BRACKET', 'R_BRACKET')):
                parent.append(token)

            elif (token.type == 'END'):
                logging.info("finished the MembraneStructure with result = %s" % result)
                return index, result;

            else:
                raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))
        # end if parent == MembraneStructure

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
            # construct a string representation of the expression (in infix form)
            if (token.type != 'PROD_DISTRIB_SEPARATOR'):
                result.infixExpression += " " + token.value

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

            elif (token.type in ('OPERATOR_ADD', 'OPERATOR_SUBTRACT', 'OPERATOR_MULTIPLY', 'OPERATOR_DIVIDE', 'OPERATOR_POWER')):
                logging.debug("processing operator %s" % token.value)
                # current operator as OperatorType enum value
                currentOperator = dictOperatorTypes[token.type]

                result.postfixStack, newOutputList = processPostfixOperator(result.postfixStack, currentOperator)
                result.items.extend(newOutputList)

            elif (token.type == 'PROD_DISTRIB_SEPARATOR'):
                logging.debug("production function end; emptying stack")
                # pop all elements in the stack
                while (len(result.postfixStack) > 0):
                    result.items.append(result.postfixStack.pop())
                logging.info("finished the production function with result = %s" % result.items)
                result.infixExpression = result.infixExpression[1:] # strip the first character (leading space)
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
                result.expression += " " + token.value

            elif (token.type == 'ID' and prev_token.type == "DISTRIBUTION_SIGN"):
                # finalize the distribution rule
                distribRule.variable = token.value # store as string for now, reference later
                result.proportionTotal += distribRule.proportion
                result.append(distribRule) # store the new distribution rule
                result.expression += token.value

            # is used to separate rules, not needed
            elif (token.type == 'OPERATOR_ADD'):
                result.expression += " " + token.value
                logging.debug("skipped '+'")
                # continue to next token
                prev_token = token;
                index += 1
                continue

            # is used to separate the proportion from the variable, not needed
            elif (token.type == "DISTRIBUTION_SIGN"):
                result.expression += token.value
                logging.debug("skipped '|'")
                # continue to next token
                prev_token = token;
                index += 1
                continue

            elif (token.type == 'R_CURLY_BRACE'):
                logging.info("finished this DistributionFunction with result = %s" % result)
                result.expression = result.expression[1:] # strip the first character (leading space)
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
            if (token.type == 'ID'):
                result.append(token.value);

            elif (token.type == 'ID' or token.type == 'NUMBER'):
                result.append(int(token.value));

            elif (token.type == 'ID' or token.type == 'NUMBER_FLOAT'):
                result.append(float(token.value));

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

    index, system = process_tokens(tokens, None, 0)

    logging.debug("constructing a global list of variables used in the entire P system")
    for membrane in system.membranes.values():
        for var in membrane.variables:
            if var not in system.variables:
                system.variables.append(var)

    logging.debug("cross-referencing string identifiers to the corresponding Pobject instance")
    # cross-reference string identifiers with references to Pobject instances
    for var in system.variables:
        for (membrane_name, membrane) in system.membranes.items():
            logging.debug("processing membrane %s" % membrane_name)
            for pr in membrane.programs:
                # replacing in production function
                for i, item in enumerate(pr.prodFunction.items[:]):
                    if (var.name == item):
                        logging.debug("replacing '%s' in production function" % item)
                        # string value is replaced with a Pobject reference
                        pr.prodFunction.items[i] = var
                        # mark this variable as part of a production function
                        var.isPartOfProductionFunction = True
                # replacing in distribution function
                for i, distribRule in enumerate(pr.distribFunction):
                    if (var.name == distribRule.variable):
                        logging.debug("replacing '%s' in distribution function" % distribRule.variable)
                        # string value is replaced with a Pobject reference
                        distribRule.variable = var

    logging.debug("Constructing the internal membrane structure of the P system")
    # construct a tree representation of the P system for use for e.g. in membrane dissolution rules
    # starting from a list of tokens: structure = [1[2]2[3]3]1
    currentMembrane = None
    prev_token = system.structure[0]
    # iteration starts from the second token (system.structure[1])
    for token in system.structure[1:]:
        if (token.type in ('ID', 'NUMBER')):
            # a new branch should be created
            if (prev_token.type == 'L_BRACKET'):
                if (currentMembrane == None):
                    currentMembrane = system.membranes[token.value]
                else:
                    # create a new child membrane
                    currentMembrane.children[token.value] = system.membranes[token.value]
                    # retain the child membrane's parent
                    currentMembrane.children[token.value].parent = currentMembrane
                    currentMembrane = currentMembrane.children[token.value]

            # a branch should be closed and move one level up
            elif (prev_token.type == 'R_BRACKET'):
                currentMembrane = currentMembrane.parent

        # store previous token
        prev_token = token

    return system
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
