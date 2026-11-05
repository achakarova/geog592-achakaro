## Homework 11 - JN to .py
## By Antoaneta Chakarova for GEOG592
## 11/05/2026

print("Importing Modules")
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

print("Accessing and downloading Census data")
statefp = "06" #California
url = "https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_county_500k.zip"
counties = gpd.read_file(url)

nc_counties = counties[counties["STATEFP"] == statefp].to_crs(5070).copy() #5070 is NAD83 - good option for lower 48 states
nc_counties = nc_counties.sort_values("NAME").reset_index(drop=True)

#Find the state name and abbreviation from the FIPS code
states_url = "https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_state_500k.zip"
states = gpd.read_file(states_url)
state_info = states[states["STATEFP"] == statefp].iloc[0]
state_name = state_info["NAME"]
state_abbr = state_info["STUSPS"]
print(state_name + " county boundaries loaded")

print("Loading MSHA mining data")
mines = pd.read_csv("AllMines.csv", encoding="latin1", low_memory=False) #has different encoding
mines = mines[mines["STATE"] == state_abbr].copy()
mines = mines.dropna(subset=["LONGITUDE", "LATITUDE"]).copy()

#longitude and latitude become map points, then use the same CRS as the counties
mines_points = gpd.GeoDataFrame(mines, geometry=gpd.points_from_xy(mines["LONGITUDE"], mines["LATITUDE"]), crs="EPSG:4326")
mines_points = mines_points.to_crs(nc_counties.crs)
print("Assigning mining records to counties")

#spatial join: keep only mines that fall within the selected state's counties
mines_by_county = gpd.sjoin(mines_points, nc_counties[["NAME", "geometry"]], how="inner", predicate="within")

print("Spatial join completed")
print("Mines with coordinates inside counties:", len(mines_by_county))

#MSHA uses PRIMARY_SIC instead of COMMODITY_CODE
commodity_names = {
    "Construction Sand and Gravel": "Sand and Gravel",
    "Sand, Common": "Sand",
    "Sand, Industrial NEC": "Industrial Sand",
    "Ground Silica": "Silica Sand",
    "Crushed, Broken Stone NEC": "Crushed Stone",
    "Crushed, Broken Granite": "Granite",
    "Crushed, Broken Limestone NEC": "Limestone",
    "Crushed, Broken Sandstone": "Sandstone",
    "Crushed, Broken Traprock": "Crushed Stone",
    "Crushed, Broken Slate": "Slate",
    "Crushed, Broken Marble": "Marble",
    "Dimension Stone NEC": "Dimension Stone",
    "Dimension Granite": "Granite",
    "Dimension Limestone": "Limestone",
    "Common Clays NEC": "Clay",
    "Clay, Ceramic, Refractory Mnls.": "Brick Clay",
    "Fire Clay": "Brick Clay",
    "Gold Ore": "Gold",
    "Silver Ore": "Silver",
    "Iron Ore": "Iron Ore",
    "Copper Ore NEC": "Copper",
    "Zinc": "Zinc",
    "Lead-Zinc Ore": "Zinc",
    "Tungsten Ore": "Tungsten",
    "Rare Earths Ore": "Rare Earths",
    "Lithium": "Lithium",
    "Talc": "Talc",
    "Pumice": "Pumice",
    "Gypsum": "Gypsum",
    "Boron Minerals": "Boron",
    "Gemstones": "Gemstone",
    "Mica": "Mica",
    "Feldspar": "Feldspar",
    "Peat": "Peat",
    "Salt": "Salt",
    "Salt, Brine Evaporated": "Salt",
    "Trona": "Trona",
    "Graphite": "Graphite",
    "Diatomaceous Earth (Diatomite)": "Diatomite",
    "Perlite": "Perlite",
    "Cement": "Cement",
    "Coal (Lignite)": "Coal"
}

mines_by_county["commodity"] = mines_by_county["PRIMARY_SIC"].map(commodity_names).fillna("Other/Unknown")

#Red will mean any mine that is NOT marked Active
commodity_colors = {
    "Sand and Gravel": "khaki",
    "Sand": "yellow",
    "Industrial Sand": "goldenrod",
    "Silica Sand": "palegoldenrod",
    "Crushed Stone": "gray",
    "Granite": "darkgray",
    "Limestone": "lightgray",
    "Sandstone": "tan",
    "Slate": "slategray",
    "Marble": "gainsboro",
    "Dimension Stone": "dimgray",
    "Clay": "peru",
    "Brick Clay": "sienna",
    "Gold": "gold",
    "Silver": "silver",
    "Iron Ore": "firebrick",
    "Copper": "chocolate",
    "Zinc": "lightsteelblue",
    "Tungsten": "steelblue",
    "Rare Earths": "mediumpurple",
    "Lithium": "plum",
    "Talc": "whitesmoke",
    "Pumice": "burlywood",
    "Gypsum": "ivory",
    "Boron": "lightcyan",
    "Gemstone": "mediumorchid",
    "Mica": "thistle",
    "Feldspar": "wheat",
    "Peat": "brown",
    "Salt": "azure",
    "Trona": "beige",
    "Graphite": "black",
    "Diatomite": "bisque",
    "Perlite": "linen",
    "Cement": "darkgray",
    "Coal": "black",
    "Other/Unknown": "lightskyblue"
}

#Number of mines by county (from the spatial join result)
county_summary = mines_by_county.groupby("NAME").size().rename("total_mines")
county_summary = nc_counties[["NAME"]].merge(county_summary, left_on="NAME", right_index=True, how="left")
county_summary["total_mines"] = county_summary["total_mines"].fillna(0)
print("Mining record counts calculated")


def county_map(county, ax):
    selected = nc_counties[nc_counties["NAME"] == county]
    county_mines = mines_by_county[mines_by_county["NAME"] == county]
    active = county_mines[county_mines["CURRENT_MINE_STATUS"] == "Active"]
    inactive = county_mines[county_mines["CURRENT_MINE_STATUS"] != "Active"]

    selected.plot(ax=ax, facecolor="whitesmoke", edgecolor="black")

    for commodity in active["commodity"].dropna().unique(): #plot each active commodity using its own color
        sites = active[active["commodity"] == commodity]
        sites.plot(ax=ax, color=commodity_colors.get(commodity, "lightskyblue"), markersize=28, label=commodity)

    if len(inactive) > 0: #Plot all non-active mine statuses in red
        inactive.plot(ax=ax, color="red", markersize=28, label="Not active")

    if len(county_mines) > 0: #Place the legend outside the map, on the right
        ax.legend(fontsize=9, loc="center left", bbox_to_anchor=(1.05, 0.5))

    ax.set_axis_off()


def locator_map(county, ax):
    selected = nc_counties[nc_counties["NAME"] == county]
    nc_counties.plot(ax=ax, facecolor="white", edgecolor="gray", linewidth=0.4)
    selected.plot(ax=ax, facecolor="steelblue", edgecolor="black")
    ax.set_axis_off()


def county_info(county, ax):
    county_mines = mines_by_county[mines_by_county["NAME"] == county]
    total = len(county_mines)
    inactive = len(county_mines[county_mines["CURRENT_MINE_STATUS"] != "Active"])

    sentence = "There are " + str(total) + " mine records in " + county + " County."
    sentence = sentence + "\n" + str(inactive) + " mines are not active."

    ax.text(0, 0.9, sentence, fontsize=16, va="top", transform=ax.transAxes)
    ax.set_axis_off()


def county_figure(county, pdf):
    fig = plt.figure(figsize=(8, 10))

    #Large county map on the left
    ax1 = fig.add_axes([0.05, 0.35, 0.62, 0.55])
    county_map(county, ax1)

    #Smaller state locator underneath
    ax2 = fig.add_axes([0.08, 0.16, 0.35, 0.16])
    locator_map(county, ax2)

    #Text underneath the maps
    ax3 = fig.add_axes([0.06, 0.05, 0.90, 0.10])
    county_info(county, ax3)

    fig.suptitle(county + " County", fontsize=22)

    pdf.savefig(fig)
    plt.close(fig)


print("Generating " + state_name + " Mining Atlas")
pdfname = statefp + ".pdf"
with PdfPages(pdfname) as pdf:
    for county in nc_counties["NAME"]:
        county_figure(county, pdf)
print("Atlas saved as " + pdfname)
print("Done! :)")


## Notes: Red points include every status other than Active, including Abandoned, Intermittent, and Temporarily Idled.
# Active mines are colored by primary commodity. Mine counts include only locations with valid coordinates inside selected state counties.
# Some MSHA records do not have coordinates and cannot appear on the maps.

## Sources: U.S. Census Bureau, Cartographic Boundary Files (2024).
# U.S. Department of Labor, Mine Safety and Health Administration (MSHA), "MSHA Mines Dataset," Data.gov.
# https://catalog.data.gov/dataset/msha-mines-dataset

## AI Use: I prompted ChatGPT in order to move the text, state map, and legend - they were covering each other.
# It gave me "The fig.add_axes([left, bottom, width, height]) numbers control where each section appears on the page, using values from 0 to 1"
# and the locations I requested afterward (Big county map, smaller state map underneath, text under both, legend on the right of the county map).

## I also used ChatGPT for the commodity colors based on the color of their resources, as well as adjusting PRIMARY_SIC instead of COMMODITY_CODE. It helped automate!