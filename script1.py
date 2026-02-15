from enigma import REFLECTOR_OPTIONS, Machine

for reflector in REFLECTOR_OPTIONS:
    machine = Machine(rotors="Beta Gamma V",
                      reflector=reflector,
                      ring_setting="04 02 14",
                      position_setting="MJM",
                      plugboard_mappings="KI XN FL")

    result = machine.encode("DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ")
    if "SECRETS" in result:
        break

print(f"code 1 = {result}, reflector = {reflector}")
