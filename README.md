# Scrambled strings challenge

The executable `./scrmabled-strings` runs as specified.

The program is an interpreted Python script, which runs under the Python 3.8.2 installed on recent OSXs.  On other UNIX like platforms, the `#!` line might need to be edited to replace `python3` with whatever the python interpreter is called.

I have interpreted the requirements to mean that the input is in ASCII, words are made up of ASCII letters, letter comparison is case sensitive, the only whitespace allowed in the dictionary is the newlines specified as part of the problem, and the long strings fit in memory.  An empty input file is interpreted as no lines, not as a single empty line.  The code has prioritised simplicity over efficiency.

The tests are run by `python3 tests.py`.
