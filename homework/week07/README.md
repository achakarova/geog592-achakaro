## Homework 8 – Geopandas Geoprocessing techniques


# Charlotte Flood Risk Project Data

This project will examine flood risk in Charlotte, with a focus on transportation and emergency access. The spatial analysis will use floodplain boundaries, streets, drainage features, and fire stations to identify roads exposed to flooding and examine how those areas connect to emergency-response facilities.

## Data

### Community Floodplain

Contains Charlotte-Mecklenburg community floodplain polygons.

Source: Charlotte-Mecklenburg Storm Water Services  
https://www.charlottenc.gov/Services/Stormwater/Data-Apps

### FEMA Floodplain

Contains FEMA floodplain polygons for the Charlotte-Mecklenburg area.

Source: Charlotte-Mecklenburg Storm Water Services / FEMA  
https://www.charlottenc.gov/Services/Stormwater/Data-Apps

### Drainage

Contains drainage features such as streams, creeks, and channels in Charlotte-Mecklenburg.

Source: City of Charlotte GIS Storm Drainage data  
https://gis.charlottenc.gov/arcgis/rest/services/STM/StormDrainage/MapServer

### Fire Stations

Contains current Charlotte Fire Department station locations.

Source: City of Charlotte GIS
https://arcg.is/1TT1a3

### Streets

Contains street centerlines for the Charlotte-Mecklenburg area.

Source: City of Charlotte / Mecklenburg County GIS

## Layers (TBD)

**Flood-exposed streets:** Street segments that overlap mapped floodplain areas, showing where transportation infrastructure may be vulnerable to flooding

**Fire stations and nearest drainage:** Fire station locations matched to the closest drainage feature to measure how near emergency facilities are to streams or channels

**Flood-exposed streets near fire stations:** Flood-prone street segments located within 0.5 mile of a fire station, highlighting areas where flooding could affect emergency access