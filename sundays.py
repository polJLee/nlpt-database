# importing the module


import datetime
import sys
import calendar

def sundays(month):
    # target year
    # month = sys.argv[1:][0]
    year = "2022"
    
    # instantiating the parameters
    start = datetime.date(int(year), month, 1)
    i = 1
    list = []
    while i < calendar.monthrange(int(year), month)[1]:
        if datetime.date(int(year), month, i).isoweekday() == 7:
            list.append(datetime.date(int(year), month, i).isoformat())
        i += 1
    return list

# argc = len(sys.argv)      <- remove comment to use the program as a stand alone function
# sundays(int(sys.argv[1:][0]))