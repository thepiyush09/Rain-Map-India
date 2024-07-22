import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth, LayerControl, Map

# Load the rainfall data
rainfall_data = pd.read_csv('rainfall_data.csv')

# Load the GeoJSON file containing the geographical boundaries of Indian districts
geojson_path = 'output.geojson'
geo_data = gpd.read_file(geojson_path)

# Print column names to check
print("Geo Data Columns:", geo_data.columns)
print("Rainfall Data Columns:", rainfall_data.columns)

# Ensure the district names are standardized (e.g., remove whitespace and convert to upper case)
geo_data['dtname'] = geo_data['dtname'].str.strip().str.upper()
rainfall_data['DISTRICT'] = rainfall_data['DISTRICT'].str.strip().str.upper()

# Correct column names
district_column_geo = 'dtname'
district_column_rainfall = 'DISTRICT'

# Merge the rainfall data with the geo data
merged_data = geo_data.merge(rainfall_data, left_on=district_column_geo, right_on=district_column_rainfall)

# Check if merge was successful
print("Merged Data Columns:", merged_data.columns)
print("Sample Merged Data:", merged_data.head())

# Create a folium map
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Create a Choropleth map
Choropleth(
    geo_data=merged_data,
    data=merged_data,
    columns=[district_column_geo, 'ANNUAL'],
    key_on='feature.properties.dtname',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Annual Rainfall (mm)'
).add_to(m)

# Add layer control
LayerControl().add_to(m)

# Save the map to an HTML file
m.save('rainfall_map.html')

# Display the map in Jupyter Notebook (if you're using one)
# m
