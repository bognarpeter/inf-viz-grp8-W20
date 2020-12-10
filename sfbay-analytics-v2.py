from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import RdYlBu, PuOr, PiYG
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.layouts import row, column
from bokeh.models import (
    GeoJSONDataSource,
    LinearColorMapper,
    ColorBar,
    NumeralTickFormatter,
)
import numpy as np
import pandas as pd
import os

from bokeh.models.widgets import Div



DATA_PATH = "./Info_VIZ/data/"
sfbay_data = "sfbay_final.csv"

# Read in data
sfbay_data_path = os.path.join(DATA_PATH, sfbay_data)
sfbay = pd.read_csv(sfbay_data_path, delimiter=",")

# Select map style to use
chosentile = get_provider(Vendors.CARTODBPOSITRON_RETINA)




####################################################################################################


#### input daterange Slider
from datetime import date
from bokeh.models.widgets import DateRangeSlider
from bokeh.io import curdoc

##input a range slider

from bokeh.io import show
from bokeh.models import CustomJS, Slider, RangeSlider

range_slider = RangeSlider(start=0, end=10, value=(1,9), step=.1, title="Stuff")
range_slider.js_on_change("value", CustomJS(code="""
    console.log('range_slider: value=' + this.value, this.toString())
"""))



year=1990
month=5


sfbay = pd.read_csv(sfbay_data_path, delimiter=",")
sfbay = sfbay[pd.to_datetime(sfbay['TimeStamp']).dt.year == year]
sfbay = sfbay[pd.to_datetime(sfbay['TimeStamp']).dt.month == month]
source = ColumnDataSource(data=sfbay)



##################################################################################



################ CREATING THE TEMPERATURE MAP ####################################

#setting the palette for the temperature
temperature_palette = RdYlBu[11]
palette = PuOr[11]
palette = PiYG[11]


# Define color mapper - which column will define the colour of the data points
color_mapper = linear_cmap(
    field_name="Temperature",
    palette=temperature_palette,
    low=sfbay["Temperature"].min(),
    high=sfbay["Temperature"].max(),
)

# Set tooltips - these appear when we hover over a data point in our map
tooltips = [("Temperature", "@Temperature"), ("stat_num", "@stat_num")]

# Create figure
temperature = figure(
    title="Temperature @ San Francisco Bay Area",
    x_axis_type="mercator",
    y_axis_type="mercator",
    x_axis_label="Longitude",
    y_axis_label="Latitude",
    tooltips=tooltips,
)

# Add map tile
temperature.add_tile(chosentile)

# Add points using mercator coordinates
temperature.circle(
    x="mercator_x",
    y="mercator_y",
    color=color_mapper,
    source=source,
    size=20,
    line_color="#000000",
    line_width=1.5,
    fill_alpha=0.7,
)

# Defines color bar
temperature_color_bar = ColorBar(
    color_mapper=color_mapper["transform"],
    formatter=NumeralTickFormatter(format="0.0[0000]"),
    label_standoff=13,
    width=8,
    location=(0, 0),
)
# Set color_bar location
temperature.add_layout(temperature_color_bar, "right")


################ CREATING THE Salinity MAP ####################################

#setting the palette for the temperature
slinity_palette = PuOr[11]
palette = PiYG[11]


# Define color mapper - which column will define the colour of the data points
color_mapper = linear_cmap(
    field_name="Salinity",
    palette=slinity_palette,
    low=sfbay["Salinity"].min(),
    high=sfbay["Salinity"].max(),
)

# Set tooltips - these appear when we hover over a data point in our map
tooltips = [("Salinity", "@Salinity"), ("stat_num", "@stat_num")]

# Create figure
salinity = figure(
    title="Salinity @ San Francisco Bay Area",
    x_axis_type="mercator",
    y_axis_type="mercator",
    x_axis_label="Longitude",
    y_axis_label="Latitude",
    tooltips=tooltips,
)

# Add map tile
salinity.add_tile(chosentile)

# Add points using mercator coordinates
salinity.circle(
    x="mercator_x",
    y="mercator_y",
    color=color_mapper,
    source=source,
    line_color="#000000",
    line_width=1.5,
    size=20,
    fill_alpha=0.7,
)

# Defines color bar
salinity_color_bar = ColorBar(
    color_mapper=color_mapper["transform"],
    formatter=NumeralTickFormatter(format="0.0[0000]"),
    label_standoff=13,
    width=8,
    location=(0, 0),
)
# Set color_bar location
salinity.add_layout(salinity_color_bar, "right")


################ CREATING THE Fluorescence MAP ####################################

#setting the palette for the temperature
fluorescence_palette = PiYG[11]


# Define color mapper - which column will define the colour of the data points
color_mapper = linear_cmap(
    field_name="Fluorescence",
    palette=fluorescence_palette,
    low=sfbay["Fluorescence"].min(),
    high=sfbay["Fluorescence"].max(),
)

# Set tooltips - these appear when we hover over a data point in our map
tooltips = [("Fluorescence", "@Fluorescence"), ("stat_num", "@stat_num")]

# Create figure
fluorescence = figure(
    title="Fluorescence @ San Francisco Bay Area",
    x_axis_type="mercator",
    y_axis_type="mercator",
    x_axis_label="Longitude",
    y_axis_label="Latitude",
    tooltips=tooltips,
)

# Add map tile
fluorescence.add_tile(chosentile)

# Add points using mercator coordinates
fluorescence.circle(
    x="mercator_x",
    y="mercator_y",
    color=color_mapper,
    source=source,
    size=20,
    line_color="#000000",
    line_width=1.5,
    fill_alpha=0.7,
)

# Defines color bar
fluorescence_color_bar = ColorBar(
    color_mapper=color_mapper["transform"],
    formatter=NumeralTickFormatter(format="0.0[0000]"),
    label_standoff=13,
    width=8,
    location=(0, 0),
)
# Set color_bar location
fluorescence.add_layout(fluorescence_color_bar, "right")


################ CREATING the Overview MAP ########################################

# Select map style to use
chosentile_overview = get_provider(Vendors.OSM)

# Create figure
stations = figure(
    title="Stations @ San Francisco Bay Area",
    x_axis_type="mercator",
    y_axis_type="mercator",
    x_axis_label="Longitude",
    y_axis_label="Latitude",
    tooltips=tooltips,
)

# Add map tile
stations.add_tile(chosentile_overview)

# Add points using mercator coordinates
stations.circle(
    x="mercator_x",
    y="mercator_y",
    color="red",
    source=source,
    size=20,
    fill_alpha=0.7,
)

############################# ADDING Controls #######################################



space_1 = Div(text="""""",width=50, height=100)
space_2 = Div(text="""""",width=30, height=200)
year_slider = Slider(title="Year of the Measurement", start = 1994, end = 2014, step=1, value=1997)
month_slider = Slider(title="Month of the Measurement", start = 1, end = 12, step=1, value=7)
depth_slider = Slider(title="Water Depth in Meters", start = 1, end = 6, step=1, value=2)
controls = column(space_1, year_slider, month_slider, depth_slider)
#contols = row(space_2, controls_1)

############################# ADDING Controls #######################################



page_title = Div(text="""Water Quality at 
the SF Bay-Area""",
                 width=350, height=100, style={'font-size':'25pt',
                                               'color': '#0086b3',
                                               'font-weight': 'bold',
                                               'text-align': 'left',
                                               'font-family': 'Arial, Helvetica, sans-serif',})


description = Div(text="""The graphics below depict important measurements of water quality in
the San Francisco Bay Area from 1994 to 2004. 
Interact with the graphs by navigating, zooming, or setting the time period for the data collection. """,
                  width=500, height=100)

space = Div(text="""""",width=50, height=100)

intro_1 = column(page_title, description)
intro_2 = row(space,intro_1)




# Display in notebook
#output_notebook()
# Save as HTML
output_file('sfbay.html', title='Default Title')

from bokeh.layouts import gridplot
grid_1 = column(intro_2, stations)
grid_2 = gridplot([[salinity, controls], [temperature, fluorescence]], plot_width=450, plot_height=400)

## Show map and slider

curdoc().title = "Bay Area"
show(row(grid_1, grid_2))
#show(row(p,slider))