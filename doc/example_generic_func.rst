=================
Generic functions
=================

Apart from :any:`example_trigonometric`, there are also generic functions that can be used in any Numerical P System simulated in Pep. The generic functions are:

    * sqrt
    * abs
    * log
    * log10
    * log2
    * min
    * max

Two parameter functions, such as ``min`` and ``max`` are called using the following syntax ``function( (parameter_1) (parameter_2) )``.

An example Numerical P System that uses the previous list of functions can be found in ``input_files/input_generic_func.pep`` and is also shown below::

   num_ps = {
       # membrane names (labels)
       H = {m1, m2};

       # test generic functions (Matlab/Octave names):
       #   sqrt, abs, log, log10, log2. min, max
       structure = [m1 [m2 ]m2 ]m1;
       #structure = [m1
               #[m2 ]m2
           #]m1;

       # membrane 1
       m1 = {
           var = {rez_1};
           # rez = 27.935 (3.3166 + 12 + 2.5649 + 1.1461 + 3.9069 + 5)
           # two variable functions like min require variables to be defined within brackets
           pr = {sqrt(11) + abs(0 - 12) + log(13) + log10(14) + log2(15) + min((5) (10)) + rez_1 * 0 -> 1|rez_1};
           var0 = (0);
       };

       m2 = {
           var = {rez_2};
           # rez = 30.480 (4.6904 + 4 + 2.9444 + 0.84510 + 8 + 10)
           # two variable functions like max require variables to be defined within brackets
           pr = {sqrt(11 * 2) + abs((0 - 12) / 3) + log(13 + 6) + log10(14 - 7) + log2(2 ^ 8) + max((5) (10)) + rez_2 * 0  -> 1|rez_2};
           var0 = (0);
       };
   }

The output of the Numerical P System, for a single execution step was obtained after executing the following command::

    ./pep.py input_files/input_generic_func.pep -n 1

and offers the following output::

   INFO     reading input file 
   INFO     building NumericalPsystem 
   INFO     building membrane list 
   INFO     building membrane structure 
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
           var = { rez_1: 0.00, }
           E = {}
           pr_0 = { sqrt ( 11 ) + abs ( 0 - 12 ) + log ( 13 ) + log10 ( 14 ) + log2 ( 15 ) + min ( ( 5 ) ( 10 ) ) + rez_1 * 0  ->  1|rez_1 }
       m2:
           var = { rez_2: 0.00, }
           E = {}
           pr_0 = { sqrt ( 11 * 2 ) + abs ( ( 0 - 12 ) / 3 ) + log ( 13 + 6 ) + log10 ( 14 - 7 ) + log2 ( 2 ^ 8 ) + max ( ( 5 ) ( 10 ) ) + rez_2 * 0  ->  1|rez_2 }
   }

   INFO     Starting simulation step 1 
   INFO     Simulation step finished succesfully 
   num_ps = {
     m1:
       var = { rez_1: 27.93, }
       E = {}
     m2:
       var = { rez_2: 30.48, }
       E = {}
   }


The P object values that are printed by the simulator are not always precisely equal to those obtained in other mathematical software. The reason is that during the printing of each value, these are rounded to the nearest 2 digit value. The internal calculations are always done using *double* precision floating point values.
