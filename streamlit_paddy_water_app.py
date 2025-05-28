
import streamlit as st
import ee
import geemap.foliumap as geemap

# Set page config
st.set_page_config(page_title="Paddy Field Water Management", layout="wide")

st.title("🌾 Paddy Field Water Management using NDWI and Satellite Data")

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# Sidebar for AOI input
st.sidebar.title("Set Area of Interest (AOI)")
lon1 = st.sidebar.number_input("Min Longitude", value=100.0)
lat1 = st.sidebar.number_input("Min Latitude", value=6.0)
lon2 = st.sidebar.number_input("Max Longitude", value=100.5)
lat2 = st.sidebar.number_input("Max Latitude", value=6.5)

aoi = ee.Geometry.Rectangle([lon1, lat1, lon2, lat2])

# Select Date
st.sidebar.title("Select Date Range")
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

# Load Sentinel-2 and compute NDWI
if start_date and end_date:
    collection = (ee.ImageCollection("COPERNICUS/S2")
                  .filterBounds(aoi)
                  .filterDate(str(start_date), str(end_date))
                  .sort("CLOUD_COVER"))

    image = collection.first()
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')

    Map = geemap.Map()
    Map.centerObject(aoi, 10)
    Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, "Sentinel RGB")
    Map.addLayer(ndwi, {'min': -1, 'max': 1, 'palette': ['brown', 'blue']}, "NDWI")

    # Display the map
    Map.to_streamlit(height=600)
else:
    st.info("Please set the date range to visualize NDWI.")
