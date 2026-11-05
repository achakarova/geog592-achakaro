## Homework 11 - JN to .py
## By Antoaneta Chakarova for GEOG592
## 11/05/2026

print("Importing Modules")
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

print("Accessing and downloading Census data")
statefp = "37" #NC
url = "https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_county_500k.zip"
counties = gpd.read_file(url)

nc_counties = counties[counties["STATEFP"] == statefp].to_crs(6543).copy() #Change crs based on state
nc_counties = nc_counties.sort_values("NAME").reset_index(drop=True)


print("Loading mining permit data")
mines = pd.read_csv("NCMiningPermits.csv") #May need to find alternative data source if automating it for another state
mines = mines.dropna(subset=["LONGITUDE", "LATITUDE"])

#longitude and latitude become map points, then use the same CRS as the counties
mines_points = gpd.GeoDataFrame(mines, geometry=gpd.points_from_xy(mines["LONGITUDE"], mines["LATITUDE"]), crs="EPSG:4326")
mines_points = mines_points.to_crs(nc_counties.crs)

print("Assigning mining permits to counties")
#spatial join: keep only mines that fall within NC counties
mines_by_county = gpd.sjoin(mines_points, nc_counties[["NAME", "geometry"]], how="inner", predicate="within")
print("Total mines assigned to counties:", len(mines_by_county))


#Red will mean any mine that is NOT marked Active
commodity_colors = {
    "Sand and Gravel": "khaki",
    "Crushed Stone": "gray",
    "Brick Clay": "sienna",
    "Sand Dipping": "goldenrod",
    "Sand Dredging": "darkgoldenrod",
    "Dimension Stone": "slategray",
    "Silica Sand": "palegoldenrod",
    "Gemstone": "mediumorchid",
    "Mica": "plum",
    "Olivine": "olivedrab",
    "Peat": "brown",
    "Feldspar": "lightsteelblue",
    "Pyrophillyte": "tan",
    "Gold": "gold",
    "Lithium": "mediumpurple",
    "Flag Stone": "darkgray",
    "Building Stone": "silver",
    "Phosphate": "darkseagreen",
    "Talc": "lightgray",
    "Other/Unknown": "lightskyblue"
}


#Number of permits by county (from the spatial join result)
county_summary = mines_by_county.groupby("NAME").size().rename("total_mines")
county_summary = nc_counties[["NAME"]].merge(county_summary, left_on="NAME", right_index=True, how="left")
county_summary["total_mines"] = county_summary["total_mines"].fillna(0)
print("Mining permit counts calculated")


def county_map(county, ax):
    selected = nc_counties[nc_counties["NAME"] == county]
    county_mines = mines_by_county[mines_by_county["NAME"] == county]
    active = county_mines[county_mines["MINE_STATUS"] == "Active"]
    inactive = county_mines[county_mines["MINE_STATUS"] != "Active"]

    selected.plot(ax=ax, facecolor="whitesmoke", edgecolor="black")

    for commodity in active["COMMODITY_CODE"].dropna().unique(): #plot each active commodity using its own color
        sites = active[active["COMMODITY_CODE"] == commodity]
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
    inactive = len(county_mines[county_mines["MINE_STATUS"] != "Active"])

    sentence = "There are " + str(total) + " mining permits in " + county + " County."
    sentence = sentence + "\n" + str(inactive) + " mines are not active."

    ax.text(0, 0.9, sentence, fontsize=16, va="top", transform=ax.transAxes)
    ax.set_axis_off()


def county_figure(county, pdf):
    fig = plt.figure(figsize=(8, 10))

    #Large county map on the left
    ax1 = fig.add_axes([0.05, 0.35, 0.62, 0.55])
    county_map(county, ax1)

    #Smaller North Carolina locator underneath
    ax2 = fig.add_axes([0.08, 0.16, 0.35, 0.16])
    locator_map(county, ax2)

    #Text underneath the maps
    ax3 = fig.add_axes([0.06, 0.05, 0.90, 0.10])
    county_info(county, ax3)

    fig.suptitle(county + " County", fontsize=22)

    pdf.savefig(fig)
    plt.close(fig)


print("Generating North Carolina Mining Atlas")
pdfname = statefp + ".pdf"
with PdfPages(pdfname) as pdf:
    for county in nc_counties["NAME"]:
        county_figure(county, pdf)
print("Done! :) Atlas saved as " + pdfname) #It's 32mb so I'm not keeping it in my folder


## Notes: Red points include mines marked Inactive, Released, Pending, or Revoked, not just records labeled Inactive.
# Active mines are colored by commodity type. Mine counts are based on coordinate locations within each county.

## Sources: U.S. Census Bureau county boundaries; NC Department of Environmental Quality mining permits.

## AI Use: I prompted ChatGPT in order to move the text, NC map, and legend - they were covering each other.
# It gave me "The fig.add_axes([left, bottom, width, height]) numbers control where each section appears on the page, using values from 0 to 1"
# and the locations I requested afterward (Big county map, smaller NC map underneath, text under both, legend on the right of the county map)
