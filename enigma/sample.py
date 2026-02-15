# -*- coding: utf-8 -*-
"""
This module contains functions to sample settings.
"""

from numbers import Integral

from .core import ALPHABET
from .rotor import ROTOR_OPTIONS, REFLECTOR_OPTIONS

__all__ = ['generatePositionSettings', 
           'generateRingSettings',
           'isOdd', 'isEven', 'isGreek', 'rotor_converter',
           'generateRotorCombinations', 'generateRotorOptions',
           'generateMissingPlugboardLetter', 'generateMissingPlugboardPairs',
           'samplePairs']

rotor_converter = {'I': 1,
                   'II': 2,
                   'III': 3,
                   'IV': 4,
                   'V': 5}

def isOdd(n):
    """
    Return whether n is odd to exclude it

    Return False for None to not exclude it
    """
    if n is None:
        return False
    
    if not isinstance(n, Integral):
        raise TypeError('n should be an integer')

    return n%2 == 1

def isEven(n):
    """
    Return whether n is even to exclude it

    Return False for None to not exclude it
    """
    if n is None:
        return False
    
    if not isinstance(n, Integral):
        raise TypeError('n should be an integer')

    return n%2 == 0

def lacksOdd(n):
    """
    Return whether n lacks an odd number in it
    """
    return all([not isOdd(int(digit)) for digit in f"{n:02d}"])

def isGreek(name):
    """
    Return whether the rotor name is one of the Greek ones Beta and Gamma
    """
    return name in ["Beta", "Gamma"]

def generatePositionSettings():
    """
    Returns a generator of position settings as alphabet characters
    based on nested list comprehension
    """
    return ([i, j, k] for i in ALPHABET for j in ALPHABET for k in ALPHABET)


def filterOutOdd(options, allow_odd=True):
    """
    Handle whether options with odd numbers in them are filtered out
    """
    if allow_odd:
        return options
    return [option for option in options if lacksOdd(option)]


def generateRingSettings(allow_odd=True):
    """
    Returns a generator of ring settings as numbers
    based on nested list comprehension, filtering out 
    numbers with odd digits if required

    :arg allow_odd: whether to allow odd digits (default True)
    :type allow_odd: bool
    """
    allowed = filterOutOdd(list(range(1, 27)), allow_odd)
    return ([f"{i:02d}", f"{j:02d}", f"{k:02d}"] for i in allowed for j in allowed for k in allowed)


def generateRotorOptions(allow_odd=True, allow_even=True,
                         allow_greek=True):
    """
    Returns a set of allowed rotor options, filtering out odd or even ones

    :arg allow_odd: whether to allow odd numbers (default True)
    :type allow_odd: bool

    :arg allow_even: whether to allow even numbers (default True)
    :type allow_even: bool

    :arg allow_greek: whether to allow Greek rotors Beta and Gamma (default True)
    :type allow_greek: bool
    """
    options = list(ROTOR_OPTIONS.keys())
    options.pop(0) # don't include Dummy

    allowed_options = []
    for option in options:
        numeric_rotor = rotor_converter.get(option)

        if isEven(numeric_rotor):
            if allow_even:
                allowed_options.append(option)
        elif isOdd(numeric_rotor):
            if allow_odd:
                allowed_options.append(option)
        elif isGreek(option):
            if allow_greek:
                allowed_options.append(option)
        elif option not in REFLECTOR_OPTIONS:
            allowed_options.append(option)

    return set(allowed_options)

def generateRotorCombinations(allow_odd=True, allow_even=True,
                              allow_greek=True):
    """
    Returns a set of allowed rotor combinations, filtering out odd or even ones

    :arg allow_odd: whether to allow odd numbers (default True)
    :type allow_odd: bool

    :arg allow_even: whether to allow even numbers (default True)
    :type allow_even: bool
    """
    allowed_options = generateRotorOptions(allow_odd, allow_even, allow_greek)
    return ([i, j, k]
            for i in allowed_options for j in allowed_options for k in allowed_options
            if i != j and j != k and k != i)

def generateMissingPlugboardLetter(pair):
    """
    Generate options for replacing the question mark in a plugboard pair
    """
    if pair.find("?") == -1:
        return [pair]
    return [pair.replace("?", letter) for letter in ALPHABET]

def generateMissingPlugboardPairs(pairs_string):
    """
    Generate full set of options for all pairs by replacing question marks where needed
    """
    return [generateMissingPlugboardLetter(pair) for pair in pairs_string.split(" ")]

def samplePairs():
    """
    Generate a list of strings containing pairs of letters, excluding matches
    """
    return [f"{i}{j}" for i in ALPHABET for j in ALPHABET
            if i != j]

