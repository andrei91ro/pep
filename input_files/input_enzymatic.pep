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

