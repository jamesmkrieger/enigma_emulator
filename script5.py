from enigma import (Machine, REFLECTOR_OPTIONS,
                    samplePairs)

code = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
cribs = ["FACEBOOK", "TWITTER", "INSTAGRAM", "SNAPCHAT"]
crib2 = ""#"YOUCANFOLLOWMYDOGON"
code_number = "5"

rotors = "V II IV"
ring_settings="06 18 07"
starting_positions = "AJL"
plugboard_pairs = "UG IE PO NX WT"

found = False

for reflector in REFLECTOR_OPTIONS:
    for perturbation1 in samplePairs():
        for perturbation2 in samplePairs()[1:]:

            machine = Machine(rotors=rotors,
                                reflector=reflector,
                                ring_setting=ring_settings,
                                position_setting=starting_positions,
                                plugboard_mappings=plugboard_pairs,
                                reflector_mapping_swaps=[perturbation1, perturbation2])

            result = machine.encode(code)

            if any([crib in result for crib in cribs]) and crib2 in result:
                found = (result, perturbation1, perturbation2, reflector)
                break
        if found:
            break
    if found:
        break



print("code", code_number, "=", result)
print("reflector =", reflector)
print("perturbation1 = ", perturbation1)
print("perturbation2 = ", perturbation2)
