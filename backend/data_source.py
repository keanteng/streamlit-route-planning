import pandas as pd
from pandas import DataFrame
import streamlit as st

def get_data(path: str) -> DataFrame:
  """Read data from CSV file.

  Args:
      path (str): Path to the CSV file

  Returns:
      DataFrame: Data from the CSV file
  """
  data = pd.read_csv(
    path,
    index_col='ID',
    parse_dates=['Open_From', 'Open_To']
  )
  return data

@st.cache_data
def convert_df(path:str):
  data = pd.read_csv(path)
  return data.to_csv(index=False).encode('utf-8')