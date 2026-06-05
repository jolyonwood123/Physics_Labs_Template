from scipy import constants

c = constants.physical_constants["alpha particle mass"]
print(constants.au)
UNITS = {
    "length":      {"m": 1.0, "cm": constants.centi, "au": constants.au, "km": constants.kilo, },
    "mass":        {"kg": 1.0, "g": constants.milli, "mg": constants.milli, "ug": constants.micro},
    "time":        {"s": 1.0, "ms": constants.milli, "min": 60.0, "hour": 3600.0, "day": 86400.0,"ug":constants.micro, "ns":constants.nano, "ps":constants.pico, "fs": constants.femto},
    "pressure":    {"Pa": 1.0, "atm": constants.atmosphere},
    "energy":      {"J": 1.0, "eV": 1.602e-19,},
    "volume":      {"L": 1.0, "ml": constants.milli}
    }


