def string_to_array(x: str, y:str) -> list:
  """Convert two strings object to number array.
  
  Args:
      x (str): String to convert to array
      y (str): String to convert to array
  
  Returns:
      list: Array of number strings
  """
  
  # convert to number with decimal
  x = float(x)
  y = float(y)
  
  return [x, y]
