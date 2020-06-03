"""
.. module:: actions
   :synopsis: The functionality required to include actions and states for
   keyboards.

.. moduleauthor:: Andrew J. Young
"""


# Imports from third party packages.
from dataclasses import dataclass
import logging
from typing import List, Callable, Dict

# Imports from the local package.
from symboard.errors import AlphabetLengthException
from settings import (
    OUTPUT_DELIMITER,
    DEFAULT_STATE_TERMINATOR,
    ACTION_TO_UNICODE_MAP,
)


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
        self,
        name: str,
        terminator: str = None,
        action_to_output_map: dict = None
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
        self.terminator = terminator if terminator else DEFAULT_STATE_TERMINATOR
        self.action_to_output_map = action_to_output_map if action_to_output_map else {}

    def _get_actions(self, output: str):
        length_to_actions_map = {
            26: latin_26,
            27: latin_27,
            28: latin_28,
            36: alphalatin,
        }

        logging.info(
            f'Length of output is {len(output)} for state {repr(self)}.'
        )
        try:
            return length_to_actions_map[len(output)]
        except KeyError:
            raise AlphabetLengthException(output)

    def _with_case(self, output_list: str, case: str):
        """ A generic method for building outputs of a certain case.

        Builds the object's action_to_output_map for all (lower|upper)case
        numeric or alphanumeric letters, such that the outputs are defined
        according to output_list.

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
        outputs: List[str] = output_list.split(OUTPUT_DELIMITER)

        actions = self._get_actions(outputs)

        for action, output in zip(getattr(actions, case), outputs):
            logging.info(f'Mapping action {action} to output {output}.')

            self.action_to_output_map[self._to_unicode(action)] = output

        return self

    def with_upper(self, output_list: str):
        return self._with_case(output_list, 'upper')

    def with_lower(self, output_list: str):
        return self._with_case(output_list, 'lower')

    def _to_unicode(self, string: str) -> str:
        try:
            return ACTION_TO_UNICODE_MAP[string]
        except KeyError:
            return string

    def with_map(self, action_to_output_map: dict):
        """ A method for overriding individual outputs for individual actions
        inside the class's action_to_output_map.

        Args:
            action_to_output_map (dict): The dict containing all of the {action:
            output} pairs to add / override inside the class's
            action_to_output_map.
        """
        action_to_output_map = {
            self._to_unicode(action): output
            for action, output in action_to_output_map.items()
        }

        for action, output in action_to_output_map.items():
            self.action_to_output_map[action] = output
        return self

    def builder_method_from_attrib_name(self, attrib_name: str) -> Callable:
        atttrib_name_to_method_map: Dict[str, Callable] = {
            'upper': self.with_upper,
            'lower': self.with_lower,
            'map': self.with_map,
        }
        return atttrib_name_to_method_map[attrib_name]


@dataclass(init=False, eq=True, repr=True, order=True)
class Action:
    """ A data class which stores information about a keylayout action.

    Properties:
        id (str): The identifier string (name) for the action.
        next_ (State, optional): The state which the keylayout should be in once
            the action occurs. This is used to enter, change, and remain in
            states.
    """
    index: int = None
    key: int = None
    name: str = None
    next_: State = None

    def __init__(self, index: int, key: int, name: str, next_=None):
        self.index = index
        self.key = key
        self.name = name
        self.id = f'({str(index)},{str(key)},{name})'
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
    upper: str = None
    lower: str = None

    def __init__(self, lower: str, upper: str = None) -> None:
        """ An initializer for a script.

        Args:
            lower (str): The «lower case» (default) output of the script.
            upper (str, optional): An optional «upper case» for a script, which
            is accessed through pressing shift. Useful for writing systems which
            has 2 sets of interchangeable letters, EG latin; cyrillic; greek;
            kana.
        """
        self.lower = lower
        self.length = len(lower)
        if upper is not None:
            self.upper = upper



latin_26_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
""" A string equal to the 26 letters of the upper case latin alphabet.
"""
latin_26_lower = 'abcdefghijklmnopqrstuvwxyz'
""" A string equal to the 26 letters of the lower case latin alphabet.
"""

alphalatin_lower = latin_26_lower + '1234567890'
""" A string equal to the 26 letters of the lower case latin alphabet, followed
by the numbers 0-9.
"""
alphalatin_upper = latin_26_upper + '&@#$%^<>()'
""" A string equal to the 26 letters of the lower case latin alphabet, followed
by the symbols &@#$%^<>() (the symbols of the JDvorak keylayout
"""


latin_26 = Script(
    upper=latin_26_upper,
    lower=latin_26_lower,
)
""" An implementation of the ISO basic latin script.
"""


latin_27 = Script(
    upper=latin_26_upper,
    lower=latin_26_lower + '\'',
)
""" An implementation of the ISO basic latin script, with «\'» included in the
lower case.
"""

latin_28 = Script(
    upper=latin_26_upper,
    lower=latin_26_lower + '\'' + '\"',
)
""" An implementation of the ISO basic latin script, with «\'» and «\"» included
in the lower case.
"""

alphalatin = Script(
    lower=alphalatin_lower,
    upper=alphalatin_upper,
)
""" An implementation of the latin script including letters 1-9 and symbols
&@#$%^<>() (the symbols of the JDvorak keylayout).
"""

