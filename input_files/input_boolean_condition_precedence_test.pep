num_ps = {
    # membrane names (labels)
    H = {m1, m2, m3, m4, m5, m6};

    structure = [m1 [m2 ]m2 [m3 ]m3 [m4 ]m4 [m5 ]m5 [m6 ]m6 ]m1;

    # membrane 1
    m1 = {
        var = {rez_1}; # variables used in the production function
        pr = {2 + 1 == 2 + 1 -> 1|rez_1}; # should add 1
        var0 = (0);
    };

    m2 = {
        var = {rez_2}; # variables used in the production function
        pr = {1 != 1 - 1 -> 1|rez_2}; # should add 1
        var0 = (0);
    };

    m3 = {
        var = {rez_3}; # variables used in the production function
        pr = {2 * 3 > 2 -> 1|rez_3}; # should add 1
        var0 = (0);
    };

    m4 = {
        var = {rez_4}; # variables used in the production function
        pr = {1 / 1 * 3 >= 2 -> 1|rez_4}; # should add 1
        var0 = (0);
    };

    m5 = {
        var = {rez_5}; # variables used in the production function
        pr = {2 < 1 + (2 + 1) ^ 3 -> 1|rez_5}; # should add 1
        var0 = (0);
    };

    m6 = {
        var = {rez_6}; # variables used in the production function
        pr = {2 / 2 + 1 - 1 <= 1 -> 1|rez_6}; # should add 1
        var0 = (0);
    };

}

