#!/usr/bin/python2
from __future__ import print_function, with_statement, division

import collections  # for named tuple && Counter (multisets)
import re  # for regex
from enum import IntEnum # for enumerations (enum from C)
import logging # for logging functions
import random # for stochastic chosing of programs
import time # for time.time()
import math # for productionFunction evaluation of math functions

##########################################################################
# auxiliary definitions
class OperatorType(IntEnum):

    """Enumeration of operator types, ordered by precedence in calculus"""

    left_brace   = 1
    # right brace is never added to the postfix stack
    eq           = 2 # a == b
    ne           = 3 # a != b
    lt           = 4 # a < b
    le           = 5 # a <= b
    gt           = 6 # a > b
    ge           = 7 # a >= b
    add          = 8
    subtract     = 9
    multiply     = 10
    divide       = 11
    power        = 12
    negate       = 13

    # trigonometric functions
    # Functions that end with 'd' use degrees instead of radians
    sin          = 14
    sind         = 15
    asin         = 16
    asind        = 17

    cos          = 18
    cosd         = 19
    acos         = 20
    acosd        = 21

    tan          = 22
    tand         = 23
    atan         = 24
    atand        = 25
    atan2        = 26
    atan2d       = 27

    cot          = 28
    cotd         = 29
    acot         = 30
    acotd        = 31

    # generic functions
    sqrt         = 32
    abs          = 33
    log          = 34 # base e (natural) logarithm
    log10        = 35 # base 10 logarithm
    log2         = 36 # base 2 logarithm
    min          = 37 # minimum between two numbers
    max          = 38 # maximum between two numbers

# end class OperatorType

dictOperatorTypes = {
        'OPERATOR_ADD': OperatorType.add,
        'OPERATOR_SUBTRACT': OperatorType.subtract,
        'OPERATOR_NEGATE': OperatorType.negate,
        'OPERATOR_MULTIPLY': OperatorType.multiply,
        'OPERATOR_DIVIDE': OperatorType.divide,
        'OPERATOR_POWER': OperatorType.power,
        'OPERATOR_EQUAL': OperatorType.eq,
        'OPERATOR_NOT_EQUAL': OperatorType.ne,
        'OPERATOR_LESS_THAN': OperatorType.lt,
        'OPERATOR_LESS_EQUAL': OperatorType.le,
        'OPERATOR_GREATER_THAN': OperatorType.gt,
        'OPERATOR_GREATER_EQUAL': OperatorType.ge,

        'FUNCTION_SIN': OperatorType.sin,
        'FUNCTION_SIND': OperatorType.sind,
        'FUNCTION_ASIN': OperatorType.asin,
        'FUNCTION_ASIND': OperatorType.asind,
        'FUNCTION_COS': OperatorType.cos,
        'FUNCTION_COSD': OperatorType.cosd,
        'FUNCTION_ACOS': OperatorType.acos,
        'FUNCTION_ACOSD': OperatorType.acosd,
        'FUNCTION_TAN': OperatorType.tan,
        'FUNCTION_TAND': OperatorType.tand,
        'FUNCTION_ATAN': OperatorType.atan,
        'FUNCTION_ATAND': OperatorType.atand,
        'FUNCTION_ATAN2': OperatorType.atan2,
        'FUNCTION_ATAN2D': OperatorType.atan2d,
        'FUNCTION_COT': OperatorType.cot,
        'FUNCTION_COTD': OperatorType.cotd,
        'FUNCTION_ACOT': OperatorType.acot,
        'FUNCTION_ACOTD': OperatorType.acotd,

        'FUNCTION_SQRT': OperatorType.sqrt,
        'FUNCTION_ABS': OperatorType.abs,
        'FUNCTION_LOG': OperatorType.log,
        'FUNCTION_LOG10': OperatorType.log10,
        'FUNCTION_LOG2': OperatorType.log2,
        'FUNCTION_MIN': OperatorType.min,
        'FUNCTION_MAX': OperatorType.max,
        }

# tuple used to describe parsed data
Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

##########################################################################
# class definitions

class NumericalPsystem(object):

    """Numerical P systems class

    :ivar array(str) H: array of strings (names of membranes)
    :ivar dict membranes: map (dictioanry) between String membrane_name: Membrane object
    :ivar MembraneStructure structure: MembraneStructure object (list of structural elements) [1 [2 ]2 ]1
    :ivar list(Pobject) variables: list of Pobjects that appear throughtout the P system
    :ivar list(Pobject) enzymes: list of enzyme Pobjects that appear throughtout the P system
    :ivar file csvFile: file used for Comma Separated Value output
    """

    def __init__(self):
        self.H = []
        self.membranes = {}
        self.structure = None
        self.variables = []
        self.enzymes = []
        self.csvFile = None

    def runSimulationStep(self):
        """Runs 1 simulation step consisting of executing one program (production & dispersion functions) for all membranes that have programs
        If a membrane has more than one program, one is chosen randomly for execution"""

        # production phase for all membranes
        for membraneName in self.H:
            membrane = self.membranes[membraneName]
            if (len(membrane.programs) < 1):
                continue
            logging.debug("Production for membrane %s" % membraneName)

            # if this membrane does not use enzymes
            if (len(membrane.enzymes) == 0):
                membrane.chosenProgramNr = 0 if len(membrane.programs) == 1 else random.randint(0, len(membrane.programs) - 1)
            else:
                membrane.chosenProgramNr = []
                for prgNr, prg in enumerate(membrane.programs):
                    if (prg.isActivatedByEnzyme()):
                        logging.debug("Program %d activated by enzyme %s" % (prgNr, prg.enzyme.name))
                        membrane.chosenProgramNr.append(prgNr)
            try:
                # if this membrane does not use enzymes
                if (len(membrane.enzymes) == 0):
                    # produce a new value
                    membrane.newValue = membrane.programs[membrane.chosenProgramNr].prodFunction.evaluate()
                else:
                    membrane.newValue = [membrane.programs[prgNr].prodFunction.evaluate() for prgNr in membrane.chosenProgramNr ]
            except RuntimeError:
                logging.error("Error encountered during production function of membrane %s, program %s" % (membraneName, membrane.chosenProgramNr))
                # re-raise the exception to stop the simulator
                raise

        ## reset variable phase
        logging.debug("Resetting all variables that are part of production functions to 0")
        for variable in self.variables:
            if (variable.wasConsumed):
                variable.value = 0
                variable.wasConsumed = False # if the program it is part of will be executed again, it will be marked as consumed
        ## reset enzymes phase
        logging.debug("Resetting all enzymes that are part of production functions to 0")
        for enzyme in self.enzymes:
            if (enzyme.wasConsumed):
                enzyme.value = 0
                enzyme.wasConsumed = False # if the program it is part of will be executed again, it will be marked as consumed

        # distribution phase for all membranes
        for membraneName in self.H:
            membrane = self.membranes[membraneName]
            if (len(membrane.programs) < 1):
                continue
            # if this membrane uses enzymes (that allow multiple program execution)
            # and no program is active
            elif (type(membrane.chosenProgramNr) == list and len(membrane.chosenProgramNr) == 0):
                continue

            # if this membrane does not use enzymes
            if (type(membrane.chosenProgramNr) == int):
                logging.debug("Distribution for membrane %s of unitary value %.02f" % (
                    membraneName,
                    membrane.newValue / membrane.programs[membrane.chosenProgramNr].distribFunction.proportionTotal))
                # distribute the previously produced value
                membrane.programs[membrane.chosenProgramNr].distribFunction.distribute(membrane.newValue)

            # if this membrane uses enzymes (that allow multiple program execution)
            elif (type(membrane.chosenProgramNr) == list):
                for i in range(len(membrane.chosenProgramNr)):
                    logging.debug("Distribution for membrane %s program %d of unitary value %.02f" % (
                        membraneName,
                        membrane.chosenProgramNr[i],
                        membrane.newValue[i] / membrane.programs[membrane.chosenProgramNr[i]].distribFunction.proportionTotal))
                    # distribute the previously produced value
                    membrane.programs[membrane.chosenProgramNr[i]].distribFunction.distribute(membrane.newValue[i])
        logging.info("Simulation step finished succesfully")
    # end runSimulationStep()

    def simulate(self, stepByStepConfirm = False, printEachSystemState = True, maxSteps = -1, maxTime = -1):
        """Simulates the numericP system until one of the imposed limits is reached

        :stepByStepConfirm: True / False - whether or not to wait for confirmation before starting the next simulation step
        :printEachSystemState: True / False - whether or not to print the P system state after the execution ofeach simulation step
        :maxSteps: The maximmum number of simulation steps to run
        :maxTime: The maximum time span that the entire simulation can last"""

        currentStep = 1;
         # time.time() == time in seconds since the Epoch
        startTime = currentTime = time.time();
        finalTime = currentTime + maxTime

        # write initial system state into csv file
        if (self.csvFile != None):
            self.csvFile.write("%d, %s, ,%s\n" % (
                currentStep,
                ", ".join([str(var.value) for var in system.variables]),
                ", ".join([str(enz.value) for enz in system.enzymes])))

        while (True):
            logging.info("Starting simulation step %d", currentStep)

            self.runSimulationStep()
            currentTime = time.time()

            if (self.csvFile != None):
                self.csvFile.write("%d, %s, ,%s\n" % (
                        currentStep,
                        ", ".join([str(var.value) for var in system.variables]),
                        ", ".join([str(enz.value) for enz in system.enzymes])))

            if (printEachSystemState):
                self.print()

            if (stepByStepConfirm):
                raw_input("Press ENTER to continue") # input raises SyntaxError

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

        result += "num_ps = {\n"
        for membraneName in self.H:
            membrane = self.membranes[membraneName]
            result += " " * indentSpaces + "%s:\n%s" % (membraneName, membrane.print(indentSpaces * 2, toString=True, withPrograms=withPrograms))
        result += "}\n"

        if (toString):
            return result
        else:
            print(result)
    # end print()

    def openCsvFile(self):
        """Opens a .csv (Comma Separated Value) file where the values of all variables and enzymes are printed at each simulation step
        The output file is named using the pattern pep_DAY-MONTH-YEAR_HOUR-MINUTE-SECOND.csv"""
        self.csvFile = open("pep_%s.csv" % time.strftime("%d-%m-%Y_%H-%M-%S"), mode="w")

        self.csvFile.write("PeP csv output. Format = STEP_NR VARIABLE_COLUMNS EMPTY_COLUMN ENZYME_COLUMNS\n")
        self.csvFile.write("step, %s, ,%s\n" % (
                ", ".join([var.name for var in system.variables]),
                ", ".join([enz.name for enz in system.enzymes])))
    # end openCsvFile()
# end class NumericalPsystem

class MembraneStructure(list):

    """P system membrane structure (list of structural elements)"""

    def __init__(self):
        list.__init__(self)
# end class MembraneStructure

class Membrane(object):

    """Membrane class, that can contain other membranes or be part of another membrane

    :ivar list(Pobject) variables: array of P objects
    :ivar list(Program) programs: list of Program objects
    :ivar int|list chosenProgramNr: the program nr that was chosen for execution OR array of chosen program numbers when enzymes are used
    :ivar double|list(double) newValue: the value that was produced during the previous production phase OR array of values when using enzymes
    :ivar list(Pobject) enzymes: array of enzyme P objects
    :ivar Membrane parent: parent membrane (Membrane object)
    :ivar dict children: map (dictioanry) between String membrane_name: Membrane object
    """

    def __init__(self, parentMembrane = None):
        self.variables = []
        self.programs = []

        self.chosenProgramNr = 0

        self.newValue = 0
        self.enzymes = []
        self.parent = parentMembrane
        self.children = {}


    def print(self, indentSpaces = 2, toString = False, withPrograms = False) :
        """Print a membrane with a given indentation level

        :indentSpaces: number of spaces used for indentation
        :toString: write to a string instead of stdout
        :withPrograms: print out the programs from each membrane, along with the membrane variables
        :returns: string print of the membrane if toString = True otherwise returns None """

        result = " " * indentSpaces

        result += "var = {"
        for var in self.variables:
            result += " %s: %.2f, " % (var.name, var.value)
        result += "}\n"

        result += " " * indentSpaces + "E = {"
        for enz in self.enzymes:
            result += " %s: %.2f, " % (enz.name, enz.value)
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

class Program(object):

    """Program class

    :ivar ProductionFunction prodFunction: ProductionFunction object
    :ivar DistributionFunction distribFunction: DistributionFunction object
    :ivar Pobject enzyme: Pobject if an enzyme is used for this program
    """

    def __init__(self):
        self.prodFunction = None
        self.distribFunction = None
        self.enzyme = None

    def print(self, indentSpaces = 2, toString = False) :
        """Print a program with a given indentation level

        :indentSpaces: number of spaces used for indentation
        :toString: write to a string instead of stdout
        :returns: string print of the rule if toString = True otherwise returns None """

        enzymeCondition = "  ->  " if type(self.enzyme) != Pobject else "  [" +self.enzyme.name + " -> ]  "
        result = " " * indentSpaces + self.prodFunction.infixExpression + enzymeCondition + self.distribFunction.expression

        if (toString):
            return result
        else:
            print(result)
    # end print()

    def isActivatedByEnzyme(self):
        """Checks whether the production function activation condition Enzyme > min(PROD_FUNCTION_VARIABLES) is true
        :returns: True / False"""

        minVarValue = None
        for prodItem in self.prodFunction.items:
            # only P object variables are considered
            if (type(prodItem) == Pobject):
                if (minVarValue == None or minVarValue > prodItem.value):
                    minVarValue = prodItem.value

        # no variables are present in the production function
        # so the production function is active
        if (minVarValue == None):
            return True

        # the activation condition holds
        if (self.enzyme.value > minVarValue):
            return True

        return False
    # end isActivatedByEnzyme()

# end class Program

class ProductionFunction(object):

    """Production function class that stores expressions using the postfix (reversed polish) form

    :ivar str infixExpression: string representation of the original expression from the input file (written in infix form)
    :ivar list postfixStack: stack of operands and operators (auxiliary for postfix form)
    :ivar list items: list of operands and operators written in postfix (reverse polish) form
    """

    def __init__(self):
        self.infixExpression = ""
        self.postfixStack = []
        self.items = []

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
                # mark this Pobject as consummed
                item.wasConsumed = True

            # (unary) operators (single parameter functions) require that one value is popped and the result is added back to the stack
            elif (item == OperatorType.sin):
                # evaluate the function
                self.postfixStack.append( math.sin(self.postfixStack.pop()) )

            elif (item == OperatorType.sind):
                # evaluate the function
                self.postfixStack.append( math.sin(math.radians(self.postfixStack.pop())) )

            elif (item == OperatorType.asin):
                # evaluate the function
                self.postfixStack.append( math.asin(self.postfixStack.pop()) )

            elif (item == OperatorType.asind):
                # evaluate the function
                self.postfixStack.append( math.degrees(math.asin(self.postfixStack.pop())) )

            elif (item == OperatorType.cos):
                # evaluate the function
                self.postfixStack.append( math.cos(self.postfixStack.pop()) )

            elif (item == OperatorType.cosd):
                # evaluate the function
                self.postfixStack.append( math.cos(math.radians(self.postfixStack.pop())) )

            elif (item == OperatorType.acos):
                # evaluate the function
                self.postfixStack.append( math.acos(self.postfixStack.pop()) )

            elif (item == OperatorType.acosd):
                # evaluate the function
                self.postfixStack.append( math.degrees(math.acos(self.postfixStack.pop())) )

            elif (item == OperatorType.tan):
                # evaluate the function
                self.postfixStack.append( math.tan(self.postfixStack.pop()) )

            elif (item == OperatorType.tand):
                # evaluate the function
                self.postfixStack.append( math.tan(math.radians(self.postfixStack.pop())) )

            elif (item == OperatorType.atan):
                # evaluate the function
                self.postfixStack.append( math.atan(self.postfixStack.pop()) )

            elif (item == OperatorType.atand):
                # evaluate the function
                self.postfixStack.append( math.degrees(math.atan(self.postfixStack.pop())) )

            elif (item == OperatorType.cot):
                # determine cot() from tan()
                self.postfixStack.append( 1 / math.tan(self.postfixStack.pop()) )

            elif (item == OperatorType.cotd):
                # evaluate the function
                # determine cot() from tan()
                self.postfixStack.append( 1 / math.tan(math.radians(self.postfixStack.pop())) )

            elif (item == OperatorType.acot):
                # evaluate the function
                self.postfixStack.append( math.atan(1 / self.postfixStack.pop()) )

            elif (item == OperatorType.acotd):
                # evaluate the function
                self.postfixStack.append( math.degrees(math.atan(1 / self.postfixStack.pop())) )

            elif (item == OperatorType.sqrt):
                # evaluate the function
                self.postfixStack.append( math.sqrt(self.postfixStack.pop()) )

            elif (item == OperatorType.abs):
                # evaluate the function
                self.postfixStack.append( math.fabs(self.postfixStack.pop()) )

            elif (item == OperatorType.log):
                # evaluate the function
                self.postfixStack.append( math.log(self.postfixStack.pop()) )

            elif (item == OperatorType.log10):
                # evaluate the function
                self.postfixStack.append( math.log10(self.postfixStack.pop()) )

            elif (item == OperatorType.log2):
                # evaluate the function
                # log(x, base)
                self.postfixStack.append( math.log(self.postfixStack.pop(), 2) )

            elif (item == OperatorType.min):
                # evaluate the function
                self.postfixStack.append( min(self.postfixStack.pop(), self.postfixStack.pop()) )

            elif (item == OperatorType.max):
                # evaluate the function
                self.postfixStack.append( max(self.postfixStack.pop(), self.postfixStack.pop()) )

            # order-dependent binary functions require that the operand order be opposite from that of the stack pop operation
            elif (item == OperatorType.atan2):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append( math.atan2(op1, op2) )

            elif (item == OperatorType.atan2d):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append( math.degrees(math.atan2(op1, op2)) )

            # (binary) operators require that two values are popped and the result is added back to the stack
            elif (item == OperatorType.add):
                # apply the operator
                self.postfixStack.append(self.postfixStack.pop() + self.postfixStack.pop())

            elif (item == OperatorType.multiply):
                # apply the operator
                self.postfixStack.append(self.postfixStack.pop() * self.postfixStack.pop())

            # order-dependent operators (-  /  ^  <  <=  >  >=) require that the operand order be opposite from that of the stack pop operation
            elif (item == OperatorType.subtract):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(op1 - op2)

            elif (item == OperatorType.negate):
                # return the same value but with the sign reversed
                self.postfixStack.append( -self.postfixStack.pop() )

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

            elif (item == OperatorType.eq):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(int(op1 == op2))

            elif (item == OperatorType.ne):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(int(op1 != op2))

            elif (item == OperatorType.lt):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(int(op1 < op2))

            elif (item == OperatorType.le):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(int(op1 <= op2))

            elif (item == OperatorType.gt):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(int(op1 > op2))

            elif (item == OperatorType.ge):
                op2 = self.postfixStack.pop()
                op1 = self.postfixStack.pop()
                # apply the operator
                self.postfixStack.append(int(op1 >= op2))

            logging.debug("postfixStack = %s" % self.postfixStack)

        if (len(self.postfixStack) > 1):
            raise RuntimeError('evaluation error / wrong number of operands or operators')
        return self.postfixStack[0]
    # end evaluate()

# end class ProductionFunction

class DistributionFunction(list):

    """Distribution function class (list of distribution rules)

    :ivar int proportionTotal: the sum of all proportions
    :ivar str expression: string representation of the distribution function
    """

    def __init__(self):
        """Initialize the underling list used to store rules"""
        list.__init__(self)
        self.proportionTotal = 0
        self.expression = ""

    def distribute(self, newValue):
        """Update the variables referenced in the distribution rules according to the specified proportions
        :newValue: a value that has to be distributed to the variables based on the proportions specified in the distribution rules"""

        for distribRule in self:
            distribRule.variable.value += (distribRule.proportion / self.proportionTotal) * newValue
    # end distribute()
# end class DistributionFunction

class DistributionRule(object):

    """Class for the distribution rules that make up a program, together with the production rules

    :ivar int proportion:
    :ivar Pobject variable:
    """

    def __init__(self):
        self.proportion = 0
        self.variable = None

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

class Pobject(object):

    """Mutable objects that are needed in order to allow all membranes that use the P object to globally modify the object

    :ivar str name:
    :ivar double value:
    :ivar boolean wasConsumed: was consumed in production function
    """

    def __init__(self, name = '', value = 0):
        self.name = name
        self.value = value
        self.wasConsumed = False
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

    # ORDER MATTERS here: more complex tokens (e.g. >= are checked before >) to avoid incorect parsing
    token_specification = [
        ('FUNCTION_ASIND',  r'asind'),     # trigonometric function 'asin (x)' with output in degrees
        ('FUNCTION_ASIN',   r'asin'),      # trigonometric function 'asin (x)' with output in radians
        ('FUNCTION_SIND',   r'sind'),      # trigonometric function 'sin (x)' with input in degrees
        ('FUNCTION_SIN',    r'sin'),       # trigonometric function 'sin (x)' with input in radians
        ('FUNCTION_ACOSD',  r'acosd'),     # trigonometric function 'acos (x)' with output in degrees
        ('FUNCTION_ACOS',   r'acos'),      # trigonometric function 'acos (x)' with output in radians
        ('FUNCTION_COSD',   r'cosd'),      # trigonometric function 'cos (x)' with input in degrees
        ('FUNCTION_COS',    r'cos'),       # trigonometric function 'cos (x)' with input in radians
        ('FUNCTION_ATAN2D', r'atan2d'),    # trigonometric function 'atan2 (y, x)' with output in degrees
        ('FUNCTION_ATAN2',  r'atan2'),     # trigonometric function 'atan2 (y, x)' with output in radians
        ('FUNCTION_ATAND',  r'atand'),     # trigonometric function 'atan (x)' with output in degrees
        ('FUNCTION_ATAN',   r'atan'),      # trigonometric function 'atan (x)' with output in radians
        ('FUNCTION_TAND',   r'tand'),      # trigonometric function 'tan (x)' with input in degrees
        ('FUNCTION_TAN',    r'tan'),       # trigonometric function 'tan (x)' with input in radians
        ('FUNCTION_ACOTD',  r'acotd'),     # trigonometric function 'acot (x)' with output in degrees
        ('FUNCTION_ACOT',   r'acot'),      # trigonometric function 'acot (x)' with output in radians
        ('FUNCTION_COTD',   r'cotd'),      # trigonometric function 'cot (x)' with input in degrees
        ('FUNCTION_COT',    r'cot'),       # trigonometric function 'cot (x)' with input in radians

        ('FUNCTION_SQRT',   r'sqrt'),      # square root function
        ('FUNCTION_ABS',    r'abs'),       # absolute value (modulus) function
        ('FUNCTION_LOG10',  r'log10'),     # base 10 logarithm function
        ('FUNCTION_LOG2',   r'log2'),      # base 2 logarithm function
        ('FUNCTION_LOG',    r'log'),       # base e (natural) logarithm function
        ('FUNCTION_MIN',    r'min'),       # minimum value between two numbers
        ('FUNCTION_MAX',    r'max'),       # maximum value between two numbers

        ('NUMBER_FLOAT',  r'\d+\.\d+'),    # Float number
        ('NUMBER',        r'\d+'),         # Integer number

        ('OPERATOR_NOT_EQUAL', r'\!\='),   # Not equal operator (!=)
        ('OPERATOR_EQUAL', r'\=\='),       # Equal operator (==)
        ('OPERATOR_LESS_EQUAL', r'\<\='),  # Less or equal operator (<=)
        ('OPERATOR_GREATER_EQUAL', r'\>\='),# Greater or equal operator (>=)

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
        ('OPERATOR_NEGATE', r'\~'),         # Subtraction operator (-)
        ('OPERATOR_MULTIPLY', r'\*'),      # Multiplication operator (*)
        ('OPERATOR_DIVIDE', r'\/'),        # Division operator (/)
        ('OPERATOR_POWER', r'\^'),         # Power operator (^)

        ('OPERATOR_LESS_THAN', r'\<'),     # Less than operator (<)
        ('OPERATOR_GREATER_THAN', r'\>'),  # Greater than operator (>)
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
        #print("kind = %s, value = %s" % (kind, value))
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
                logging.debug("finished the MembraneStructure with result = %s" % result)
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

                elif (prev_token.value == 'E'):
                    logging.info("building enzyme list");
                    index, enzymes = process_tokens(tokens, list(), index + 1);
                    for enz in enzymes:
                        result.enzymes.append(Pobject(name = enz))

                elif (prev_token.value == 'pr'):
                    logging.info("building Program");
                    index, program = process_tokens(tokens, Program(), index + 1);
                    result.programs.append(program)

                elif (prev_token.value == 'var0'):
                    logging.info("building var0 list");
                    index, variables = process_tokens(tokens, list(), index + 1);
                    for i, var in enumerate(variables):
                        result.variables[i].value = var

                elif (prev_token.value == 'E0'):
                    logging.info("building E0 list");
                    index, enzymes = process_tokens(tokens, list(), index + 1);
                    for i, enz in enumerate(enzymes):
                        result.enzymes[i].value = enz

                else:
                    raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))
        # end if parent == Membrane

        elif (type(parent) == Program):
            logging.debug("processing as Program")

            if (token.type == 'L_CURLY_BRACE'):
                logging.info("building production function");
                index, result.prodFunction = process_tokens(tokens, ProductionFunction(), index + 1);

            elif (token.type == 'L_BRACKET'):
                logging.info("storing enzyme required by program");
                if (tokens[index + 1].type == 'ID'):
                    # storing enzyme as string for now, will be referenced later to a Pobject
                    result.enzyme = tokens[index + 1].value
                    index += 2
                else:
                    raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))


            # build a distribution rule if the PROD_DISTRIB_SEPARATOR '|' is reached for a non-enzymatic program or R_BRACKET ']' is reached for an enzymatic program
            elif ((token.type == 'PROD_DISTRIB_SEPARATOR' and result.enzyme == None)
                    or (token.type == 'R_BRACKET' and type(result.enzyme) == str)):
                logging.info("building distribution rule");
                index, result.distribFunction = process_tokens(tokens, DistributionFunction(), index + 1);

            elif (token.type == 'R_CURLY_BRACE'):
                logging.debug("finished this Program with result = %s" % result)
                return index, result;

            elif (token.type == 'END'):
                logging.debug("finished this block with result = %s" % result)
                return index, result;

            else:
                raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))
        # end if parent == Program

        elif (type(parent) == ProductionFunction):
            logging.debug("processing as ProductionFunction")
            # construct a string representation of the expression (in infix form)
            if (token.type != 'PROD_DISTRIB_SEPARATOR' and token.type != 'L_BRACKET'):
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
                while (result.postfixStack[-1] != OperatorType.left_brace):
                    op = result.postfixStack.pop()
                    # append all popped operators
                    result.items.append(op)
                # now that all elements that were above the left_brace were removed, we pop the left_brace (now the top-most element) from the stack
                result.postfixStack.pop()

            elif (token.type in dictOperatorTypes.keys()):
                logging.debug("processing operator %s" % token.value)
                # current operator as OperatorType enum value
                currentOperator = dictOperatorTypes[token.type]

                result.postfixStack, newOutputList = processPostfixOperator(result.postfixStack, currentOperator)
                result.items.extend(newOutputList)

            elif (token.type == 'PROD_DISTRIB_SEPARATOR' or token.type == 'L_BRACKET'):
                logging.debug("production function end; emptying stack")
                # pop all elements in the stack
                while (len(result.postfixStack) > 0):
                    result.items.append(result.postfixStack.pop())
                logging.debug("finished the production function with result = %s" % result.items)
                result.infixExpression = result.infixExpression[1:] # strip the first character (leading space)
                # the Program should also see PROD_DISTRIB_SEPARATOR or L_BRACKET in order to trigger the build of a distribution function or to store an enzyme for this program
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
                logging.debug("finished this DistributionFunction with result = %s" % result)
                result.expression = result.expression[1:] # strip the first character (leading space)
                return index, result;

            else:
                raise RuntimeError("Unexpected token '%s' on line %d" % (token.value, token.line))
        # end if parent == DistributionFunction

        elif (type(parent) == DistributionRule):
            logging.debug("processing as DistributionRule")

            if (token.type == 'R_CURLY_BRACE'):
                logging.debug("finished this DistributionRule with result = %s" % result)
                return index, result;
        # end if parent == DistributionRule

        elif (type(parent) == list):
            logging.debug("processing as List")
            if (token.type == 'ID'):
                result.append(token.value);

            elif (token.type == 'NUMBER'):
                if (prev_token.type == 'OPERATOR_SUBTRACT'):
                    result.append(-int(token.value));
                else:
                    result.append(int(token.value));

            elif (token.type == 'NUMBER_FLOAT'):
                if (prev_token.type == 'OPERATOR_SUBTRACT'):
                    result.append(-float(token.value));
                else:
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
            logging.debug("finished this block with result = %s" % result)
            return index, result;

        prev_token = token;
        index += 1
    return index, result
#end process_tokens
def readInputFile(filename, printTokens = True):
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


    logging.debug("constructing a global list of enzymes used in the entire P system")
    for membrane in system.membranes.values():
        for enz in membrane.enzymes:
            if enz not in system.enzymes:
                system.enzymes.append(enz)

    logging.debug("cross-referencing string identifiers of VARIABLES to the corresponding Pobject instance")
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
                # replacing in distribution function
                for i, distribRule in enumerate(pr.distribFunction):
                    if (var.name == distribRule.variable):
                        logging.debug("replacing '%s' in distribution function" % distribRule.variable)
                        # string value is replaced with a Pobject reference
                        distribRule.variable = var

    logging.debug("cross-referencing string identifiers of ENZYMES to the corresponding Pobject instance")
    # cross-reference string identifiers with references to Pobject instances
    for enz in system.enzymes:
        for (membrane_name, membrane) in system.membranes.items():
            logging.debug("processing membrane %s" % membrane_name)
            for prg_nr, pr in enumerate(membrane.programs):
                # replace the program enzyme name with reference
                if (enz.name == pr.enzyme):
                    logging.debug("replacing '%s' as program %d enzyme" % (enz.name, prg_nr))
                    pr.enzyme = enz
                # replacing in production function
                for i, item in enumerate(pr.prodFunction.items[:]):
                    if (enz.name == item):
                        logging.debug("replacing '%s' in production function" % item)
                        # string value is replaced with a Pobject reference
                        pr.prodFunction.items[i] = enz
                # replacing in distribution function
                for i, distribRule in enumerate(pr.distribFunction):
                    if (enz.name == distribRule.variable):
                        logging.debug("replacing '%s' in distribution function" % distribRule.variable)
                        # string value is replaced with a Pobject reference
                        distribRule.variable = enz

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
        print("Usage: pep.py PEP_INPUT_FILE [options]")
        print("    [options] can be:")
        print("        * -n NR: stop the simulation after NR execution steps")
        print("        * --step:          step-by-step execution")
        print("        * --csv:           write a Comma Separated Values (CSV) file that contains the values of all Pobjects at each simulation step")
        print("        * -v | --debug:    increase verbosity")
        print("        * -v0 | --error:   decrease verbosity")
        exit(1)

    # step by step simulation
    step = False
    if ('--step' in sys.argv):
        step = True

    # nr of simulation steps
    nrSteps = -2 # -2 == undefined, -1 == unlimited
    if ('-n' in sys.argv):
        try:
            nrSteps = int(sys.argv[sys.argv.index('-n') + 1])
        except (ValueError, IndexError):
            logging.error("Expected a number (of simulation steps) after the '-n' parameter")
        finally:
            # if nrSteps still is undefined (-2)
            if (nrSteps == -2):
                exit(1)

    system = readInputFile(sys.argv[1])

    if ("--csv" in sys.argv):
        system.openCsvFile()


    if (logLevel <= logging.WARNING):
        # print the structure of the P system
        system.print(indentSpaces=4, withPrograms = True)


    system.simulate(stepByStepConfirm = step, maxSteps = nrSteps)

    if (system.csvFile != None):
        logging.info("Wrote csv output file %s" % system.csvFile.name)
        system.csvFile.close()

    print("\n\n");
