"""
.. module:: actions
   :synopsis: The functionality required to include actions and states for
   keyboards.

.. moduleauthor:: Andrew J. Young
"""


# Imports from third party packages.
from yaml import safe_load
from dataclasses import dataclass

# Imports from the local package.
from symboard.errors import AlphabetLengthException


@dataclass(init=False, eq=True, repr=True)
class State:
    """ A data class which stores information about a keyboard state.

    Properties:
        name (str): The name of the state.
        terminator (str): The terminator for the state. This is used when a
            state is entered, and another key is pressed. This output is
            overridden by defining a certain key to have a certain output when
            within a state. For example, if we're in the state «acute», which
            has terminator «´», if we type a space (which does not override the
            output), we will have typed «´ ». But, if we type «a» (which
            overrides the output to be «á» («a» with acute accent), then we will
            have typed only «á».
        action_to_output_map (dict): A map which defines the output for when a
            specific action occurs while in this state.
    """
    name: str = None
    terminator: str = None
    action_to_output_map: dict = None

    def __init__(
        self, name: str, terminator: str, action_to_output_map: dict = None
    ) -> None:
        """ Initializes an object. If an action_to_output_map is provided, then
        the object's action_to_output_map attribute will be set to it.
        Otherwise, the object's action_to_output_map will be set to {}.

        Args:
            name (str): The name of the state.
            terminator (str): The terminator of the state.
            action_to_output_map (dict, optional): A map which defines the
                output for when a specific action occurs while in this state.
        """
        self.name = name
        self.terminator = terminator
        if action_to_output_map is None:
            self.action_to_output_map = {}
        else:
            self.action_to_output_map = action_to_output_map

    def _get_actions(self, output: str) -> None:
        if len(output) == 26:
            return latin
        elif len(output) == 36:
            return alphalatin
        else:
            raise AlphabetLengthException(output)

    def with_lower(self, output_list: str) -> None:
        """ Builds the object's action_to_output_map for all lowercase numeric
        or alphanumeric letters, such that the outputs are defined according to
        output_list.

        Example:
            my_state = State(name, terminator).with_lower(
                "á,b́,ć,d́,é,f́,ǵ,h́,í,ȷ́,ḱ,ĺ,ḿ,ń,ó,ṕ,q́,ŕ,ś,t́,ú,v́,ẃ,x́,ý,ź"
            )

        In the above example, my_state will output «á» when «a» is typed; «b́»
        when «b» is typed, and so on.

        Args:
            output_list (str): The output which is expected for each key, in
                alphabetical order, and separated by commas.
        """
        outputs = output_list.split(',')

        actions = self._get_actions(outputs)

        for action, output in zip(actions.lower, outputs):
            self.action_to_output_map[action] = output

        return self


@dataclass(init=False, eq=True, repr=True, order=True)
class Action:
    """ A data class which stores information about a keylayout action.

    Properties:
        id_ (str): The identifier string (name) for the action.
        next_ (State, optional): The state which the keylayout should be in once
            the action occurs. This is used to enter, change, and remain in
            states.
    """
    id_: str = None
    next_: State = None

    def __init__(self, id_, next_=None):
        self.id_ = id_
        if next_ is not None:
            self.next_ = next_


@dataclass(init=False, eq=True, repr=True, order=True)
class Script:
    """ A data class which stores information about a script. A script is
    defined to be a set of unique, individual characters with an ordering. This
    definition is subject to change.

    Properties:
        length (int): The length of the script. For a Script «script»:
            script.length == len(script.lower) == len(script.upper)
        lower (int): The «lower case» (default) output of the script.
        upper (int, optional): An optional «upper case» for a script, which is
            accessed through pressing shift. Useful for digraphical writing
            systems (which have 2 sets of interchangeable letters). Examples of
            such scripts include latin; cyrillic; and greek (upper and lower
            case), and kana (hiragana and katakana).
    """
    length: int = None
    lower: str = None
    upper: str = None

    def __init__(self, lower: str, upper: str = None) -> None:
        """ An initializer for a script.

        Args:
            lower (str): The «lower case» (default) output of the script.
            upper (str, optional): An optional «upper case» for a script, which
            is accessed through pressing shift. Useful for writing systems which
            has 2 sets of interchangeable letters, EG latin; cyrillic; greek;
            kana.
        """
        if len(lower) != len(upper):
            raise AlphabetLengthException(lower)

        self.lower = lower
        self.length = len(lower)
        if upper is not None:
            self.upper = upper


latin = Script(
    lower='abcdefghijklmnopqrstuvwxyz',
    upper='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
)
""" An implementation of the latin script.
"""


alphalatin = Script(
    lower=latin.lower + '1234567890',
    upper=latin.upper + '&@#$%^<>()',
)
""" An implementation of the latin script including letters 1-9 and symbols
&@#$%^<>() (the symbols of the JDvorak keylayout).
"""


actions_26_lower = latin.lower
""" A string equal to the 26 letters of the lower case latin alphabet.
"""
actions_26_upper = latin.upper
""" A string equal to the 26 letters of the upper case latin alphabet.
"""

actions_36_lower = alphalatin.lower
""" A string equal to the 26 letters of the lower case latin alphabet, followed
by the numbers 0-9.
"""
actions_36_upper = alphalatin.upper
""" A string equal to the 26 letters of the lower case latin alphabet, followed
by the symbols &@#$%^<>() (the symbols of the JDvorak keylayout
"""

