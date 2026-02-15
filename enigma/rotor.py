"""This module defines the following classes

  * :const:`.ROTOR_OPTIONS` - dictionary containing options of mapping strings for rotors, including reflectors
  * :class:`.Rotor` - class for each rotor
  * :func:`.rotor_from_name` - interface function to abstract away instantiating a rotor

  * :const:`.REFLECTOR_OPTIONS` - dictionary containing options of mapping strings for reflectors only
  * :class:`.Reflector` - class based on :class:`.Rotor` with rotation not doing anything  
"""

__all__ = ['ROTOR_OPTIONS', 'Rotor', 'rotor_from_name',
           'REFLECTOR_OPTIONS', 'Reflector']

from .core import EncodingDict, ALPHABET
from .plugboard import Plugboard, PlugLead
from numbers import Integral

ROTOR_OPTIONS = {
'Dummy': (ALPHABET, False),
'Beta':  ('LEYJVCNIXWPBQMDRTAKZGFUHOS', False),
'Gamma': ('FSOKANUERHMBTIYCWLQPZXVGJD', False),
'I': ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
'II': ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
'III': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
'IV': ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
'V': ('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
}
REFLECTOR_OPTIONS = {
'A': ('EJMZALYXVBWFCRQUONTSPIKHGD', False),
'B': ('YRUHQSLDPXNGOKMIEBFZCWVJAT', False),
'C': ('FVPJIAOYEDRZXWGCTKUQSBNMHL', False),
}

# Add reflector options to rotor options for easier init checks
for k, v in REFLECTOR_OPTIONS.items():
    ROTOR_OPTIONS[k] = v

class Rotor(EncodingDict):
    def __init__(self,
                 name: str | None="Dummy", 
                 position: int | None=0,
                 ring_setting: str | int | None=0):
        """
        Initialise an instance with a mapping string, 
        creating a private mapping dictionary dict 
        that is used by :meth:`self.encode_right_to_left`

        :arg name: rotor name as key from ROTOR_OPTIONS
        :type name: str

        :arg position: target position as index or alphabet letter
        :type position: int, str

        :arg ring_setting: ring setting, offsetting in opposite direction
        :type ring_setting: str
        """
        # Check input type and value
        if not isinstance(name, str):
            raise TypeError('name should be a string')
        if name not in ROTOR_OPTIONS:
            raise ValueError('name should be a key of ROTOR_OPTIONS')
        
        self._name = name
        self._position = 0
        self._num_rotations = 0

        self.setRingOffset(ring_setting)

        # Start with no mappings and fill them after
        self._dict = {}
        self._dict['left'] = {}
        self._dict['right'] = {}
        
        # Replace encodings with the mapping in both directions
        mapping_str, notch = ROTOR_OPTIONS[name]
        for i in range(26):
            self._dict['right'][ALPHABET[i]] = mapping_str[i]
            self._dict['left'][mapping_str[i]] = ALPHABET[i]

        self._notch = notch

        if position != 0:
            self.rotateToPosition(position)

    def __repr__(self):
        return f'Rotor: {self._name} ' \
            f'({self.getPosition()}, {self._notch}, {self.isAtNotch()}, ' \
            f'rotations:{self._num_rotations}, ring_offset:{self._ring_offset})'

    def _shift_in(self, ch: str) -> str:
        """Apply position and ring to an input contact before wiring."""
        idx = ALPHABET.index(ch)
        idx = (idx + self._position - self._ring_offset) % 26
        return ALPHABET[idx]

    def _unshift_out(self, ch: str) -> str:
        """Remove position and ring after wiring to get back to machine-relative letter."""
        idx = ALPHABET.index(ch)
        idx = (idx - self._position + self._ring_offset) % 26
        return ALPHABET[idx]

    def encode_right_to_left(self, ch: str) -> str:
        """
        Signal entering from the right (keyboard side), exiting left (toward reflector).
        Offsets (position, ring) are applied internally.
        """
        # 1) shift input by (position - ring)
        shifted = self._shift_in(ch)
        # 2) pass through static wiring (right map)
        wired = self._dict['right'][shifted]
        # 3) unshift by (-position + ring)
        return self._unshift_out(wired)

    def encode_left_to_right(self, ch: str) -> str:
        """
        Signal entering from the left (from reflector), exiting right (back to keyboard).
        Offsets (position, ring) are applied internally.
        """
        # 1) shift input by (position - ring)
        shifted = self._shift_in(ch)
        # 2) pass through static wiring (right map)
        wired = self._dict['left'][shifted]   # inverse path
        # 3) unshift by (-position + ring)
        return self._unshift_out(wired)

    def getDict(self, direction='left'):
        if direction not in ['left', 'right']:
            raise ValueError('direction should be left or right')
        return self._dict[direction]
    
    def isNotched(self):
        return self._notch is not False
    
    def getName(self):
        return self._name
    
    def getNotch(self):
        return self._notch
    
    def rotate(self, update_dicts=False):
        if update_dicts:
            mapping_list = list(self._dict['right'].values())
            # move first element to the end
            mapping_list.append(mapping_list.pop(0))

            for i in range(26):
                self._dict['right'][ALPHABET[i]] = mapping_list[i]
                self._dict['left'][mapping_list[i]] = ALPHABET[i]

        self._position = (self._position + 1) % 26
        self._num_rotations += 1

    def rotateToPosition(self, target=0):
        """
        This function is used for initialising a rotor
        with a particular setting by rotating it to a target position.
        It does not account for notches and rotate other rotors.

        :arg target: target position as an index from 0 to 25
        :type target: int
        """
        if not isinstance(target, Integral):
            if not isinstance(target, str):
                raise TypeError('target should be an integer or string')
            if len(target) == 1 and target in ALPHABET:
                target = ALPHABET.index(target)

        if target not in range(26):
            raise ValueError('target should range from 0 up to be excluding 26')
        
        while self._position != target:
            self.rotate()

    def getPosition(self):
        return ALPHABET[self._position]

    def isAtNotch(self):
        return (self.isNotched() and 
                self.getPosition() == self.getNotch())
    
    def setRingOffset(self, ring_setting):
        if isinstance(ring_setting, str):
            if ring_setting.isnumeric():
                ring_setting = int(ring_setting)
            elif ring_setting.isalpha() and len(ring_setting) == 1:
                ring_setting = ALPHABET.index(ring_setting)

        if not isinstance(ring_setting, int):
            raise ValueError("ring setting should be an int or str")

        self._ring_offset = ring_setting

    def getRingOffset(self):
        return f"{self._ring_offset+1:02d}"


def rotor_from_name(name):
    return Rotor(name)


class Reflector(Rotor, Plugboard):
    """
    This is essentially the same as a rotor but doesn't rotate.

    It is also based on Plugboard as it has leads, which can be perturbed

    Because it reflects, the machine can just encode from right to left.
    Therefore, add lead perturbations only needs to affect the right dictionary
    """
    def rotate(self):
        # don't have anything happen
        pass

    def __repr__(self):
        return f'Reflector: ({self._name})'

    def add(self, lead):
        """
        Add a :class:`~.PlugLead` instance *lead*
        to update the relevant dictionary

        :arg lead: a PlugLead instance that updates the dict
        :type lead: :class:`~.PlugLead`

        This function is used by :meth:`~.addLead` and :meth:`~.addLeads`,
        which are inherited from :class:`~.Plugboard`
        """
        # Update the dictionary with reassigned values once
        for key, value in lead.getDict(subset=True).items():
            self._dict['right'][key] = value

    def swapLeads(self, start_points):
        """
        Swap a pair of leads based on one pair of *start_points*
        """
        if not isinstance(start_points, (str,list)):
            raise TypeError("start_points should be a string or list")
        end_points = [self._dict['right'][key] for key in start_points]
        pairs = [f"{start}{list(reversed(end_points))[i]}"
                 for (i, start) in enumerate(start_points)]
        self.addLeads(pairs)

    def makeSwaps(self, pairs):
        """
        Swap multiple pair of leads based on *pairs* of start_points
        """
        if isinstance(pairs, str):
            pairs = pairs.split(" ")
        if not isinstance(pairs, list):
            raise TypeError("pairs should be a string or list")

        [self.swapLeads(pair) for pair in pairs]


if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    pass
