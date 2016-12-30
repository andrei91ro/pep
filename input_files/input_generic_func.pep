num_ps = {
    # membrane names (labels)
    H = {m1, m2};

    # test generic functions (Matlab/Octave names):
    #   sqrt, abs, log, log10, log2
    structure = [m1 [m2 ]m2 ]m1;
    #structure = [m1
            #[m2 ]m2
        #]m1;

    # membrane 1
    m1 = {
        var = {rez_1};
        # rez = 22.935 (3.3166 + 12 + 2.5649 + 1.1461 + 3.9069)
        pr = {sqrt(11) + abs(0 - 12) + log(13) + log10(14) + log2(15) + rez_1 * 0 -> 1|rez_1};
        var0 = (0);
    };

    m2 = {
        var = {rez_2};
        # rez = 20.480 (4.6904 + 4 + 2.9444 + 0.84510 + 8)
        pr = {sqrt(11 * 2) + abs((0 - 12) / 3) + log(13 + 6) + log10(14 - 7) + log2(2 ^ 8) + rez_2 * 0  -> 1|rez_2};
        var0 = (0);
    };
}

