###############################
PeP input file syntax reference
###############################
--------------
Basic template
--------------

The basic template of a *Numerical P system* in PeP is::

    num_ps = {
        H = {m1, m2};

        structure = [m1 [m2 ]m2 ]m1;

        m1 = {
            var = {x_1}; # variables that are part of this membrane
            pr = {2*x_1 + 1 -> 1|x_2};
            var0 = (0);
        };

        ...
    }

where:

    * ``num_ps``: the name of the P system
    * ``H``: a list of membrane names
    * ``structure``: describes the structure of the system. In this instance, membrane *m2* is contained by *m1*
    * ``m1 = { ... }``: the definition of membrane *m1*. Note the name of the membrane is the same as the one defined in ``H``
    * ``var = {x_1}``: a comma separated list of P objects that are part of this membrane
    * ``pr = {2*x_1 + 1 -> 1|x_2}``: the definition of a program. **A single program is allowed per membrane, for a non-enzymatic Numerical P System**

        * The ``pr`` keyword is the same for all programs.
        * The right arrow ``->`` is used to separate the *production function* (left-side) from the *distribution function* (right-side)
    * ``var0 = (0)``: a comma separated list of initial P object valuea, specified in the same order as that used for ``var``
    * comments start with ``#``
    * code blocks are delimited using ``{  }`` and are used for

        * ``num_ps``
        * ``H``
        * ``m1``
        * ``var``
        * ``pr``
    * lists of numeric constants are delimited using ``(  )`` and are used mainly for ``var0``

Note that the three suspension dots ``...`` do not have any syntactical meaning.

----------------------------
Enzymatic Numerical P System
----------------------------

An *Enzymatic Numerical P System* preserves all of the syntax elements of a *Numerical P System* and introduces several small modifications.

The basic template of an *Enzymatic Numerical P system* in PeP is::

    num_ps = {

        ...

        m3 = {
            var = {x_1_1, x_2_1, x_3_1}; # variables
            E = {e_1_1, e_2_1}; # enzymes
            pr = {2*x_1_1 + x_2_1 [e_1_1 -> ] 1|x_2_1 + 1|x_3_1 + 1|x_1_2};
            pr = {x_2_1 + 3*x_3_1 [e_1_1 -> ] 1|x_2_1 + 2|x_1_2};
            pr = {x_1_1 + 4*x_3_1 [e_2_1 -> ] 1|x_1_1 + 2|x_2_1};
            var0 = (2, 3, 4); # initial values for variables x_1_1, x_2_1, x_3_1
            E0  = (4, 1); # initial values for enzymes e_1_1, e_2_1
        };

        ...
    }

Compared to a normal *Numerical P System*, an *Enzymatic Numerical P System* introduces the following changes:

    * ``E = {e_1_1}``: a comma separated list of P objects that are the enzymes of this membrane
    * ``E0 = (0)``: a comma separated list of initial enzyme P object valuea, specified in the same order as that used for ``E``
    * in what regards programs (``pr``)

        * multiple program definitions (``pr``) are allowed
        * within the definition of a program, the ``->`` is replaced with ``[e_1_1 -> ]`` where ``e_1_1`` is the name of an enzyme P object that conditions the execution of this program. **Note that within an Enzymatic Numerical P System, there can be membranes that do not use enzymes**.

