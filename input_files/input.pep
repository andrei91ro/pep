num_ps = {
    # membrane names (labels)
    H = {skin, plus, minus};

    # structure = [1[2]2[3]3]1;

    # membrane 1
    skin = {
        var = {x_1_1}; # variables used in the production function
        pr = {2.56 * x_1_1 ^ 2 -> 1|x_1_1 + 1|x_1_2};
        pr = {(2 + 3) * 7 -> 5|x_1_3};
        var0 = (3);
    }
}
