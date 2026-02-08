# -*- coding: utf-8 -*-
"""This module defines the following classes

  * :class:`.PlugLead`
  * :class:`.Plugboard`
"""

__all__ = ['PlugLead', 'Plugboard']

from .core import EncodingDict

class PlugLead(EncodingDict):
    def __init__(self, mapping):
        """
        Initialise an instance with a mapping string, 
        creating a private mapping dictionary dict 
        that is used by :meth:`self.encode`

        :arg mapping: 2-character string for two-way mapping
        :type mapping: str
        """
        # Check input type and value
        if not isinstance(mapping, str):
            raise TypeError('mapping should be a string')
        if len(mapping) != 2:
            raise ValueError('mapping should have 2 characters')
        if not mapping.isalpha():
            raise ValueError('mapping should contain letters only')
        
        # Start with all characters mapped to themselves from inheritance
        super().__init__()
        
        # Replace encodings with the mapping in both directions
        self.dict[mapping[0]] = mapping[1]
        self.dict[mapping[1]] = mapping[0]

    def __repr__(self):
        return f'PlugLead: (mapping: {self.getDict(subset=True)})'

class Plugboard(EncodingDict):
    """Simple class that just updates the encoding dict
    
    Almost everything is inherited, including __init__
    """
    def __init__(self, leads=None):
        super().__init__()
        if leads is not None:
            self.addLeads(leads)

    def add(self, lead):
        """
        Add a :class:`~.PlugLead` instance *lead*
        to update the dict

        :arg lead: a PlugLead instance that updates the dict
        :type lead: :class:`~.PlugLead`
        """
        # Update the dictionary with reassigned values
        for key, value in lead.getDict(subset=True).items():
            self.dict[key] = value

    def addLead(self, mapping):
        """
        Create and add a :class:`~.PlugLead` instance
        based on *mapping* to update the dict

        :arg mapping: a mapping string for instantiating a PlugLead instance
        :type mapping: str
        """
        lead = PlugLead(mapping)
        self.add(lead)

    def addLeads(self, mappings):
        """
        Create and add multiple :class:`~.PlugLead` instances
        based on each mapping string in *mappings* to update the dict

        :arg mappings: a list or space-separated string containing
            mapping strings for instantiating PlugLead instances
        :type mapping: str, list
        """
        if isinstance(mappings, str):
            mappings = mappings.split(" ")
        if not isinstance(mappings, list):
            raise ValueError("mappings should be a list or string")
        
        if not all([isinstance(item, str) for item in mappings]):
            raise TypeError('mappings should have strings in a list or separated by spaces')

        for mapping in mappings:
            self.addLead(mapping)


# You will need to write more classes, which can be done here or in separate files, you choose.


if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    pass
