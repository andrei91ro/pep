##################
An initial example
##################

This example was initially presented in:

    G. Păun and R. Păun, “Membrane Computing and Economics: Numerical P Systems,” Fundamenta Informaticae, vol. 73, no. 1,2. IOS Press, pp. 213–227, 01-Jan-2006.

The PeP input file for this system can also be found at ``input_files/input_example_3.pep`` ::

    num_ps = {
        # membrane names (labels)
        H = {m1, m2, m3};

        structure = [m1 [m2 ]m2 [m3 ]m3 ]m1;

        # membrane 1
        m1 = {
            var = {x_1_1}; # variables used in the production function
            #var0 = (15);
            var0 = (0);
        };

        m2 = {
            var = {x_1_2}; # variables used in the production function
            pr = {2*x_1_2 + 1 -> 1|x_1_1};
            #var0 = (0.5);
            var0 = (0);
        };

        m3 = {
            var = {x_1_3}; # variables used in the production function
            pr = {2*(x_1_3 + 1) -> 1|x_1_3 + 1|x_1_2};
            #var0 = (12.6);
            var0 = (0);
        };
    }

The following command is used to run this Numerical P system for 5 simulation steps::

    ./pep.py input_files/input_example_3.pep -n 5

This 5 step execution produces the following output::

    INFO     reading input file 
    INFO     building NumericalPsystem 
    INFO     building membrane list 
    INFO     building membrane structure 
    INFO     building Membrane 
    INFO     building variable list 
    INFO     building var0 list 
    INFO     building Membrane 
    INFO     building variable list 
    INFO     building Program 
    INFO     building production function 
    INFO     building distribution rule 
    INFO     building var0 list 
    INFO     building Membrane 
    INFO     building variable list 
    INFO     building Program 
    INFO     building production function 
    INFO     building distribution rule 
    INFO     building var0 list 
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

    INFO     Starting simulation step 3 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 9.00, }
        E = {}
      m2:
        var = { x_1_2: 3.00, }
        E = {}
      m3:
        var = { x_1_3: 3.00, }
        E = {}
    }

    INFO     Starting simulation step 4 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 16.00, }
        E = {}
      m2:
        var = { x_1_2: 4.00, }
        E = {}
      m3:
        var = { x_1_3: 4.00, }
        E = {}
    }

    INFO     Starting simulation step 5 
    INFO     Simulation step finished succesfully 
    num_ps = {
      m1:
        var = { x_1_1: 25.00, }
        E = {}
      m2:
        var = { x_1_2: 5.00, }
        E = {}
      m3:
        var = { x_1_3: 5.00, }
        E = {}
    }

    WARNING  Maximum number of simulation steps exceeded; Simulation stopped 
    INFO     Simulation finished succesfully after 5 steps and 0.001450 seconds; End state below: 
    num_ps = {
      m1:
        var = { x_1_1: 25.00, }
        E = {}
      m2:
        var = { x_1_2: 5.00, }
        E = {}
      m3:
        var = { x_1_3: 5.00, }
        E = {}
    }

Notice that after reading the entire Numerical P system, an initial print of the system, as read from the file, is shown.

This print contains the programs, P objects and the enzymes of the P system. The initial values of the P objects are also included::

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

After finishing each simulation step, a simpler print of the system is shown, where the program contents is excluded.
