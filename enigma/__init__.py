# -*- coding: utf-8 -*-
"""This package defines constants, classes and functions to model the
enigma machine.

Individual modules in different files provide the following:

core
=============

  * :const:`.ALPHABET` - string containing capital letters of the alphabet
  * :class:`.EncodingDict` - base class to hold encodings


plugboard
================

The following are for plug leads and the plug board containing them.

  * :class:`.PlugLead` - 
  * :class:`.Plugboard`

rotor
================

  * :const:`.ROTOR_OPTIONS` - dictionary containing options of mapping strings for rotors, including reflectors
  * :class:`.Rotor` - class for each rotor
  * :func:`.rotor_from_name` - interface function to abstract away instantiating a rotor

  * :const:`.REFLECTOR_OPTIONS` - dictionary containing options of mapping strings for reflectors only
  * :class:`.Reflector` - class based on :class:`.Rotor` and :class:`.Plugboard`
    with rotation not doing anything and there being an option to add a lead to change the encoding

machine
================
  * :class:`.Machine` - class that puts it all together

sample
================
  functions for sampling settings for code breaking

"""

__all__ = []

from . import core
from .core import *
__all__.extend(core.__all__)

from . import plugboard
from .plugboard import *
__all__.extend(plugboard.__all__)

from . import rotor
from .rotor import *
__all__.extend(rotor.__all__)

from . import machine
from .machine import *
__all__.extend(machine.__all__)

from . import sample
from .sample import *
__all__.extend(sample.__all__)