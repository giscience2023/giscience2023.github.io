import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from shapely.geometry import Point
import contextily as ctx
import os
import pickle

# Load CSV file
print("Reading organisations..",)
df = pd.read_csv('organisations.csv')
print(f"\t...read {len(df)} locations")

# Initialize geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

def geocode_location(name, retries=3, delay=2, timeout=5):
    for _ in range(retries):
        try:
            location = geolocator.geocode(name, timeout=timeout)
            if location:
                return Point(location.longitude, location.latitude)
        except (GeocoderTimedOut, GeocoderUnavailable):
            time.sleep(delay)  # Wait for a few seconds before retrying
    return None

# Geocode each organization name
print("Geocoding locations")

# File path for the pickled GeoDataFrame
pickle_file = 'geocoded_organisations.pkl'

# Check if the pickle file exists
if os.path.exists(pickle_file):
    # Load the GeoDataFrame from the pickle file
    with open(pickle_file, 'rb') as f:
        gdf = pickle.load(f)
else:
    # Load CSV file
    df = pd.read_csv('organisations.csv')

    # Geocode each organization name
    df['geometry'] = df['organisation_name'].apply(geocode_location)

    # Drop organizations that couldn't be geocoded
    df = df.dropna(subset=['geometry'])

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Save the GeoDataFrame to a pickle file
    with open(pickle_file, 'wb') as f:
        pickle.dump(gdf, f)


#df['geometry'] = df['organisation_name'].apply(geocode_location)

# Drop organizations that couldn't be geocoded
#df = df.dropna(subset=['geometry'])

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry')

print("Plotting")
# Plot the data
#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#ax = world.plot(color='white', edgecolor='black')
#gdf.plot(ax=ax, marker='o', color='red', markersize=5)
#plt.show()


# Plot the data
fig, ax = plt.subplots(figsize=(15, 10))

# Use a better basemap
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.boundary.plot(ax=ax, linewidth=1, color='black', zorder=3)
gdf.plot(ax=ax, marker='o', color='blue', markersize=50, zorder=4)

# Add basemap tiles
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite, zoom=0)

# Customize the appearance
ax.set_title("Organization Locations", fontsize=20)
ax.set_xlabel("Longitude", fontsize=14)
ax.set_ylabel("Latitude", fontsize=14)
ax.set_axis_off()

plt.tight_layout()
plt.show()

