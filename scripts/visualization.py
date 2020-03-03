import pandas as pd
import os
from bokeh.io import output_file, show, curdoc
from bokeh.models import ColumnDataSource, HoverTool, Slope
from bokeh.models.widgets import Select, Slider
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import row

# path to data file
data = pd.read_csv(
    os.path.dirname(os.getcwd()) + '/Versus/data/merged_games.csv', index_col=False
)

# Col_Names:
# 'TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_ID', 'PLAYER_NAME',
# 'START_POSITION', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A',
# 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL',
# 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS', 'GAME_DATE_EST', 'COURT'

# selecting which columns to include in dataset
filtered = data[['PLAYER_NAME', 'PTS', 'FGA', 'GAME_DATE_EST', 'FGM', 'COURT']]

# formatting 'game_date_est' col for datetime, changing to show only year
filtered['GAME_DATE_EST'] = pd.to_datetime(filtered['GAME_DATE_EST'], format='%Y-%m-%d')
filtered['GAME_DATE_EST'] = filtered['GAME_DATE_EST'].dt.year

# fill blanks with 0s
filtered.fillna(0)

# declare source data for glyphs
source = ColumnDataSource(filtered[filtered['GAME_DATE_EST'] == 2003])

# coloring
# index_cmap = factor_cmap(
#     'COURT', palette=['red', 'blue', 'yellow'],
#     factors=sorted(filtered['COURT'].unique()), end=1)

# determining figure attributes
p = figure(
    plot_width=700, plot_height=500,
    toolbar_location="above", title="Scoring Efficiency by Totals",
    title_location='above')

p.title.text_font_size = '25px'
p.title.text_color = 'red'
p.xaxis.axis_label = 'Total_Points'
p.yaxis.axis_label = 'Total_Field_Goal_Attempts'

# setting axis
p.square(
    x='PTS', y='FGA', size=5, source=source)

# determining hovertool 'hovers'
hover_tool = HoverTool(
    tooltips=[
        ('Player', '@PLAYER_NAME'),
        ('Total_Points', '@PTS'),
        ('Total_FGM', '@FGM'),
        ('Total_FGA', '@FGA'),
        ('Location','@COURT')])

# adding hovertool to glyph
p.add_tools(hover_tool)

# creating slider
slider = Slider(
    start=filtered['GAME_DATE_EST'].min(),
    end=filtered['GAME_DATE_EST'].max(),
    value=filtered['GAME_DATE_EST'].min(), step=1, title="Season")

# slider call back function
def slider_update(attr, old, new):
    new_year = slider.value
    new_data = ColumnDataSource(filtered[filtered['GAME_DATE_EST'] == new_year])
    source.data = new_data.data


slider.on_change('value', slider_update)

layout = row(
    slider, p)

show(layout)
