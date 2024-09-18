from shiny.express import input, render, ui
from shinywidgets import render_widget  
from ipyleaflet import GeoJSON, Map, Marker
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geojson
import folium

# run download.py
import download

median_postcode_pd = pd.read_csv("../data/raw/median_price_per_postcode.csv")

with open("../data/landing/geodata/suburbs.geojson", "r") as f:
    geojson_suburbs = geojson.load(f)

def postcode_highlight(feature):
    postcode = feature["properties"]["mccid_int"]
    if int(postcode) == input.postcode():
        return {"color":"white", "fillColor":"red"}
    return {"color":"white", "fillColor":"black"}

with ui.sidebar():
    ui.input_selectize("var", "Select Column", choices = list(median_postcode_pd.columns.values))
    ui.input_slider("bins", "Number of Bins", min=5, max=50, value=10)
    ui.input_numeric("postcode", "Input Postcode", 3000)

@render.plot
def hist():
    sns.displot(median_postcode_pd, x = input.var(), bins = input.bins())

with ui.card():
    @render_widget  
    def map():
        map_melb = Map(center=(-37.8082, 144.96332), zoom=12)

        geo_json = GeoJSON(  
            data=geojson_suburbs,  
            style={  
                "opacity": 1,  
                "dashArray": "9",  
                "fillOpacity": 0.2,  
                "weight": 1,  
            },
            hover_style={"color": "white", "dashArray": "0", "fillOpacity": 0.5},
            style_callback = postcode_highlight
        ) 
        map_melb.add_layer(geo_json)
        
        return map_melb