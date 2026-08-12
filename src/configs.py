from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
# DEV CONSTANTS
VERSION = "1.0.0"
# PROJECT SPECIFIC CONFIGS (DONE DURING USE)


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


print(f"RECORDED DATA = {RECORDED_DATA_CONFIGS}")
print("\n")
