===============
Getting Started
===============

--------
Download
--------

The first step is to set up Python (2 or 3). Installation files and documentation can be found at `<https://www.python.org/>`_


The simulator is available for both Python 2 and 3 versions and can be downloaded from the following links:

    * `PeP for Python 3 <https://github.com/andrei91ro/pep/archive/master.zip>`_
    * `PeP for Python 2 <https://github.com/andrei91ro/pep/archive/python2_compatible_take_two.zip>`_


Optionally, the `colorlog <https://pypi.python.org/pypi/colorlog>`_ Python module can be installed in order to color messages according to the level of importance.

-----
Usage
-----

The simulator can be used as a standalone application::

    pep.py INPUT_FILE_NAME.pep [OPTIONS]

where [OPTIONS] can be:

* ``--step``: require the user to press enter after befor running the next simulation step;
* ``-n NUMBER``: stop the simulation after `n` simulation steps;
* ``--csv``: write a .csv document at the end of the simulation that contains the values of each variable at each simulation step;
* ``-v`` or ``--debug``: increase verbosity by showing DEBUG messages
* ``-v0`` or ``--error``: reduce verbosity by showing only ERROR messages


The :any:`examples` section contains different numerical P systems as well as the output that is produced.
