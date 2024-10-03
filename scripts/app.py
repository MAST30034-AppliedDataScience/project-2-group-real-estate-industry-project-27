from shiny.express import input, render, ui
from shinywidgets import render_widget  
from ipyleaflet import GeoJSON, Map, Marker
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
import seaborn as sns
import geojson
import folium

# run download.py
#import download

median_postcode_pd = pd.read_csv("../data/raw/median_price_per_postcode.csv")
historical_price_pd = pd.read_csv("../data/raw/cleaned all properties.csv")

df_melted = historical_price_pd.reset_index().melt(id_vars=['suburb'])
df_melted = df_melted[df_melted["variable"] != "index"]
df_melted = df_melted.replace("Dec 2003.1", "Dec 2003")
df_melted["variable"] = pd.to_datetime(df_melted["variable"])
df_melted = df_melted.rename(columns = {"suburb":"Suburb", "variable":"Date", "value":"Price"})

with open("../data/landing/geodata/suburbs.geojson", "r") as f:
    geojson_suburbs = geojson.load(f)

def postcode_highlight(feature):
    postcode = feature["properties"]["mccid_int"]
    if int(postcode) == input.postcode():
        return {"color":"white", "fillColor":"green"}
    return {"color":"white", "fillColor":"black"}

def median_rental_colour(feature):
    postcode = feature["properties"]["mccid_int"]
    df_median_price = median_postcode_pd[median_postcode_pd["postcode"] == int(postcode)]
    if df_median_price.empty:
        return {"color":"white", "fillColor":"black"}   
    median_price_max = max(median_postcode_pd[input.var()])
    median_price_min = min(median_postcode_pd[input.var()])
    price_col = (df_median_price[input.var()] - median_price_min) / (median_price_max - median_price_min)
    hex_col = colors.to_hex(cm.YlOrRd(float(max(price_col)))) 
    return {"color":"white", "fillColor":hex_col}

def highlight_selected_by_price(feature):
    postcode = feature["properties"]["mccid_int"]
    df_median_price = median_postcode_pd[median_postcode_pd["postcode"] == int(postcode)]
    if df_median_price.empty:
        return {"color":"white", "fillColor":"black"}
    price_min, price_max = input.price()
    if price_min <= max(df_median_price[input.var()]) <= price_max:
        return {"color":"white", "fillColor":"green"}
    return {"color":"white", "fillColor":"black"}    

def list_median(suburb, historical):
    historical_subset = historical[historical["suburb"] == suburb]
    historical_subset = historical_subset.T.drop("suburb")
    historical_subset["x"] = range(0, historical_subset.shape[0])
    historical_subset = historical_subset.rename(columns = {historical_subset.columns[0]:"y"})
    return historical_subset

with ui.sidebar():
    hist_choices = list(median_postcode_pd.columns.values)
    suburb_choices = ["all"] + historical_price_pd["suburb"].tolist()
    ui.input_checkbox("hist_check", "Filter Histogram by Suburb?\n(Warning: may result in sparse graphs)", False)
    ui.input_selectize("var", "Select Rental Type", choices = hist_choices[2:])
    ui.input_selectize("suburb", "Select Suburb", choices = suburb_choices)
    ui.input_selectize("map_type", "Select Map Display Type", choices = ["Postcode", "Median Price", "Filter Price"])
    ui.input_numeric("postcode", "Input Postcode", 3000)
    ui.input_slider("price", "Price Range Highlight", min=0, max=1000, value=[200,500])

@render.plot
def hist():
    if input.suburb() == "all" or not input.hist_check():
        displt = sns.displot(median_postcode_pd, x = input.var(), bins = 20)
    else:
        df_median_subset = median_postcode_pd[median_postcode_pd["suburb"] == input.suburb().upper()]
        displt = sns.displot(df_median_subset, x = input.var(), bins = 20)
    displt.figure.suptitle("Median Rental Price: " + input.var())

@render.plot
def line():
    if input.suburb() == "all":
        lplot = sns.lineplot(data = df_melted, x = "Date", y = "Price", hue="Suburb")
    else:
        df_melted_subset = df_melted[df_melted["Suburb"] == input.suburb()]
        lplot = sns.lineplot(data = df_melted_subset, x = "Date", y = "Price", hue="Suburb")

    lplot.set(xlabel = "time", ylabel = "median price")
    lplot.figure.suptitle("Median Rental Price over Time (" + input.suburb() + ")")
    lplot.get_legend().set_visible(False)

    
with ui.card():
    @render_widget  
    def map():
        map_melb = Map(center=(-37.8082, 144.96332), zoom=12)
        match input.map_type():
            case "Postcode": style_func = postcode_highlight
            case "Median Price": style_func = median_rental_colour
            case "Filter Price": style_func = highlight_selected_by_price

        geo_json = GeoJSON(  
            data=geojson_suburbs,  
            style={  
                "opacity": 1,  
                "dashArray": "9",  
                "fillOpacity": 0.5,  
                "weight": 1,  
            },
            hover_style={"color": "white", "dashArray": "0", "fillOpacity": 0.8},
            style_callback = style_func
        ) 
        map_melb.add_layer(geo_json)
        
        return map_melb