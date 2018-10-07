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

