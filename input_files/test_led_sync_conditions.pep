num_ps = {
    # membrane names (labels)
    #H = {m1, m2, m3, m4};
    H = {m1, m2, m3};

    structure = [m1
            [m2 ]m2
            [m3 ]m3
            #[m4 ]m4
    ]m1;

    # membrane 1
    m1 = {
        var = {robotID_1, base_led, bcast1_1, epuck0_signal, epuck1_signal, epuck2_signal}; # variables used in the production function
        #pr = { 2 * ( ((robotID_1 == 0) * epuck2_signal) + ((robotID_1 == 1) * epuck0_signal) + ((robotID_1 == 2) * epuck1_signal)) + (base_led * 0)  -> 1|base_led + 1|bcast1_1};
        pr = { 2 * ( ((robotID_1 == 0) * epuck2_signal) + ((robotID_1 == 1) * epuck0_signal) + ((robotID_1 == 2) * epuck1_signal)) -> 1|base_led + 1|bcast1_1};
        var0 = (1, 0, 0, 1, 0, 0);
    };

    m2 = {
        var = {a, b, c, rez1, rez2}; # variables used in the production function
        pr = { 2 * ( ((a == 1) * 0) + ((b == 2) * 1) + ((c == 3) * 0) ) -> 1|rez1 + 1|rez2};
        var0 = (1, 2, 3);
    };

    m3 = {
        var = {rez3_1, rez3_2}; # variables used in the production function
        pr = { 2 * ( ((1) * 0) + ((1) * 1) + ((1) * 0) ) -> 1|rez3_1 + 1|rez3_2};
        var0 = (0, 0);
    };

    #m4 = {
        #var = {rez4_1, rez4_2}; # variables used in the production function
        #pr = { 2 * ( ((1) * 0) + ((1) * 1) + ((1) * 0) ) -> 1|rez4_1 + 1|rez4_2};
        #var0 = (0, 0);
    #};
}

