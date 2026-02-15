from enigma import Machine, generatePositionSettings

code = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
crib = "UNIVERSITY"
code_number = "2"

rotors = "Beta I III"
reflector = "B"
ring_settings="23 02 10"
starting_positions = "UNKNOWN"
plugboard_pairs = "VH PT ZG BJ EY FS"

for position_setting in generatePositionSettings():
    machine = Machine(rotors=rotors,
                      reflector=reflector,
                      ring_setting=ring_settings,
                      position_setting=position_setting,
                      plugboard_mappings=plugboard_pairs)

    result = machine.encode(code)
    if crib in result:
        break

print(f"code {code_number} = {result}, position_setting = {position_setting}")
