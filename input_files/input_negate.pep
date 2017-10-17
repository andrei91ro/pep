num_ps = {
    # membrane names (labels)
    H = {m5};

    structure = [m5 ]m5;

    # membrane 1

    m5 = {
        var = {x_5}; # variables used in the production function
        pr = {~sin( ~3) *2 + x_5*0 -> 1|x_5};
        var0 = (2);
    };
}

