num_ps = {
    # membrane names (labels)
    #H = {m1};
    #H = {m1, m2};
    H = {m1, m2, m3, m4, m5, m6};

    # test trignonometric functions (Matlab/Octave names):
    #   sin, sind, asin, asind
    #   cos, cosd, acos, acosd
    #   tan, tand, atan, atand, atan2, atan2d
    #   cot, cotd, acot, acotd,
    structure = [m1 [m2 ]m2 [m3 ]m3 [m4 ]m4 [m5 ]m5 [m6 ]m6 ]m1;
    #structure = [m1
            #[m2 ]m2
        #]m1;

    # membrane 1
    m1 = {
        var = {rez_1};
        # rez = 5
        pr = {3 + 2 * sin(3.1416 / 2) + rez_1 * 0 -> 1|rez_1};
        var0 = (0);
    };

    m2 = {
        var = {rez_2};
        # two variable functions like atan2 require variables to be defined within brackets
        # atan2 ( (y) (x) )
        # rez = -0.9272
        pr = {atan2((0 - 4) (3 * 1)) + rez_2 * 0 -> 1|rez_2};
        var0 = (0);
    };

    m3 = {
        var = {rez_3};
        # rez = 91.556 (0.52360 + 90 + 0.99749 + 0.034899)
        pr = {asin(0.5) + asind(1) + sin(1.5) + sind(2) + rez_3 * 0 -> 1|rez_3};
        var0 = (0);
    };

    m4 = {
        var = {rez_4};
        # rez = 2.1173 (1.0472 + 0 + 0.070737 + 0.99939)
        pr = {acos(0.5) + acosd(1) + cos(1.5) + cosd(2) + rez_4 * 0 -> 1|rez_4};
        var0 = (0);
    };

    m5 = {
        var = {rez_5};
        # rez = 100.05 (0.46365 + 45 + 14.101 + 0.034921 + 0.64350 + 39.806)
        pr = {atan(0.5) + atand(1) + tan(1.5) + tand(2) + atan2( (3) (4)) + atan2d((5) (6)) + rez_5 * 0 -> 1|rez_5};
        var0 = (0);
    };

    m6 = {
        var = {rez_6};
        # rez = 74.814 (1.1071 + 45 + 0.070915 + 28.636)
        pr = {acot(0.5) + acotd(1) + cot(1.5) + cotd(2) + rez_6 * 0 -> 1|rez_6};
        var0 = (0);
    };
}

