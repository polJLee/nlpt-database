# importing the module
import pandas as pd
  
# target year
year = "2022"
  
# instantiating the parameters
start = year + "-01-01"
periods = 52
freq = "W-SUN"
  
# fetching the Sundays
sundays = pd.date_range(start = start,
                        periods = periods,
                        freq = freq)
  
# printing the Sundays                        
print(sundays)
