from enigma import (Machine, generateMissingPlugboardLetter)

code = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
crib1 = "TUTOR"
crib2 = "MAKING"
code_number = "4"

rotors = "V III IV"
reflector = "A"
ring_settings="24 12 10"
starting_positions = "SWU"
plugboard_pairs = "WP RJ A? VF I? HN CG BS".split(" ")

found = False
for plugboard_pair_1 in generateMissingPlugboardLetter("A?"):

    plugboard_pairs[2] = plugboard_pair_1

    for plugboard_pair_2 in generateMissingPlugboardLetter("I?"):

        plugboard_pairs[4] = plugboard_pair_2

        machine = Machine(rotors=rotors,
                          reflector=reflector,
                          ring_setting=ring_settings,
                          position_setting=starting_positions,
                          plugboard_mappings=plugboard_pairs)

        result = machine.encode(code)

        if crib1 in result and crib2 in result:
            found = (result, plugboard_pair_1, plugboard_pair_2)
            break

    if found:
        break


print("code", code_number, "=", result)
print("pair 1 =", plugboard_pair_1)
print("pair 2 = ", plugboard_pair_2)
