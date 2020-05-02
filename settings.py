"""
.. module:: settings
   :synopsis: A file containing settings used globally throughout Symboard. They
   have been placed in one file so that they're easy to configure.

.. moduleauthor:: Andrew J. Young

"""

VERSION: str = '0.2.0'
""" The current version of symboard being used, equivalent to a string
<major_version>.<minor_version>.<patch>
"""

DEFAULT_OUTPUT_PATH: str = './a.keylayout'
""" If no output path is specified, the keylayout will default to being written
to the path specified by DEFAULT_OUTPUT_PATH. This string can, but does not need
to, end in «.keylayout».
"""

# Integration testing variables {

KEEP_INTEGRATION_TEST_OUTPUT_FILE = False
""" True iff you want to keep the created output from integration tests as the
default. Otherwise False. """

KEEP_ISO_INTEGRATION_TEST_OUTPUT_FILE = False
""" True iff you want to keep the created output from Iso integration tests as
the default. Otherwise False. """

KEEP_ISO_DVORAK_INTEGRATION_TEST_OUTPUT_FILE = False
""" True iff you want to keep the created output from IsoDvorak integration
tests as the default. Otherwise False. """

KEEP_ISO_JDVORAK_INTEGRATION_TEST_OUTPUT_FILE = False
""" True iff you want to keep the created output from integration tests for
IsoJDvorak as the default. Otherwise False. """

# } Integration testing variables.
