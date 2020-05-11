"""
.. module:: settings
   :synopsis: A file containing settings used globally throughout Symboard. They
   have been placed in one file so that they're easy to configure.

.. moduleauthor:: Andrew J. Young

"""

# Package settings {

PACKAGE_NAME = 'symboard'
""" The name of the package.
"""

VERSION: str = '0.2.0'
""" The current version of symboard being used, equivalent to a string
<major_version>.<minor_version>.<patch>
"""

DEFAULT_OUTPUT_PATH = './a.keylayout'
""" If no output path is specified, the keylayout will default to being written
to the path specified by DEFAULT_OUTPUT_PATH. This string can, but does not need
to, end in «.keylayout».
"""

OUTPUT_DELIMITER = ','
""" The delimiter used by state files between key outputs. So, «abc» would
become the output of a single key, while «a,bc» would be the output of 2. Used
throughout the states defined in the states directory, and by State builders.
"""

# } Package settings
# Import using dotenv {

from dotenv import load_dotenv
# Explicitly providing path to '.env', with verbosity.
env_path = './.env.pub'
load_dotenv(dotenv_path=env_path, verbose=True)

# } Import using dotenv

