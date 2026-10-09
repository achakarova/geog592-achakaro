# Homework 8 – GeoPandas Geoprocessing Techniques

## Charlotte Flood Risk Project

This project asks where flooding and storm hazards may affect transportation and emergency access in Charlotte-Mecklenburg. The analysis combines floodplain, street, drainage, fire station, FEMA, and NOAA storm data.

## Data

### Community Floodplain
Charlotte-Mecklenburg community floodplain polygons used to identify flood-exposed streets.  
Source: Charlotte-Mecklenburg Storm Water Services  
https://www.charlottenc.gov/Services/Stormwater/Data-Apps

### FEMA Floodplain
FEMA floodplain polygons used for the attribute-join layer with Mecklenburg County storm information.  
Source: Charlotte-Mecklenburg Storm Water Services / FEMA  
https://www.charlottenc.gov/Services/Stormwater/Data-Apps

### Drainage
Streams, creeks, and drainage channels used to create the 500-foot drainage buffer.  
Source: City of Charlotte GIS  
https://gis.charlottenc.gov/arcgis/rest/services/STM/StormDrainage/MapServer

### Fire Stations
Current Charlotte Fire Department station locations used in the drainage and emergency-access analyses.  
Source: City of Charlotte GIS  
https://arcg.is/1TT1a3

### Streets
Charlotte-Mecklenburg street centerlines used to identify roads exposed to flooding.  
Source: City of Charlotte / Mecklenburg County GIS  
https://gis.charlottenc.gov/arcgis/rest/services/CountyData/Streets/MapServer

### NOAA Storm Events
storm_data is a non-spatial table of NOAA storm events used for the attribute join.  
Source: NOAA National Centers for Environmental Information, Storm Events Database  
https://www.ncei.noaa.gov/access/storm-events-database/

## Analysis

### Layer 1: Flood-Exposed Streets
Question: Which streets intersect the community floodplain?  
Answer: The spatial join selects the street segments that overlap mapped community floodplain areas.

### Spatial Join Analysis
Question: Which street classes appear most often among flood-exposed streets?  
Answer: The Layer 1 spatial-join result is grouped by STREETCLASS and displayed as a table and bar graph.

### Layer 2: Fire Stations Near Drainage
Question: Which fire stations are within 500 feet of drainage features?  
Answer: A 500-foot drainage buffer identifies the stations that are close to streams, creeks, or drainage channels.

### Layer 3: Flood-Exposed Streets Near Fire Station 1
Question: Which flood-exposed streets are within 3 miles of Fire Station 1?  
Answer: Distance measurements identify the flood-exposed street segments that fall within the 3-mile distance.

### Attribute Join
Question: What NOAA storm history is associated with the Mecklenburg County FEMA floodplain area?  
Answer: storm_data (csv) is summarized for Mecklenburg County and joined to the FEMA floodplain polygons, creating a new layer containing both FEMA geometry and storm-event attributes.
