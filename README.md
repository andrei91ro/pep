# PeP (Enzymatic) Numerical P System simulator written in Python 3 (with branch for Python 2).

## Command line usage
python2 pep.py INPUT_FILE_NAME.pep [OPTIONS]

where OPTIONS can be:

* `--step`: require the user to press enter after befor running the next simulation step;
* `-n NUMBER`: stop the simulation after `n` simulation steps;
* `--csv`: write a .csv document at the end of the simulation that contains the values of each variable at each simulation step;
* `--debug`: increase verbosity by showing DEBUG messages
* `--error`: reduce verbosity by showing only ERROR messages
This is the python 2 compatible branch

If [colorlog](https://pypi.python.org/pypi/colorlog) is installed, then messages will be coloured according to the level of importance.

# Authors
Andrei George Florea, [Cătălin Buiu](http://catalin.buiu.net)

[Department of Automatic Control And Systems Engineering](http://acse.pub.ro),

Politehnica University of Bucharest

Bucharest, Romania.
