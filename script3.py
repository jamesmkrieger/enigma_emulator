from enigma import (Machine, generateRingSettings, 
                    generateRotorCombinations,
                    REFLECTOR_OPTIONS)

code = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
crib = "THOUSANDS"
code_number = "3"

starting_positions = "EMY"
plugboard_pairs = "FH TS BE UQ KD AL"

nRotorCombos = len(list(generateRotorCombinations(allow_odd=False))) # 24
nRingSettings = len(list(generateRingSettings(allow_odd=False))) # 512
nReflectors = 3

nCombinations = nRotorCombos * nRingSettings * nReflectors # 36,864

found = False
for ring_settings in generateRingSettings(allow_odd=False):
    for rotors in generateRotorCombinations(allow_odd=False, allow_greek=True):
        for reflector in REFLECTOR_OPTIONS:

            machine = Machine(rotors=rotors,
                            reflector=reflector,
                            ring_setting=ring_settings,
                            position_setting=starting_positions,
                            plugboard_mappings=plugboard_pairs)

            result = machine.encode(code)

            if crib in result:
                found = (result, ring_settings, rotors, reflector)
                break
        if found:
            break
    if found:
        break


print("code", code_number, "=", result)
print("ring_settings =", ring_settings)
print("rotors = ", rotors)
print("reflector = ", reflector)
