import pandas as pd
import os
from bokeh.io import output_file, show, curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Select, Slider
from bokeh.plotting import figure
from bokeh.layouts import row, column

# path to data file
data = pd.read_csv(
    os.path.dirname(os.getcwd()) + '/Versus/data/merged_games.csv', index_col=False
)

# group the data and classify it for bokeh viz
grouped_data = data.groupby('PLAYER_NAME').agg(
    {'PTS': ['min', 'max', 'mean', 'var', 'median'], 'FGA': 'sum','GAME_DATE_EST':['min', 'max']})
source = ColumnDataSource(grouped_data)

print(grouped_data.head())
print(grouped_data.columns)

# determining plot attributes
p = figure(
    plot_width=700, plot_height=500, toolbar_location="right", title="Scoring Efficiency"
)

# setting axis
p.square(
    x='PTS_mean', y='FGA_sum', source=source, size=5
)

# determining hovertool 'hovers'
hover_tool = HoverTool(
    tooltips=[('team', '@PLAYER_NAME'), ('avg_pts', '@PTS_mean'),
              ('total_fga', '@FGA_sum')]
)

# determining slider 
slider = Slider(
    start=2003, end=2020, value=2003, step=1, title="Year"
)

# Define a callback function: callback
def callback(attr, old, new):
 
    # Read the current value of the slider: scale
    scale = slider.value
 
    # Compute the updated y using np.sin(scale/x): new_y
    new_y = pd.np.sin(scale/x)
 
    # Update source with the new data values
    source.data = {'x': x, 'y': new_y}

slider.on_change('value', callback)

# adding hovertool to glyph
p.add_tools(hover_tool)

layout = column(slider, p)
curdoc().add_root(layout)

show(layout)
