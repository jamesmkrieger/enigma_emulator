# -*- coding: utf-8 -*-
"""
This module contains :class:`.Machine` that brings contents
from other modules together to emulate an Enigma machine.
"""

__all__ = ['Machine']

from .core import ALPHABET
from .plugboard import Plugboard
from .rotor import (Rotor, rotor_from_name, 
                    REFLECTOR_OPTIONS, Reflector)

from numbers import Integral

SETTINGS = ["ring", "position"]

class Machine():
    def __init__(self,
                 rotors: int | str | list | None=None,
                 reflector: str | None='A',
                 ring_setting: str | list | None=None,
                 position_setting: str | list | None=None,
                 plugboard_mappings: str | list | None=None,
                 reflector_mapping_swaps: str | list | None=None,
                 ):
        """
        Initialise a Machine instance with the relevant components

        :arg rotors: names of rotors as space-separated string or list
            from left to right (inserted and used first as right to left)
            default is to put in *num_rotors* dummy rotors that 
            encode each letter as itself initially
        :type rotors: str, list

        :arg reflector: name of reflector, default is **'A'**
        :type reflector: str

        :arg ring_setting: string or list containing ring offset settings of rotors
        :type ring_setting: str, list

        :arg position_setting: string or list containing initial positions of rotors
        :type position_setting: str, list

        :arg plugboard_mappings: mappings to initialise plugboard leads
            default is to build an empty one
        :type plugboard_mappings: str, list

        :arg reflector_mapping_swaps: mappings to replace reflector leads
        :type reflector_mapping_swaps: str, list
        """
        self._plugboard = Plugboard(plugboard_mappings)

        self._num_rotors = 0
        self._rotors = []
        if rotors is None:
            rotors = [Rotor("Dummy")] * 3
        self.addRotorSet(rotors)
        self._next_rotor = 0            

        if position_setting is None:
            position_setting = ["A", "A", "A"]
        self.applySetting(position_setting)

        if ring_setting is None:
            ring_setting = ["01", "01", "01"]
        self.applySetting(ring_setting, ring=True)

        if not isinstance(reflector, str):
            raise TypeError('reflector should be None or string')
        if reflector not in REFLECTOR_OPTIONS:
            raise ValueError(
                'reflector should be one of {0}'.format(
                list(REFLECTOR_OPTIONS)
            ))
        self._reflector = Reflector(reflector)

        if reflector_mapping_swaps is not None:
            self._reflector.makeSwaps(reflector_mapping_swaps)

    def addRotor(self, name, position=None):
        if position is None:
            position = self._next_rotor

        self._rotors.append(rotor_from_name(name))
        self._num_rotors += 1
        self._next_rotor = (position + 1) % self._num_rotors

    def addRotorSet(self, rotors):
        rotors = self.handleTripletInputs(rotors, name="rotors")
        for i, rotor in enumerate(reversed(rotors)):
            self.addRotor(rotor, i)

    def getRotors(self, left_to_right=False):
        """
        get rotors either from right to left as entered (default)
        or from left to right if *left_to_right* is **True**
        """
        if left_to_right:
            return self._rotors[::-1]
        return self._rotors
    
    def getSetting(self):
        return " ".join([f"{(rotor.getPosition(), rotor.getRingOffset())}"
                         for rotor in reversed(self._rotors)])
    
    def getPositionSetting(self):
        return " ".join([rotor.getPosition()
                         for rotor in reversed(self._rotors)])        
    
    def getRingSetting(self):
        return " ".join([rotor.getRingOffset()
                         for rotor in reversed(self._rotors)])  

    def getRotor(self, slot=0):
        return self._rotors[slot]

    def getOtherRotorSlots(self, slot=0):
        rotors = list(range(self._num_rotors))
        rotors.pop(slot)
        return rotors
    
    def getSuccessiveRotorSlots(self, slot=0):
        return list(range(slot+1, self._num_rotors))

    def getReflector(self):
        return self._reflector

    def rotateRotor(self, slot=0, trace=False):
        """
        Rotate a rotor with the possibility of other rotors rotating

        :arg slot: slot of rotor to rotate counting from the right as 0
        :type slot: int

        If the rotor to be rotated is at its notch, then it will rotate
        the next rotor before rotating itself.

        Also, any rotor that is at its notch, it will be called to rotate
        and will rotate the next rotor first too. This is called double step.
        """
        if slot not in range(self._num_rotors):
            raise ValueError('Invalid slot')
        

        # If a caller manually rotates a non-rightmost rotor, do a direct rotate.
        # This avoids recursion. Notch effects will be driven when rotating rotor 0
        if slot != 0:
            self._rotors[slot].rotate()
            return

        # Check which rotors are at notches that affect others (can only be 0 or 1)
        r0 = self._rotors[0]
        r1 = self._rotors[1]
        r2 = self._rotors[2]

        r0_notch = r0.isAtNotch()
        r1_notch = r1.isAtNotch()

        # Decide who steps

        # Right rotor (0) always steps.
        r0_steps = True
        # Middle rotor of stepping set (1) steps if right is at notch OR middle is at notch (double-step).
        r1_steps = r0_notch or r1_notch
        # Left of stepping set (2) steps if middle is at notch.
        r2_steps = r1_notch

        # Execute the steps
        if r2_steps:
            r2.rotate()
            if trace:
                print("rotated rotor 2")
        if r1_steps:
            r1.rotate()
            if trace:
                print("rotated rotor 1")
        if r0_steps:
            r0.rotate()
            if trace:
                print("rotated rotor 0")

    def handleTripletInputs(self, inputs, name="rotors"):
        if isinstance(inputs, str):
            inputs = inputs.split(" ")
        
        if not isinstance(inputs, list):
            raise TypeError(f'{name} should be a string or list')
        
        if len(inputs) == 1 and name in SETTINGS:
            inputs = list(inputs[0])

        if len(inputs) != self._num_rotors and name in SETTINGS:
            raise ValueError(f'the number of {name} entries for initialisation should match num_rotors ({self._num_rotors})')

        if not all([isinstance(item, str) for item in inputs]):
            raise TypeError(f'{name} should have strings in a list or separated by spaces')
        
        if name in SETTINGS:
            inputs = [self.convertPosition(position, type=name) for position in inputs]
        
        return inputs

    def convertPosition(self, position, type=SETTINGS[1]):
        if position.isalpha():
            return ALPHABET.index(position)
        return int(position) - 1

    def applySetting(self, setting, ring=False):
        name = "ring" if ring else "position"
        setting = self.handleTripletInputs(setting, name=name)

        for i, position in enumerate(reversed(setting)):
            rotor = self._rotors[i]
            if ring:
                rotor.setRingOffset(position)
            else:
                rotor.rotateToPosition(position)

    def updateReflectorLeads(self, mappings):
        self._reflector.addLeads(mappings)

    def getNextRotor(self, slot=0, left_to_right=False):
        next = slot-1 if left_to_right else slot+1
        if next in range(self._num_rotors):
            return self.getRotor(next)
        return self.getReflector()

    def pressKey(self, key=None, rotate_first=True, trace=False):

        if key is None or key not in ALPHABET:
            raise ValueError("key must be a single uppercase A-Z letter")

        if trace:
            print(f"key {key} pressed")

        if rotate_first:
            self.rotateRotor(0)

        # Plugboard IN
        signal = self._plugboard.encode(key)
        if trace:
            print(f"signal from plugboard contact {key}")
        

        # Right-to-left through all rotors
        for i, rotor in enumerate(self.getRotors()):  # indices: 0=rightmost
            prev = signal
            signal = rotor.encode_right_to_left(signal)
            if trace:
                print(f"R→L rotor {i} {rotor} : {prev} -> {signal}")

        # Reflector
        prev = signal
        signal = self.getReflector().encode_right_to_left(signal)
        if trace:
            print(f"REFLECT {self.getReflector()} : {prev} -> {signal}")

        # Left-to-right back through rotors
        if trace:
            print("now the signal goes left to right, hitting the contacts and coming out the pins")
        
        for i, rotor in enumerate(self.getRotors(left_to_right=True)):
            actual = self._num_rotors - (i+1)
            prev = signal
            signal = rotor.encode_left_to_right(signal)
            if trace:
                print(f"L←R rotor {actual} {rotor} : {prev} -> {signal}")

        # Plugboard OUT
        prev = signal
        signal = self._plugboard.encode(signal)
        if trace:
            print(f"[OUT] from rotors {prev} -> plugboard -> {signal}")

        return signal
        
    def encode(self, string, trace=False):
        result = ""
        for char in string:
            result += self.pressKey(char, trace=trace)
        return result

if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    pass
