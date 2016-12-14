num_ps = {
    # membrane names (labels)
    H = {m1, m2, m3, m4};

    structure = [m1 [m2 [m3 ]m3 [m4]m4 ]m2 ]m1;

    # membrane 1
    m1 = {
        var = {x_1_1}; # variables used in the production function
        pr = {2 * x_1_1^2 -> 1|x_1_1 + 1|x_1_2};
        var0 = (1);
    };

    m2 = {
        var = {x_1_2, x_2_2, x_3_2}; # variables used in the production function
        pr = {x_1_2^3 - x_1_2 - 3*x_2_2 - 9 -> 1|x_2_2 + 1|x_3_2 + 1|x_2_3};
        var0 = (3, 1, 0);
    };

    m3 = {
        var = {x_1_3, x_2_3}; # variables used in the production function
        pr = {2*x_1_3 - 4*x_2_3 + 4 -> 2|x_1_3 + 1|x_2_3 + 1|x_1_2};
        var0 = (2, 1);
    };

    m4 = {
        var = {x_1_4, x_2_4, x_3_4}; # variables used in the production function
        pr = {x_1_4 * x_2_4 * x_3_4 -> 1|x_1_4 + 1|x_2_4 + 1|x_3_4 + 1|x_3_2};
        var0 = (2, 2, 2);
    };
}

