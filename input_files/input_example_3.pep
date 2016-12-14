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

