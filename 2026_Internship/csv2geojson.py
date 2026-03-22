import geopandas as gpd
import pandas as pd

df = pd.read_csv("data/solaranlagen.csv")
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.GeoSeries.from_wkt(df["WKT"]),
    crs="EPSG:4326"
)

gdf.to_file("data/solaranlagen.geojson", driver="GeoJSON")
