# Symboard class diagram

This is a directory containing a UML class diagram generated using pyreverse and
graphviz.

## Known issues

pyreverse does not detect dataclass structures, instead only reading \_\_init\_\_
methods for class variables to include in UML diagrams. This means that some of
the information on class attributes is inaccurate.
