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
grouped_data = data.groupby('TEAM_ABBREVIATION').mean()
source = ColumnDataSource(grouped_data)

# determining plot attributes
p = figure(
    plot_width=700, plot_height=500, toolbar_location="right", title="Perfomance by Age"
    )

# setting axis
p.square(
    x='REB', y='PTS', source=source, size=5
    )

# determining hovertool 'hovers'
hover_tool = HoverTool(
    tooltips=[('avg_pts', '@PTS')]
    )

# adding hovertool to glyph
p.add_tools(hover_tool)

show(p)