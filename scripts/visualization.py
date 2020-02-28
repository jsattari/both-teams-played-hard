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

data = data[['PLAYER_NAME', 'PTS', 'FGA', 'GAME_DATE_EST']]

data['GAME_DATE_EST'] = pd.to_datetime(data['GAME_DATE_EST'])

data['GAME_DATE_EST'] = data['GAME_DATE_EST'].dt.strftime('%Y')

# data = data.groupby('PLAYER_NAME')
# group the data and classify it for bokeh viz
# grouped_data = data.groupby('PLAYER_NAME').agg(
#    {'PTS': ['min', 'max', 'mean', 'var', 'median'], 'FGA': 'sum','GAME_DATE_EST':['min', 'max']})
source = ColumnDataSource(data={
    'x': data.loc[2003].PTS,
    'y': data.loc[2003].FGA,
    'player': data.loc[2003].PLAYER_NAME
    })

# determining plot attributes
p = figure(
    plot_width=700, plot_height=500, toolbar_location="right", title="Scoring Efficiency"
)

# setting axis
p.square(
    x='x', y='y', source=source, size=5
)

# determining hovertool 'hovers'
hover_tool = HoverTool(
    tooltips=[
        ('player_name', '@player')]
)

# determining slider 
slider = Slider(
    start=2003, end=2020, value=2003, step=1, title="Year"
)

# Define a callback function: callback
def callback(attr, old, new):
    yr = slider.value
    new_data = {
        'x': data.loc[yr].PTS,
        'y': data.loc[yr].FGA,
        'player': data.loc[yr].PLAYER_NAME
    }
 
    # Update source with the new data values
    source.data = new_data

slider.on_change('value', callback)

# adding hovertool to glyph
p.add_tools(hover_tool)

layout = column(slider, p)
curdoc().add_root(layout)

show(layout)
