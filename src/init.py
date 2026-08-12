import json
from datetime import datetime as dt
from datetime import timezone
from pathlib import Path

import configs as conf
from utils import get_date

project_name = conf.PROJECT_NAME


class State:
    def __init__(self):
        self.state_path = conf.STATE_DIR
        with open(self.state_path / "log_template.md", encoding="utf-8") as template:
            self.template_json = template.read()
        with open(self.state_path / "UnInit_state.json") as uninitialised:
            self.uninit = uninitialised.read()
        with open(self.state_path / "project_state.json") as file:
            self.state = file.read()

    def uninitialise(self):
        with open(self.state_path / "UnInit_state.json") as uninitialised:
            self.state = json.load(uninitialised)

        self.update_project_state(self.state)

    def get_brief(self) -> str:
        with open(self.state_path / "brief.md") as file:
            self.brief = str(file.read())
        return self.brief

    def update_project_state(self, new_state: dict) -> None:
        with open(self.state_path / "project_state.json", "w") as file:
            json.dump(new_state, file, indent=2)

    def read_project_state(self) -> dict:
        with open(self.state_path / "project_state.json") as file:
            state = json.load(file)
        return state

    def read_file_metadata(self, file_name: str):
        file = Path(file_name)
        info = file.stat()

        return {
            "name": file.name,
            "size_bytes": info.st_size,
            "modified": dt.fromtimestamp(info.st_mtime, tz=timezone.utc),
            "is_file": file.is_file(),
            "extension": file.suffix,
        }

    def get_dataset_list(self):
        data_sets_str = ""
        for name in conf.RECORDED_DATA_CONFIGS:
            info = self.read_file_metadata(name)
            data_sets_str += (
                f"|{info['name']}|{info['size_bytes']}|{info['modified']}|Recorded|\n"
            )
        for name in conf.REFERENCE_DATA_CONFIGS:
            info = self.read_file_metadata(name)
            data_sets_str += (
                f"|{info['name']}|{info['size_bytes']}|{info['modified']}|Reference|\n"
            )
        print(data_sets_str)
        return data_sets_str

    def initialise(self) -> None:
        self.brief: str = self.get_brief()
        self.state: dict = self.read_project_state()
        if self.state["INIT"] is True:
            print("State initialised already")
            self.state["OVERVIEW"] = self.get_brief()
            data_sets_str = ""

        else:
            date = get_date()
            data_sets_str = self.get_dataset_list()

            project_info = {
                "INIT": True,
                "FOLDER_NAME": conf.PROJECT_NAME,
                "FIRST_UPDATED": dt.today().strftime(conf.DISPLAY_DATE_FORMAT),
                "LAST_UPDATED": dt.today().strftime(conf.DISPLAY_DATE_FORMAT),
                "OVERVIEW": self.get_brief(),
                "DATASET_LIST": data_sets_str,
                "LOG_ENTRIES": [
                    f"|{date}|{conf.VERSION}| Started project and initialised workspace|"
                ],
            }

            self.update_project_state(project_info)

    def create_log_str(self, logs: list):
        current_state = self.read_project_state()
        log_str = ""
        for line in current_state["LOG_ENTRIES"]:
            log_str += line + "\n"
            print(log_str)
        return log_str

    def log_state(self, log: str) -> None:
        # reads the state json appends a log to the log key (list) then writes this new json back.
        date = get_date()
        current_state = self.read_project_state()

        new_log = f"|{date}|{conf.VERSION}|{log}|"

        data_sets_str = self.get_dataset_list()
        current_state["DATASET_LIST"] = data_sets_str
        current_state["LOG_ENTRIES"].append(new_log)

        self.update_project_state(current_state)

    def output_md(self) -> None:
        with open(self.state_path / "log_template.md", encoding="utf-8") as file:
            template: str = file.read()
        current_state = self.read_project_state()
        log_str = self.create_log_str(current_state["LOG_ENTRIES"])
        current_state["LOG_ENTRIES"] = log_str
        lab_md = template.format_map(current_state)
        with open(
            self.state_path / f"{conf.PROJECT_NAME}.md", "w", encoding="utf-8"
        ) as file:
            file.write(lab_md)


def init_state() -> int:

    # TEST OF DATA RETRIEVAL AND PLOTTING FUNCTIONALITY
    #
    # test = BaseLab("kinematics")
    # print(test.timeit(test.create_2dgraph, "distance_m", "velocity_mps"))
    # test.save_plot()
    try:
        state = State()
        state.initialise()
        print(state.read_project_state())
        state.output_md()
    except Exception as e:  # noqa: BLE001
        print(f"STATE INITIALISING FAILED: {e}")

    return 0


def log_state(log: str):
    state = State()
    state.log_state(log)


def reload_state():
    state = State()
    state.read_project_state()


init_state()
log_state("WASSSSUUPPPPP")
