from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
# DEV CONSTANTS
VERSION = "1.0.0"
# for unit conversion and look/output
UNIT_LOOKUP = {
    "Metre": (1, 0, 0, 0, 0, 0, 0),
    "Gram": (0, 1, 0, 0, 0, 0, 0),
    "Second": (0, 0, 1, 0, 0, 0, 0),
    "Ampere": (0, 0, 0, 1, 0, 0, 0),
    "Kelvin": (0, 0, 0, 0, 1, 0, 0),
    "Mole": (0, 0, 0, 0, 0, 1, 0),
    "Candela": (0, 0, 0, 0, 0, 0, 1),
    "Newton": (1, 1, -2, 0, 0, 0, 0),
    "Velocity": (1, 0, -1, 0, 0, 0, 0),
    "Joule": (1, 2, -2, 0, 0, 0, 0),
    "Pascal": (-1, 1, -2, 0, 0, 0, 0),
}

SI_UNITS = [("m", 0), ("kg", 1), ("s", 2), ("A", 3), ("K", 4), ("mol", 5), ("cd", 6)]
DERIVED_UNITS = {
    "N": (1, 1, -2, 0, 0, 0, 0),
    "J": (1, 2, -2, 0, 0, 0, 0),
    "Pa": (-1, 1, -2, 0, 0, 0, 0),
}
# PATH CONSTANTS
MAIN_DIR = Path(__file__).resolve().parent.parent
STATE_DIR = MAIN_DIR / "State"
PLOT_DIR = MAIN_DIR / "Plots"
TESTS_DIR = MAIN_DIR / "Tests"
DATA_SETS_DIR = MAIN_DIR / "DataRaw"

RECORDED_DATA_DIR = DATA_SETS_DIR / "Recorded"
REFERENCE_DATA_DIR = DATA_SETS_DIR / "Reference"
CLEAN_DATA_DIR = MAIN_DIR / "DataRaw"
PROCESSED_DATA_DIR = MAIN_DIR / "DataRaw"

PROJECT_NAME = MAIN_DIR.name
TEMPLATE_LOG = MAIN_DIR / "State" / "log_template"
PROJECT_LOG = MAIN_DIR / "State" / f"{PROJECT_NAME}.md"
DISPLAY_DATE_FORMAT = "%d-%m-%Y %H:%M"
PROJECT_STATE_PATH = MAIN_DIR / "State" / "project_state.json"

# PROJECT SPECIFIC CONFIGS (DONE DURING USE)
# name of data file and number of rows to remove KV pair
RECORDED_DATA_CONFIGS = [f for f in RECORDED_DATA_DIR.iterdir() if f.is_file()]
REFERENCE_DATA_CONFIGS = [f for f in REFERENCE_DATA_DIR.iterdir() if f.is_file()]
