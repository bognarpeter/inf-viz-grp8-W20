from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import PRGn, RdYlGn
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

DATA_PATH = "data"
sfbay_data = "sfbay_final.csv"

# Read in data
sfbay_data_path = os.path.join(DATA_PATH, sfbay_data)
sfbay = pd.read_csv(sfbay_data_path, delimiter=",")

# Select tile set to use
chosentile = get_provider(Vendors.STAMEN_TONER)
# Choose palette
# palette = PRGn[11]
palette = PRGn[11]
source = ColumnDataSource(data=sfbay)

# Define color mapper - which column will define the colour of the data points
color_mapper = linear_cmap(
    field_name="Temperature",
    palette=palette,
    low=sfbay["Temperature"].min(),
    high=sfbay["Temperature"].max(),
)

# Set tooltips - these appear when we hover over a data point in our map
tooltips = [("Temperature", "@Temperature"), ("stat_num", "@stat_num")]

# Create figure
p = figure(
    title="Title",
    x_axis_type="mercator",
    y_axis_type="mercator",
    x_axis_label="Longitude",
    y_axis_label="Latitude",
    tooltips=tooltips,
)

# Add map tile
p.add_tile(chosentile)

# Add points using mercator coordinates
p.circle(
    x="mercator_x",
    y="mercator_y",
    color=color_mapper,
    source=source,
    size=30,
    fill_alpha=0.7,
)

# Defines color bar
color_bar = ColorBar(
    color_mapper=color_mapper["transform"],
    formatter=NumeralTickFormatter(format="0.0[0000]"),
    label_standoff=13,
    width=8,
    location=(0, 0),
)
# Set color_bar location
p.add_layout(color_bar, "right")

# Display in notebook
# output_notebook()
# Save as HTML
# output_file('sfbay.html', title='Default Title')

# Show map
show(p)
