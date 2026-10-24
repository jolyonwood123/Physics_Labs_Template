import os
import time
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime as dt
from enum import Enum
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import configs as conf

MAIN_DIR = Path(__file__).resolve().parent.parent
print(MAIN_DIR)
RAW_CONFIGS = os.getenv("DATA_CONFIGS", "{}")

PLOT_DIR = MAIN_DIR / "Plots"
TESTS_DIR = MAIN_DIR / "Tests"
MY_RAW_DATA_DIR = MAIN_DIR / "DataRaw" / "Recorded"
REFERENCE_RAW_DATA_DIR = MAIN_DIR / "DataRaw" / "Reference"
CLEAN_DATA_DIR = MAIN_DIR / "DataCleaned"
PROCESSED_DATA_DIR = MAIN_DIR / "DataProcessed"


def get_date() -> str:
    return dt.now(tz=UTC).strftime(conf.DISPLAY_DATE_FORMAT)


def get_data(data_configs: list | None = None) -> dict:
    filenames = [item.name for item in (MY_RAW_DATA_DIR).iterdir() if item.is_file()]
    DATA_DIR = MY_RAW_DATA_DIR
    data_store = {}

    for filename in filenames:
        path = DATA_DIR / filename
        print(path)
        if path.exists():
            data_store[filename] = pd.read_csv(path)

            print(filename + ": Found and loaded")

    return data_store


class Magnitude(Enum):
    # Defined Magnitude of common used prefixs
    Atto = (10**-18, "a")
    Femto = (10**-15, "f")
    Pico = (10**-12, "p")
    Nano = (10**-9, "n")
    Micro = (10**-6, "u")
    Milli = (10**-3, "m")
    Centi = (10**-2, "c")
    Deci = (10**-1, "d")
    Hecto = (10**1, "h")
    Deca = (10**2, "da")
    Kilo = (10**3, "k")
    Mega = (10**6, "M")
    Giga = (10**9, "G")
    Tera = (10**12, "T")
    Peta = (10**15, "P")
    Exa = (10**18, "E")

    @property
    def get_mag(self):
        return self.value[0]

    @property
    def get_prefix(self):
        return self.value[1]


@dataclass
class EmpData:
    point: float
    units: str
    magnitude: Magnitude  # Factor from base units eg (1000) for kilometer
    sf: None | int = None
    abs_uncertainty: float | None = None
    rel_uncertainty: float | None = None
    per_uncertainty: float | None = None

    @classmethod
    def from_abs_uncertainty(cls, point, units, mag, abs):
        rel = abs / point
        per = rel * 100

        return cls(
            point=point,
            units=units,
            magnitude=mag,
            abs_uncertainty=abs,
            rel_uncertainty=rel,
            per_uncertainty=per,
        )

    @classmethod
    def from_rel_uncertainty(cls, point, units, mag, rel):
        abs = rel * point
        per = rel * 100
        return cls(
            point=point,
            units=units,
            magnitude=mag,
            abs_uncertainty=abs,
            per_uncertainty=per,
            rel_uncertainty=rel,
        )


@dataclass
class CalcData:
    pass


class LabDataSet:
    def __init__(self, filename: str):
        data_store = get_data()
        self._df = data_store[filename]
        self.name = filename
        self.projectdir = os.path.dirname(os.path.abspath(__file__))
        self.plot_dir = PLOT_DIR

        print(self.projectdir)
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)

    def timeit(self, func, *args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Operation took {end - start:.4f} seconds.")
        return result

    def __getattr__(self, name):
        return getattr(self._df, name)

    def __getitem__(self, key):
        # Delegate the bracket lookup to the internal dataframe
        return self._df[key]

    def converter(
        self, column: str, target_units_in_units: int = 1, data_units: int = 1
    ):
        df = self._df  # noqa: F841
        data = self._df[column]
        conversion_factor = data_units / target_units_in_units
        self._df[column] = data * conversion_factor
        return self._df[column]

    def create_2dgraph(self, xaxis: str, yaxis: str, figsize: tuple = (10, 10)):
        df = self._df
        self.last_xaxis = xaxis
        self.last_yaxis = yaxis

        plt.figure(figsize=figsize)
        plt.plot(df[xaxis], df[yaxis], label="", color="red")
        plt.title(
            f"{yaxis.upper().replace('_', ' ')} vs {xaxis.upper().replace('_', ' ')}"
        )
        plt.xlabel(xaxis.replace("_", " "))
        plt.ylabel(yaxis.replace("_", " "))
        plt.grid(True)
        plt.legend()
        return plt, xaxis, yaxis

    def display_2dgraph(self):
        plt.tight_layout()
        plt.show()

    # Create, Display, then Save Graph for x and y
    def CDS_graph(self, xaxis: str, yaxis: str, figsize: tuple = (10, 10)):
        self.create_2dgraph(xaxis, yaxis, figsize)
        self.display_2dgraph()
        self.save_plot()

    def save_plot(self, plot_name: str = "untitled"):

        class_name = type(self).__name__  # noqa: F841
        if plot_name == "untitled":
            plot_name = f"{self.name}_{self.last_xaxis}_vs_{self.last_yaxis}"

        save_path = os.path.join(self.projectdir, self.plot_dir, plot_name)
        print(save_path)
        counter = 0
        while os.path.exists(f"{save_path}.png"):
            counter += 1
            save_path = f"{save_path}_V{counter}"

        plt.savefig(save_path, dpi=300)

        plt.close()
        print(f"Graph saved to: {self.projectdir}{self.plot_dir}as {plot_name}.png")


if __name__ == "__main__":
    pass
