import pandas as pd
import os
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Select
from bokeh.plotting import figure

# path to data file
data = pd.read_csv(
    os.path.dirname(os.getcwd()) + '/Versus/data/merged_games.csv', index_col=False
)

# group the data and classify it for bokeh viz
grouped_data = data.groupby('PLAYER_NAME').agg(
    {'PTS': ['min', 'max', 'mean', 'var', 'median'], 'FGA': 'mean'})
source = ColumnDataSource(grouped_data)
print(grouped_data.head())
print(grouped_data.columns)
# determining plot attributes
p = figure(
    plot_width=700, plot_height=500, toolbar_location="right", title="Perfomance by Age"
)

# setting axis
p.square(
    x='PTS_mean', y='PTS_var', source=source, size=5
)

# determining hovertool 'hovers'
hover_tool = HoverTool(
    tooltips=[('team', '@PLAYER_NAME'), ('avg_pts', '@PTS_mean'),
              ('median_pts', '@PTS_median')]
)

# adding hovertool to glyph
p.add_tools(hover_tool)

show(p)
