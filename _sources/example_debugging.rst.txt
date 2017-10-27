############
More details
############

Occasionally it may happen that the system is not behaving as expected.
As in generic computer programming, PeP also offers methods to analyze the execution.

In this example, the same input file as that used in :any:`example_paun` will be used (``input_files/input_example_3.pep``)

One debugging tool is the step by step execution, that can be achieved using the ``--step``` command line parameter.

The second debugging tool implies the ``-v`` command line parameter that increases the verbosity level.::

    ./pep.py input_files/input_example_3.pep -n 1 -v

With this parameter, the output of the simulator becomes::

    INFO     reading input file 
    DEBUG    process_tokens (parent_type = <class 'NoneType'>, index = 0) 
    DEBUG    token = 'num_ps' 
    DEBUG    processing as GENERAL 
    DEBUG    token = '=' 
    DEBUG    processing as GENERAL 
    INFO     building NumericalPsystem 
    DEBUG    process_tokens (parent_type = <class '__main__.NumericalPsystem'>, index = 2)                                                                                  
    DEBUG    token = '{' 
    DEBUG    processing as NumericalPsystem 
    DEBUG    token = 'H' 
    DEBUG    processing as NumericalPsystem 
    DEBUG    token = '=' 
    DEBUG    processing as NumericalPsystem 
    INFO     building membrane list 
    DEBUG    process_tokens (parent_type = <class 'list'>, index = 5) 
    DEBUG    token = '{' 
    DEBUG    processing as List 
    DEBUG    token = 'm1' 
    DEBUG    processing as List 
    DEBUG    token = ',' 
    DEBUG    processing as List 
    DEBUG    token = 'm2' 
    DEBUG    processing as List 
    DEBUG    token = ',' 
    DEBUG    processing as List 
    DEBUG    token = 'm3' 
    DEBUG    processing as List 
    DEBUG    token = '}' 
    DEBUG    processing as List 
    DEBUG    token = ';' 
    DEBUG    processing as List 
    DEBUG    finished this block with result = ['m1', 'm2', 'm3'] 
    DEBUG    token = 'structure' 
    DEBUG    processing as NumericalPsystem 
    DEBUG    token = '=' 
    DEBUG    processing as NumericalPsystem 
    INFO     building membrane structure 
    DEBUG    process_tokens (parent_type = <class '__main__.MembraneStructure'>, index = 15)                                                                                
    DEBUG    token = '[' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = 'm1' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = '[' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = 'm2' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = ']' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = 'm2' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = '[' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = 'm3' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = ']' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = 'm3' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = ']' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = 'm1' 
    DEBUG    processing as MembraneStructure 
    DEBUG    token = ';' 
    DEBUG    processing as MembraneStructure 
    DEBUG    finished the MembraneStructure with result = [Token(type='L_BRACKET', value='[', line=5, column=16), Token(type='ID', value='m1', line=5, column=17), Token(type='L_BRACKET', value='[', line=5, column=20), Token(type='ID', value='m2', line=5, column=21), Token(type='R_BRACKET', value=']', line=5, column=24), Token(type='ID', value='m2', line=5, column=25), Token(type='L_BRACKET', value='[', line=5, column=28), Token(type='ID', value='m3', line=5, column=29), Token(type='R_BRACKET', value=']', line=5, column=32), Token(type='ID', value='m3', line=5, column=33), Token(type='R_BRACKET', value=']', line=5, column=36), Token(type='ID', value='m1', line=5, column=37)]                                                                              
    DEBUG    token = 'm1' 
    DEBUG    processing as NumericalPsystem 
    DEBUG    token = '=' 
    DEBUG    processing as NumericalPsystem 
    INFO     building Membrane 
    DEBUG    process_tokens (parent_type = <class '__main__.Membrane'>, index = 30) 
    DEBUG    token = '{' 
    DEBUG    processing as Membrane 
    DEBUG    token = 'var' 
    DEBUG    processing as Membrane 
    DEBUG    token = '=' 
    DEBUG    processing as Membrane 
    INFO     building variable list 
    DEBUG    process_tokens (parent_type = <class 'list'>, index = 33) 
    DEBUG    token = '{' 
    DEBUG    processing as List 
    DEBUG    token = 'x_1_1' 
    DEBUG    processing as List 
    DEBUG    token = '}' 
    DEBUG    processing as List 
    DEBUG    token = ';' 
    DEBUG    processing as List 
    DEBUG    finished this block with result = ['x_1_1'] 
    DEBUG    token = 'var0' 
    DEBUG    processing as Membrane 
    DEBUG    token = '=' 
    DEBUG    processing as Membrane 
    INFO     building var0 list 
    DEBUG    process_tokens (parent_type = <class 'list'>, index = 39) 
    DEBUG    token = '(' 
    DEBUG    processing as List 
    DEBUG    token = '0' 
    DEBUG    processing as List 
    DEBUG    token = ')' 
    DEBUG    processing as List 
    DEBUG    token = ';' 
    DEBUG    processing as List 
    DEBUG    finished this block with result = [0] 
    DEBUG    token = '}' 
    DEBUG    processing as Membrane 
    DEBUG    token = ';' 
    DEBUG    processing as Membrane 
    DEBUG    finished this block with result = <__main__.Membrane object at 0x7f1bcecfdac8>                                                                                 
    DEBUG    token = 'm2' 
    DEBUG    processing as NumericalPsystem 
    DEBUG    token = '=' 
    DEBUG    processing as NumericalPsystem 
    INFO     building Membrane 
    DEBUG    process_tokens (parent_type = <class '__main__.Membrane'>, index = 47) 
    DEBUG    token = '{' 
    DEBUG    processing as Membrane 
    DEBUG    token = 'var' 
    DEBUG    processing as Membrane 
    DEBUG    token = '=' 
    DEBUG    processing as Membrane 
    INFO     building variable list 
    DEBUG    process_tokens (parent_type = <class 'list'>, index = 50) 
    DEBUG    token = '{' 
    DEBUG    processing as List 
    DEBUG    token = 'x_1_2' 
    DEBUG    processing as List 
    DEBUG    token = '}' 
    DEBUG    processing as List 
    DEBUG    token = ';' 
    DEBUG    processing as List 
    DEBUG    finished this block with result = ['x_1_2'] 
    DEBUG    token = 'pr' 
    DEBUG    processing as Membrane 
    DEBUG    token = '=' 
    DEBUG    processing as Membrane 
    INFO     building Program 
    DEBUG    process_tokens (parent_type = <class '__main__.Program'>, index = 56) 
    DEBUG    token = '{' 
    DEBUG    processing as Program 
    INFO     building production function 
    DEBUG    process_tokens (parent_type = <class '__main__.ProductionFunction'>, index = 57)                                                                               
    DEBUG    token = '2' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing integer number 
    DEBUG    token = '*' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing operator * 
    DEBUG    token = 'x_1_2' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing variable 
    DEBUG    token = '+' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing operator + 
    DEBUG    token = '1' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing integer number 
    DEBUG    token = '->' 
    DEBUG    processing as ProductionFunction 
    DEBUG    production function end; emptying stack 
    DEBUG    finished the production function with result = [2, 'x_1_2', <OperatorType.multiply: 10>, 1, <OperatorType.add: 8>]                                             
    DEBUG    token = '->' 
    DEBUG    processing as Program 
    INFO     building distribution rule 
    DEBUG    process_tokens (parent_type = <class '__main__.DistributionFunction'>, index = 63)                                                                             
    DEBUG    token = '1' 
    DEBUG    processing as DistributionFunction 
    DEBUG    token = '|' 
    DEBUG    processing as DistributionFunction 
    DEBUG    skipped '|' 
    DEBUG    token = 'x_1_1' 
    DEBUG    processing as DistributionFunction 
    DEBUG    token = '}' 
    DEBUG    processing as DistributionFunction 
    DEBUG    finished this DistributionFunction with result = [<__main__.DistributionRule object at 0x7f1bcecfdcc0>]                                                        
    DEBUG    token = ';' 
    DEBUG    processing as Program 
    DEBUG    finished this block with result = <__main__.Program object at 0x7f1bcecfdbe0>                                                                                  
    DEBUG    token = 'var0' 
    DEBUG    processing as Membrane 
    DEBUG    token = '=' 
    DEBUG    processing as Membrane 
    INFO     building var0 list 
    DEBUG    process_tokens (parent_type = <class 'list'>, index = 70) 
    DEBUG    token = '(' 
    DEBUG    processing as List 
    DEBUG    token = '0' 
    DEBUG    processing as List 
    DEBUG    token = ')' 
    DEBUG    processing as List 
    DEBUG    token = ';' 
    DEBUG    processing as List 
    DEBUG    finished this block with result = [0] 
    DEBUG    token = '}' 
    DEBUG    processing as Membrane 
    DEBUG    token = ';' 
    DEBUG    processing as Membrane 
    DEBUG    finished this block with result = <__main__.Membrane object at 0x7f1bcecfdb70>                                                                                 
    DEBUG    token = 'm3' 
    DEBUG    processing as NumericalPsystem 
    DEBUG    token = '=' 
    DEBUG    processing as NumericalPsystem 
    INFO     building Membrane 
    DEBUG    process_tokens (parent_type = <class '__main__.Membrane'>, index = 78) 
    DEBUG    token = '{' 
    DEBUG    processing as Membrane 
    DEBUG    token = 'var' 
    DEBUG    processing as Membrane 
    DEBUG    token = '=' 
    DEBUG    processing as Membrane 
    INFO     building variable list 
    DEBUG    process_tokens (parent_type = <class 'list'>, index = 81) 
    DEBUG    token = '{' 
    DEBUG    processing as List 
    DEBUG    token = 'x_1_3' 
    DEBUG    processing as List 
    DEBUG    token = '}' 
    DEBUG    processing as List 
    DEBUG    token = ';' 
    DEBUG    processing as List 
    DEBUG    finished this block with result = ['x_1_3'] 
    DEBUG    token = 'pr' 
    DEBUG    processing as Membrane 
    DEBUG    token = '=' 
    DEBUG    processing as Membrane 
    INFO     building Program 
    DEBUG    process_tokens (parent_type = <class '__main__.Program'>, index = 87) 
    DEBUG    token = '{' 
    DEBUG    processing as Program 
    INFO     building production function 
    DEBUG    process_tokens (parent_type = <class '__main__.ProductionFunction'>, index = 88)                                                                               
    DEBUG    token = '2' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing integer number 
    DEBUG    token = '*' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing operator * 
    DEBUG    token = '(' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing operator ( 
    DEBUG    token = 'x_1_3' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing variable 
    DEBUG    token = '+' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing operator + 
    DEBUG    token = '1' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing integer number 
    DEBUG    token = ')' 
    DEBUG    processing as ProductionFunction 
    DEBUG    processing operator ) 
    DEBUG    token = '->' 
    DEBUG    processing as ProductionFunction 
    DEBUG    production function end; emptying stack 
    DEBUG    finished the production function with result = [2, 'x_1_3', 1, <OperatorType.add: 8>, <OperatorType.multiply: 10>]                                             
    DEBUG    token = '->' 
    DEBUG    processing as Program 
    INFO     building distribution rule 
    DEBUG    process_tokens (parent_type = <class '__main__.DistributionFunction'>, index = 96)                                                                             
    DEBUG    token = '1' 
    DEBUG    processing as DistributionFunction 
    DEBUG    token = '|' 
    DEBUG    processing as DistributionFunction 
    DEBUG    skipped '|' 
    DEBUG    token = 'x_1_3' 
    DEBUG    processing as DistributionFunction 
    DEBUG    token = '+' 
    DEBUG    processing as DistributionFunction 
    DEBUG    skipped '+' 
    DEBUG    token = '1' 
    DEBUG    processing as DistributionFunction 
    DEBUG    token = '|' 
    DEBUG    processing as DistributionFunction 
    DEBUG    skipped '|' 
    DEBUG    token = 'x_1_2' 
    DEBUG    processing as DistributionFunction 
    DEBUG    token = '}' 
    DEBUG    processing as DistributionFunction 
    DEBUG    finished this DistributionFunction with result = [<__main__.DistributionRule object at 0x7f1bcecfdda0>, <__main__.DistributionRule object at 0x7f1bcecfddd8>]  
    DEBUG    token = ';' 
    DEBUG    processing as Program 
    DEBUG    finished this block with result = <__main__.Program object at 0x7f1bcecfdd30>                                                                                  
    DEBUG    token = 'var0' 
    DEBUG    processing as Membrane 
    DEBUG    token = '=' 
    DEBUG    processing as Membrane 
    INFO     building var0 list 
    DEBUG    process_tokens (parent_type = <class 'list'>, index = 107) 
    DEBUG    token = '(' 
    DEBUG    processing as List 
    DEBUG    token = '0' 
    DEBUG    processing as List 
    DEBUG    token = ')' 
    DEBUG    processing as List 
    DEBUG    token = ';' 
    DEBUG    processing as List 
    DEBUG    finished this block with result = [0] 
    DEBUG    token = '}' 
    DEBUG    processing as Membrane 
    DEBUG    token = ';' 
    DEBUG    processing as Membrane 
    DEBUG    finished this block with result = <__main__.Membrane object at 0x7f1bcecfdcf8>                                                                                 
    DEBUG    token = '}' 
    DEBUG    processing as NumericalPsystem 
    DEBUG    constructing a global list of variables used in the entire P system 
    DEBUG    constructing a global list of enzymes used in the entire P system 
    DEBUG    cross-referencing string identifiers of VARIABLES to the corresponding Pobject instance                                                                        
    DEBUG    processing membrane m1 
    DEBUG    processing membrane m2 
    DEBUG    replacing 'x_1_1' in distribution function 
    DEBUG    processing membrane m3 
    DEBUG    processing membrane m1 
    DEBUG    processing membrane m2 
    DEBUG    replacing 'x_1_2' in production function 
    DEBUG    processing membrane m3 
    DEBUG    replacing 'x_1_2' in distribution function 
    DEBUG    processing membrane m1 
    DEBUG    processing membrane m2 
    DEBUG    processing membrane m3 
    DEBUG    replacing 'x_1_3' in production function 
    DEBUG    replacing 'x_1_3' in distribution function 
    DEBUG    cross-referencing string identifiers of ENZYMES to the corresponding Pobject instance                                                                          
    DEBUG    Constructing the internal membrane structure of the P system 
    num_ps = {
        m1:
            var = { x_1_1: 0.00, }
            E = {}
        m2:
            var = { x_1_2: 0.00, }
            E = {}
            pr_0 = { 2 * x_1_2 + 1  ->  1|x_1_1 }
        m3:
            var = { x_1_3: 0.00, }
            E = {}
            pr_0 = { 2 * ( x_1_3 + 1 )  ->  1|x_1_3 + 1|x_1_2 }
    }

    INFO     Starting simulation step 1 
    DEBUG    Production for membrane m2 
    DEBUG    postfixStack = [2] 
    DEBUG    postfixStack = [2, 0] 
    DEBUG    postfixStack = [0] 
    DEBUG    postfixStack = [0, 1] 
    DEBUG    postfixStack = [1] 
    DEBUG    Production for membrane m3 
    DEBUG    postfixStack = [2] 
    DEBUG    postfixStack = [2, 0] 
    DEBUG    postfixStack = [2, 0, 1] 
    DEBUG    postfixStack = [2, 1] 
    DEBUG    postfixStack = [2] 
    DEBUG    Resetting all variables that are part of production functions to 0 
    DEBUG    Resetting all enzymes that are part of production functions to 0 
    DEBUG    Distribution for membrane m2 of unitary value 1.00 
    DEBUG    Distribution for membrane m3 of unitary value 1.00 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 1.00, }
        E = {}
      m2:
        var = { x_1_2: 1.00, }
        E = {}
      m3:
        var = { x_1_3: 1.00, }
        E = {}
    }

    INFO     Starting simulation step 2 
    DEBUG    Production for membrane m2 
    DEBUG    postfixStack = [2] 
    DEBUG    postfixStack = [2, 1.0] 
    DEBUG    postfixStack = [2.0] 
    DEBUG    postfixStack = [2.0, 1] 
    DEBUG    postfixStack = [3.0] 
    DEBUG    Production for membrane m3 
    DEBUG    postfixStack = [2] 
    DEBUG    postfixStack = [2, 1.0] 
    DEBUG    postfixStack = [2, 1.0, 1] 
    DEBUG    postfixStack = [2, 2.0] 
    DEBUG    postfixStack = [4.0] 
    DEBUG    Resetting all variables that are part of production functions to 0 
    DEBUG    Resetting all enzymes that are part of production functions to 0 
    DEBUG    Distribution for membrane m2 of unitary value 3.00 
    DEBUG    Distribution for membrane m3 of unitary value 2.00 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 4.00, }
        E = {}
      m2:
        var = { x_1_2: 2.00, }
        E = {}
      m3:
        var = { x_1_3: 2.00, }
        E = {}
    }


The output now includes DEBUG messages that offer usefull information regarding:

    * Input file parsing.
        Any input file error will be easy to spot by tracing back the previous messages that show the context of the parsing
    * Production function expresion.
        The expression is evaluated as a postfix notation (Reverse Polish, RPN) and by watching the *postfixStack* messages, it is easy to evaluate the correctness of the calculations. ``DEBUG    postfixStack = [2, 0]``
    * Distribution function expression
        There are messages that show the unitary value that will be distributed from each membrane:``DEBUG    Distribution for membrane m2 of unitary value 1.00``
    * [Enzymatic] Numerical P Systems also show a special DEBUG message, ``DEBUG    Program 0 activated by enzyme e_1_1``,that helps in observing which program was activated by an enzyme at each simulation step.

