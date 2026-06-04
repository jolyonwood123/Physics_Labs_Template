import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
from dotenv import load_dotenv
import json
import time
load_dotenv()
raw_configs = os.getenv("DATA_CONFIGS", '{}')
data_configs = json.loads(raw_configs)
plot_dir = str(os.getenv("PLOTSDIR"))
print(plot_dir)
filenames = []

def get_data(data_configs:dict=data_configs):
    DATA_DIR = Path(__file__).resolve().parent / 'data'
    data_store = {}
    
    for filename, row_remove in data_configs.items():
        path = DATA_DIR / f"{filename}.csv"
        if path.exists():
            data_store[filename] = pd.read_csv(path, skiprows=row_remove)
            filenames.append(filename)
    return data_store
        
class BaseLab:
    
    def __init__(self, filename:str, plot_dir=plot_dir):
        self._df = data_store[filename]
        self.name = filename
        self.projectdir = os.path.dirname(os.path.abspath(__file__))
        self.plot_dir = self.projectdir + plot_dir


        
        print(self.projectdir)
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)
        


    def timeit(self, func, *args, **kwargs ):
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

    def converter(self, column: str, target_units_in_units: int=1, data_units: int=1):
        df = self._df
        data = self._df[column]
        conversion_factor = data_units / target_units_in_units
        self._df[column] = data * conversion_factor
        return self._df[column]
    
    def create_2dgraph(self, xaxis: str, yaxis: str, figsize:tuple=(10,10)):
        df = self._df
        self.last_xaxis = xaxis
        self.last_yaxis = yaxis

        plt.figure(figsize=figsize)
        plt.plot(df[xaxis], df[yaxis], label="", color='red')
        plt.title(f"{yaxis.upper().replace("_", " ")} vs {xaxis.upper().replace("_", " ")}")
        plt.xlabel(xaxis.replace("_", " "))
        plt.ylabel(yaxis.replace("_", " "))
        plt.grid(True)          
        plt.legend()
        return plt, xaxis, yaxis
        
        
    def display_2dgraph(self):
        plt.tight_layout()
        plt.show()
    def save_plot(self, plot_name:str="untitled"):

        class_name = type(self).__name__
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

    
        
        
   
        
        


    
data_store = get_data()
test = BaseLab('kinematics')

# print(test.converter('velocity_mps', 1000))
print(test.timeit(test.create_2dgraph, 'distance_m', 'velocity_mps'))
test.save_plot()











 









