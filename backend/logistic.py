import openrouteservice as ors
from pandas import DataFrame
from openrouteservice.exceptions import ApiError
import pandas as pd

def get_vehicles(number:int, depot: list) -> list:
  vehicles = list()
  for idx in range(number):
    vehicles.append(
        ors.optimization.Vehicle(
            id=idx,
            start=list(reversed(depot)),
            # end=list(reversed(depot)),
            capacity=[500],
            time_window=[1553241600, 1553284800]  # Fri 8-20:00, expressed in POSIX timestamp
        )
    )
    
  return vehicles

def get_delivery_stations(data: DataFrame):
  deliveries = list()
  for delivery in data.itertuples():
    deliveries.append(
        ors.optimization.Job(
            id=delivery.Index,
            location=[delivery.Lon, delivery.Lat],
            service=1200,  # Assume 20 minutes at each site
            amount=[delivery.Needed_Amount],
            time_windows=[[
                int(delivery.Open_From.timestamp()),  # VROOM expects UNIX timestamp
                int(delivery.Open_To.timestamp())
            ]]
        )
    )
    
  return deliveries
    
def get_ors_client(api_key: str) -> ors.Client:
    try:
        ors_client = ors.Client(key=api_key)
        # Optionally, you can make a test request to validate the API key
        ors_client.directions(coordinates=[[8.34234, 48.23424], [8.34423, 48.26424]])
        return ors_client
    except ApiError as e:
        raise ValueError("Invalid API key or request error: " + str(e))

def get_optimization(
    ors_client: ors.Client,
    vehicles: list,
    delivery_stations: list
):
  optimization = ors_client.optimization(
      jobs=delivery_stations,
      vehicles=vehicles,
      geometry=True
  )
  
  return optimization

def generate_report_table(result) -> DataFrame:
  extract_fields = ['distance', 'amount', 'duration']
  data = [{key: route[key] for key in extract_fields} for route in result['routes']]

  vehicles_df = pd.DataFrame(data)
  vehicles_df.index.name = 'vehicle'
  
  return vehicles_df
  
def generate_schedule_table(result) -> list:
  stations = list()
  for route in result['routes']:
    vehicle = list()
    for step in route["steps"]:
        vehicle.append(
            [
                step.get("job", "Depot"),  # Station ID
                step["arrival"],  # Arrival time
                step["arrival"] + step.get("service", 0),  # Departure time

            ]
        )
    stations.append(vehicle)
  
  return stations

def iterative_schedule(stations: list, number: int, data: DataFrame) -> DataFrame:
    df_stations = pd.DataFrame(stations[number], columns=["Station ID", "Arrival", "Departure"])
    df_stations['Arrival'] = pd.to_datetime(df_stations['Arrival'], unit='s')
    df_stations['Departure'] = pd.to_datetime(df_stations['Departure'], unit='s')
    
    # Ensure ID is a column in data
    if 'ID' in data.index.names:
        data = data.reset_index()
    
    # Merge with data to get the Place column
    df_stations = df_stations.merge(data[['ID', 'Place']], left_on='Station ID', right_on='ID', how='left')
    
    # Skip mapping if the Station ID is "Depot"
    df_stations.loc[df_stations['Station ID'] == 'Depot', 'Place'] = 'Depot'
    
    # Drop the ID column as it's no longer needed
    df_stations.drop(columns=['ID'], inplace=True)
    
    return df_stations
  