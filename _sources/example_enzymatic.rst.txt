=============
Using Enzymes
=============

This example was initially presented in:

    A. B. Pavel and C. Buiu, “Using enzymatic numerical P systems for modeling mobile robot controllers,” Nat. Comput., vol. 11, no. 3, pp. 387–393, Aug. 2011.

The PeP input file for this system can also be found at ``input_files/input_enzymatic.pep``::

    num_ps = {
        # membrane names (labels)
        H = {m1, m2, m3};

        structure = [m1 [m2 ]m2 [m3 ]m3 ]m1;

        # membrane 1
        m1 = {
            var = {x_1_1, x_2_1, x_3_1}; # variables used in the production function
            E = {e_1_1, e_2_1}; # set of enzyme variables
            pr = {2*x_1_1 + x_2_1 [e_1_1 -> ] 1|x_2_1 + 1|x_3_1 + 1|x_1_2};
            pr = {x_2_1 + 3*x_3_1 [e_1_1 -> ] 1|x_2_1 + 2|x_1_2};
            pr = {x_1_1 + 4*x_3_1 [e_2_1 -> ] 1|x_1_1 + 2|x_2_1};
            var0 = (2, 3, 4); # initial values for variables x_1_1, x_2_1, x_3_1
            E0  = (4, 1); # initial values for enzymes e_1_1, e_2_1
        };

        m2 = {
            var = {x_1_2, x_2_2}; # variables used in the production function
            E = {e_1_2}; # set of enzyme variables
            pr = {x_1_2 + x_2_2 [e_1_2 -> ] 1|x_1_2 + 1|x_2_2 + 1|x_2_1};
            var0 = (3, 2);
            E0  = (5);
        };

        m3 = {
            var = {x_1_3, x_2_3, x_3_3}; # variables used in the production function
            pr = {x_1_3 + x_2_3 + x_3_3 -> 1|x_1_3 + 1|x_2_3 + 1| x_3_3};
            var0 = (2, 4, 1);
        };
    }

The system is executed for 5 simulation steps using the following command::

    ./pep.py input_files/input_enzymatic.pep -n 5

and offers the following output::

    INFO     reading input file 
    INFO     building NumericalPsystem 
    INFO     building membrane list 
    INFO     building membrane structure 
    INFO     building Membrane 
    INFO     building variable list 
    INFO     building enzyme list 
    INFO     building Program 
    INFO     building production function 
    INFO     storing enzyme required by program 
    INFO     building distribution rule 
    INFO     building Program 
    INFO     building production function 
    INFO     storing enzyme required by program 
    INFO     building distribution rule 
    INFO     building Program 
    INFO     building production function 
    INFO     storing enzyme required by program 
    INFO     building distribution rule 
    INFO     building var0 list 
    INFO     building E0 list 
    INFO     building Membrane 
    INFO     building variable list 
    INFO     building enzyme list 
    INFO     building Program 
    INFO     building production function 
    INFO     storing enzyme required by program 
    INFO     building distribution rule 
    INFO     building var0 list 
    INFO     building E0 list 
    INFO     building Membrane 
    INFO     building variable list 
    INFO     building Program 
    INFO     building production function 
    INFO     building distribution rule 
    INFO     building var0 list 
    num_ps = {
        m1:
            var = { x_1_1: 2.00,  x_2_1: 3.00,  x_3_1: 4.00, }
            E = { e_1_1: 4.00,  e_2_1: 1.00, }
            pr_0 = { 2 * x_1_1 + x_2_1  [e_1_1 -> ]  1|x_2_1 + 1|x_3_1 + 1|x_1_2 }
            pr_1 = { x_2_1 + 3 * x_3_1  [e_1_1 -> ]  1|x_2_1 + 2|x_1_2 }
            pr_2 = { x_1_1 + 4 * x_3_1  [e_2_1 -> ]  1|x_1_1 + 2|x_2_1 }
        m2:
            var = { x_1_2: 3.00,  x_2_2: 2.00, }
            E = { e_1_2: 5.00, }
            pr_0 = { x_1_2 + x_2_2  [e_1_2 -> ]  1|x_1_2 + 1|x_2_2 + 1|x_2_1 }
        m3:
            var = { x_1_3: 2.00,  x_2_3: 4.00,  x_3_3: 1.00, }
            E = {}
            pr_0 = { x_1_3 + x_2_3 + x_3_3  ->  1|x_1_3 + 1|x_2_3 + 1|x_3_3 }
    }

    INFO     Starting simulation step 1 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 0.00,  x_2_1: 9.00,  x_3_1: 2.33, }
        E = { e_1_1: 4.00,  e_2_1: 1.00, }
      m2:
        var = { x_1_2: 14.00,  x_2_2: 1.67, }
        E = { e_1_2: 5.00, }
      m3:
        var = { x_1_3: 2.33,  x_2_3: 2.33,  x_3_3: 2.33, }
        E = {}
    }

    INFO     Starting simulation step 2 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 3.11,  x_2_1: 19.78,  x_3_1: 3.00, }
        E = { e_1_1: 4.00,  e_2_1: 1.00, }
      m2:
        var = { x_1_2: 18.89,  x_2_2: 5.22, }
        E = { e_1_2: 5.00, }
      m3:
        var = { x_1_3: 2.33,  x_2_3: 2.33,  x_3_3: 2.33, }
        E = {}
    }

    INFO     Starting simulation step 3 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 0.00,  x_2_1: 18.26,  x_3_1: 8.67, }
        E = { e_1_1: 4.00,  e_2_1: 1.00, }
      m2:
        var = { x_1_2: 46.74,  x_2_2: 5.22, }
        E = { e_1_2: 5.00, }
      m3:
        var = { x_1_3: 2.33,  x_2_3: 2.33,  x_3_3: 2.33, }
        E = {}
    }

    INFO     Starting simulation step 4 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 11.56,  x_2_1: 29.20,  x_3_1: 6.09, }
        E = { e_1_1: 4.00,  e_2_1: 1.00, }
      m2:
        var = { x_1_2: 52.83,  x_2_2: 5.22, }
        E = { e_1_2: 5.00, }
      m3:
        var = { x_1_3: 2.33,  x_2_3: 2.33,  x_3_3: 2.33, }
        E = {}
    }

    INFO     Starting simulation step 5 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 11.56,  x_2_1: 29.20,  x_3_1: 6.09, }
        E = { e_1_1: 4.00,  e_2_1: 1.00, }
      m2:
        var = { x_1_2: 52.83,  x_2_2: 5.22, }
        E = { e_1_2: 5.00, }
      m3:
        var = { x_1_3: 2.33,  x_2_3: 2.33,  x_3_3: 2.33, }
        E = {}
    }

    WARNING  Maximum number of simulation steps exceeded; Simulation stopped 
    INFO     Simulation finished succesfully after 5 steps and 0.001952 seconds; End state below: 
    num_ps = {
      m1:
        var = { x_1_1: 11.56,  x_2_1: 29.20,  x_3_1: 6.09, }
        E = { e_1_1: 4.00,  e_2_1: 1.00, }
      m2:
        var = { x_1_2: 52.83,  x_2_2: 5.22, }
        E = { e_1_2: 5.00, }
      m3:
        var = { x_1_3: 2.33,  x_2_3: 2.33,  x_3_3: 2.33, }
        E = {}
    }

The most important observation is that in an Enzymatic Numerical P System there is the posibility of definining multiple programs in the same membrane.
This actually was the motivating factor behind the proposal of enzymes.

At each execution step, each program is checked whether the value of the enzyme is smaller than the minimum value of the "reactants" (the P objects that are part of the production function).
Each program that passes this condition is allowed to execute.


