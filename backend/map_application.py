import folium
from folium.plugins import BeautifyIcon
import pandas as pd
from pandas import DataFrame
import openrouteservice as ors

def create_map(geocoordinate: list) -> folium.Map:
  m = folium.Map(location=geocoordinate, tiles='OpenStreetMap', zoom_start=12)
  return m

def add_marker(m:folium.Map, data: DataFrame) -> folium.Map:
    for location in data.itertuples():
      tooltip = folium.map.Tooltip("<h4><b>ID {}</b></p><p>Supplies needed: <b>{}</b></p><p><b>Place: {}</b></p>".format(
          location.Index, location.Needed_Amount, location.Place
      ))

      folium.Marker(
          location=[location.Lat, location.Lon],
          tooltip=tooltip,
          icon=BeautifyIcon(
              icon_shape='marker',
              number=int(location.Index),
              spin=True,
              text_color='red',
              background_color="#FFF",
              inner_icon_style="font-size:12px;padding-top:-5px;"
          )
      ).add_to(m)
    
    return m
  
def add_depot_marker(m:folium.Map, depot_geocoordinates: list) -> folium.Map:
  folium.Marker(
      location=depot_geocoordinates,
      icon=folium.Icon(color="green", icon="bus", prefix='fa'),
      setZIndexOffset=1000
  ).add_to(m)
  
  return m

def add_optimized_route(m:folium.Map, result):
  for color, route in zip(['green', 'red', 'blue'], result['routes']):
    decoded = ors.convert.decode_polyline(route['geometry'])  # Route geometry is encoded
    gj = folium.GeoJson(
        name='Vehicle {}'.format(route['vehicle']),
        data={"type": "FeatureCollection", "features": [{"type": "Feature",
                                                         "geometry": decoded,
                                                         "properties": {"color": color}
                                                         }]},
        style_function=lambda x: {"color": x['properties']['color']}
    )
    gj.add_child(folium.Tooltip(
        """<h4>Vehicle {vehicle}</h4>
        <b>Distance</b> {distance} m <br>
        <b>Duration</b> {duration} secs
        """.format(**route)
    ))
    gj.add_to(m)
    
  folium.LayerControl().add_to(m)
  
  return m