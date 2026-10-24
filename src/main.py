import pandas as pd
import plotly.express as px

import init
import utils
from data_struct import EmpData

# import scipy
# import matplotlib.pyplot as plt

init.uninit_state()
init.init_state()
raw_data = utils.get_data()
print(raw_data["FreeFallData.csv"])


FF_data = utils.LabDataSet("FreeFallData.csv")

time_points = FF_data["time (sec)"]
height_points = FF_data["height (sec)"]

Time = EmpData.from_abs_uncertainty(time_points, (0, 0, 1, 0, 0, 0, 0), 1, 0.1)
Height = EmpData.from_abs_uncertainty(height_points, (1, 0, 0, 0, 0, 0, 0, 0), 1, 0.1)

Data = pd.DataFrame({"Time": Time, "Height": Height})
print()
# FF_data.CDS_graph("time (sec)", "height (m)", figsize=(5, 5))

fig = px.scatter(FF_data, FF_data["time (sec)"], FF_data["height (m)"])
fig.show()
