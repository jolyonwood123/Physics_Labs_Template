import logging
from dataclasses import dataclass
from enum import Enum

import numpy as np
from pandas import Series

from configs import SI_UNITS, UNIT_LOOKUP

logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
logger = logging.getLogger()


class Magnitude(Enum):
    # Defined Magnitude of common used prefixs
    Atto: tuple = (10**-18, "a")
    Femto: tuple = (10**-15, "f")
    Pico: tuple = (10**-12, "p")
    Nano: tuple = (10**-9, "n")
    Micro: tuple = (10**-6, "u")
    Milli: tuple = (10**-3, "m")
    Centi: tuple = (10**-2, "c")
    Deci: tuple = (10**-1, "d")
    Hecto: tuple = (10**1, "h")
    Deca: tuple = (10**2, "da")
    Kilo: tuple = (10**3, "k")
    Mega: tuple = (10**6, "M")
    Giga: tuple = (10**9, "G")
    Tera: tuple = (10**12, "T")
    Peta: tuple = (10**15, "P")
    Exa: tuple = (10**18, "E")

    @property
    def get_mag(self):
        return self.value[0]

    @property
    def get_prefix(self):
        return self.value[1]


@dataclass
class Unit:
    # Dimensional Analysis Object with displaying and operator overloaded functions

    Metre: int = 0
    Kilogram: int = 0
    Second: int = 0
    Ampere: int = 0
    Kelvin: int = 0
    Mole: int = 0
    Candela: int = 0

    @property
    def unit(self):
        return (
            self.Metre,
            self.Kilogram,
            self.Second,
            self.Ampere,
            self.Kelvin,
            self.Mole,
            self.Candela,
        )

    @classmethod
    def from_values(
        cls,
        Metre: int = 0,
        Kilogram: int = 0,
        Second: int = 0,
        Ampere: int = 0,
        Kelvin: int = 0,
        Mole: int = 0,
        Candela: int = 0,
    ):
        return cls(Metre, Kilogram, Second, Ampere, Kelvin, Mole, Candela)

    @classmethod
    def from_tuple(cls, input: tuple):
        return cls(input[0], input[1], input[2], input[3], input[4], input[5], input[6])

    def __str__(self) -> str:
        unit_str = ""
        for index, dim in enumerate(self.unit):
            if dim == 0:
                pass
            elif self.unit in UNIT_LOOKUP:
                return UNIT_LOOKUP[self.unit]
            else:
                si_unit = SI_UNITS[index]
                unit_str += f"{si_unit[0]}^{dim} "
        return unit_str

    def __add__(self, other):
        if self == other:
            return self
        else:
            logger.error(f"Cannot add {self} with {other}")
            raise TypeError

    def __sub__(self, other):
        if self == other:
            return self
        else:
            logger.error(f"Cannot add {Unit} with {type(other)}")
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, Unit):
            return self.add_tuple(other)
        else:
            logger.error(f"Cannot multiply {Unit} with {type(other)}")
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return self.sub_tuple(other)
        else:
            logger.error(f"Cannot divide {Unit} with {type(other)}")
            raise TypeError

    def sub_tuple(self, other):
        # unit1 - unit2
        result: tuple = tuple(
            [dim - other.unit[index] for index, dim in enumerate(self.unit)]
        )
        return self.from_tuple(result)

    def add_tuple(self, other):
        # unit1 + unit2
        result: tuple = tuple(
            [dim + other.unit[index] for index, dim in enumerate(self.unit)]
        )
        return self.from_tuple(result)


# A = Unit.from_values(1, 1, 1, 0, 0, 0, 0)
# B = Unit.from_values(1, 1, 1, 0, 0, 0, 0)
# multiply = A * B  # (2, 2, 2, 0, 0, 0, 0)
# addition = A + B  # (1, 1, 1, 0, 0, 0, 0)
# subtraction = A - B  # (1, 1, 1, 0, 0, 0, 0)
# division = A / B  # (0, 0, 0, 0, 0, 0, 0)
# print(repr(multiply))
# print(multiply)
# print(repr(addition))
# print(addition)
# print(repr(subtraction))
# print(subtraction)
# print(repr(division))
# print(division)
# print(subtraction == addition)
# print(Unit.from_values(1, 0, 0, 0, 0, 0, 0))


@dataclass
class EmpData:
    points: np.ndarray
    units: Unit
    magnitude: Magnitude  # Factor from base units eg (1000) for kilometer
    resolution: None | float = (
        None  # Minimum measurement that can reasonably be made in base units (no prefix)
    )

    @classmethod
    def from_abs_uncertainty(cls, points: Series, units, mag: Magnitude, abs):
        points = points * mag.get_mag
        rel: np.ndarray = abs / points

        return cls(
            point=points,
            units=units,
            magnitude=mag,
            abs_uncertainty=abs,
            rel_uncertainty=rel,
        )

    def __add__(self, other):
        if self.resolution < self.other:
            resolution = self.other
        else:
            resolution = self.resolution
        return EmpData(
            self.points + other.points, self.unit, self.magnitude, resolution=resolution
        )

    def __mul__(self, other):
        pass

    def __div__(self, other):
        pass

    def __sub__(self, other):
        pass


@dataclass
class CalcData:
    pass
