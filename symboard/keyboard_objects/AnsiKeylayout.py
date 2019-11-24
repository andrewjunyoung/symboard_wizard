'''
@author: Andrew J. Young
@description: A class representing the ANSI keylayout.
'''

from keylayouts.Keylayout import Keylayout

class AnsiKeylayout(Keylayout):
    name: str = 'ANSI'
    langauge: str = 'latin'
    key_map: Dict[int, str] = {
        01: '', 
        02: '', 
        03: '', 
        04: '', 
        05: '', 
        06: '', 
        07: '', 
        08: '', 
        09: '', 
        10: '', 
        # TODO
    }
