# -*- coding: utf-8 -*-
"""This module defines base constants and classes
to build up from.

  * :const:`.ALPHABET` - string containing capital letters of the alphabet
  * :class:`.EncodingDict` - base class to hold encodings
"""

__all__ = ['ALPHABET', 'EncodingDict']

# Create an object containing the alphabet that can be used globally
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class EncodingDict(object):
    """
    Base class for handling encoding dictionaries
    """
    def __init__(self):
        """Create an encoding dictionary where all characters are mapped to themselves"""
        self.dict = {}
        for char in ALPHABET:
            self.dict[char] = char

    def encode(self, character):
        """
        Read from the mapping dictionary to encode a character.

        :arg character: 1-character string to be encoded
        :type mapping: str        
        """
        # Check input type and value
        if not isinstance(character, str):
            raise TypeError('character should be a string')
        if len(character) != 1:
            raise ValueError('character should have 1 character')
        if not character.isalpha():
            raise ValueError('character should contain a letter only')
        
        # Return encoded value from the object's dictionary using the character as a key
        return self.dict[character]
    
    def getDict(self, subset=False):
        """Return a copy of the dictionary
        
        This can optionally be a subset, having only reassigned entries
        if *subset* is **True** (default is **False**).
        """
        if subset:
            return self._getReassignedDict()
        return self.dict.copy()
    
    def _getReassignedDict(self):
        # Make and return a new dict with reassigned entries only
        new_dict = {}
        for key, value in self.dict.items():
            if value != key:
                new_dict[key] = value
        return new_dict


if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    pass
