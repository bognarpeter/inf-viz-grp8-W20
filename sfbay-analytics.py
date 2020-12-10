#!/usr/bin/env python3

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

from bokeh.models.widgets import Div
from bokeh.layouts import gridplot
from bokeh.io import curdoc
from bokeh.models import CustomJS, Slider, RangeSlider

import pandas as pd
import os

# constants
DATA_PATH = "data/"
FILE_NAME = "sfbay_final.csv"
INITIAL_YEAR = 2000
INITIAL_MONTH = 5
INITIAL_DEPTH = 5
INITIAL_SURR = 3
INITIAL_MIN_DEPTH = INITIAL_DEPTH - INITIAL_SURR / 2
INITIAL_MAX_DEPTH = INITIAL_DEPTH + INITIAL_SURR / 2


def get_data():
    data_path = os.path.join(DATA_PATH, FILE_NAME)
    return pd.read_csv(data_path, delimiter=",")


def get_initial_data(df):
    df_selected = df[
        (pd.to_datetime(df["TimeStamp"]).dt.year == INITIAL_YEAR)
        & (pd.to_datetime(df["TimeStamp"]).dt.month == INITIAL_MONTH)
        & (df["Depth"] >= INITIAL_MIN_DEPTH)
        & (df["Depth"] <= INITIAL_MAX_DEPTH)
    ]

    df_grouped = df_selected.groupby(["Stations"]).mean()

    return ColumnDataSource(data=df_grouped)


def update_data(attrname, old, new):

    # Get the current slider values
    year = year_slider.value
    month = month_slider.value
    depth = depth_slider.value
    surr = surrounding_depth_slider.value

    min_depth = depth - surr / 2
    max_depth = depth + surr / 2

    sfbay_selected = sfbay[
        (pd.to_datetime(sfbay["TimeStamp"]).dt.year == year)
        & (pd.to_datetime(sfbay["TimeStamp"]).dt.month == month)
        & (sfbay["Depth"] >= min_depth)
        & (sfbay["Depth"] <= max_depth)
    ]

    sfbay_grouped = sfbay_selected.groupby(["Stations"]).mean()

    source.data = sfbay_grouped


def create_figure(title, tooltips):
    return figure(
        title=title,
        x_axis_type="mercator",
        y_axis_type="mercator",
        x_axis_label="Longitude",
        y_axis_label="Latitude",
        tooltips=tooltips,
    )


def create_cmap(palette, field):
    return linear_cmap(
        field_name=field,
        palette=palette,
        low=sfbay[field].min(),
        high=sfbay[field].max(),
    )


def create_colorbar(color_mapper):
    return ColorBar(
        color_mapper=color_mapper["transform"],
        formatter=NumeralTickFormatter(format="0.0[0000]"),
        label_standoff=13,
        width=8,
        location=(0, 0),
    )


def create_figure_wrapper(source, field_name, palette, tile, circle_size=15):

    MONO_COLOR = False

    if isinstance(palette, str):
        MONO_COLOR = True

    if MONO_COLOR:
        color_mapper = palette
    else:
        color_mapper = create_cmap(palette, field_name)

    # Create figure
    tooltips = [("Station Number", "@Stations")]
    if field_name != "Stations":
        tooltips.append((field_name, f"@{field_name}"))

    title = f"{field_name} @ San Francisco Bay Area"
    fig = create_figure(title, tooltips)

    # Add map tile
    fig.add_tile(tile)

    # Add points using mercator coordinates
    fig.circle(
        x="mercator_x",
        y="mercator_y",
        color=color_mapper,
        source=source,
        size=circle_size,
        line_color="#000000",
        line_width=1.5,
        fill_alpha=0.7,
    )

    if not MONO_COLOR:
        # Defines color bar
        color_bar = create_colorbar(color_mapper)
        # Set color_bar location
        fig.add_layout(color_bar, "right")

    return fig


def create_figures():
    default_tile = get_provider(Vendors.CARTODBPOSITRON_RETINA)

    temperature_field_name = "Temperature"
    temperature_palette = RdYlBu[11]
    temperature = create_figure_wrapper(
        source, temperature_field_name, temperature_palette, default_tile
    )

    salinity_field_name = "Salinity"
    salinity_palette = PuOr[11]
    salinity = create_figure_wrapper(
        source, salinity_field_name, salinity_palette, default_tile
    )

    fluorescence_field_name = "Fluorescence"
    fluorescence_palette = PiYG[11]
    fluorescence = create_figure_wrapper(
        source, fluorescence_field_name, fluorescence_palette, default_tile
    )

    station_tile = get_provider(Vendors.OSM)
    station_field_name = "Stations"
    station_palette = "blue"
    stations = create_figure_wrapper(
        source, station_field_name, station_palette, station_tile, circle_size=10
    )

    return temperature, salinity, fluorescence, stations


def create_widgets(sfbay):
    timestamp_col = pd.to_datetime(sfbay["TimeStamp"])

    sfbay_year = timestamp_col.dt.year
    max_year = max(sfbay_year)
    min_year = min(sfbay_year)

    sfbay_month = timestamp_col.dt.month
    max_month = max(sfbay_month)
    min_month = min(sfbay_month)

    sfbay_depth = sfbay["Depth"]
    max_depth = sfbay_depth.max()
    min_depth = sfbay_depth.min()

    year_slider = Slider(
        title="Year of the Measurement",
        start=min_year,
        end=max_year,
        step=1,
        value=INITIAL_YEAR,
    )
    month_slider = Slider(
        title="Month of the Measurement",
        start=min_month,
        end=max_month,
        step=1,
        value=INITIAL_MONTH,
    )
    depth_slider = Slider(
        title="Water Depth in Meters",
        start=min_depth,
        end=max_depth,
        step=0.5,
        value=INITIAL_DEPTH,
    )
    surrounding_depth_slider = Slider(
        title="Surrounding Water for Depth in Meters",
        start=0,
        end=3,
        step=0.5,
        value=INITIAL_SURR,
    )

    return year_slider, month_slider, depth_slider, surrounding_depth_slider


def construct_html(elements):

    page_title = Div(
        text="""Water Quality at
    the SF Bay-Area""",
        width=350,
        height=100,
        style={
            "font-size": "25pt",
            "color": "#0086b3",
            "font-weight": "bold",
            "text-align": "left",
            "font-family": "Arial, Helvetica, sans-serif",
        },
    )

    description = Div(
        text="""The graphics below depict important measurements of water quality in
    the San Francisco Bay Area from 1994 to 2004.
    Interact with the graphs by navigating, zooming, or setting the time period for the data collection. """,
        width=500,
        height=100,
    )

    space = Div(text="""""", width=50, height=100)

    intro = column(page_title, description)
    left_top = row(space, intro)

    left_grid = column(left_top, elements["stations"])
    right_grid = gridplot(
        [
            [elements["salinity"], elements["controls"]],
            [elements["temperature"], elements["fluorescence"]],
        ],
        plot_width=450,
        plot_height=400,
    )

    return left_grid, right_grid


### CREATE FIGURES ###
sfbay = get_data()
source = get_initial_data(sfbay)
temperature, salinity, fluorescence, stations = create_figures()

### CREATE WIDGETS ###
year_slider, month_slider, depth_slider, surrounding_depth_slider = create_widgets(
    sfbay
)
widgets = [year_slider, month_slider, depth_slider, surrounding_depth_slider]
controls = column(widgets)
for widget in widgets:
    widget.on_change("value", update_data)

### CONSTRUCT HTML ###
left_grid, right_grid = construct_html(
    {
        "stations": stations,
        "salinity": salinity,
        "temperature": temperature,
        "fluorescence": fluorescence,
        "controls": controls,
    }
)
curdoc().add_root(row(left_grid, right_grid))
curdoc().title = "Bay Area Water Quality"
