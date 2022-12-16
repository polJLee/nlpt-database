# importing the module


import datetime
import sys
import calendar


def easter(year):
    
    year = int(year)

    D = 225 - 11*(year % 19)

    if D > 50:
        while D >= 51:
            D -= 30
    if D > 48:
        D -= 1

    E = int((year + (year/4) + D + 1) % 7)
    Q = D + 7 - E

    output = []
    if Q < 32:
        month = '03'
        Eday = Q
        Gday = str(Q - 2)
        output.append(f"{Eday}.{month}")
        output.append(f"{Gday}.{month}")
    else:
        month = '04'
        day = Q - 31
        if day < 10 and day > 2:
            Eday = '0' + str(day) 
            Gday = '0' + str(day - 2)
            output.append(f"{Eday}.{month}")
            output.append(f"{Gday}.{month}")
        elif day <= 2:
            day = '0' + str(day)
            output.append(f"{day}.{month}")
            month = '03'
            day = str(31 - (2-int(day)))
            output.append(f"{day}.{month}")
        else:
            output.append(f"{day}.{month}")
            day = str(day - 2)
            output.append(f"{day}.{month}") 
    return output


def sundays(month, year):
    # target year
    # month = sys.argv[1:][0]
    east = easter(year)
    Gday = east[1][0:2]
    Gmonth = east[1][4:6]
    goodFriday = datetime.date(year, int(Gmonth), int(Gday))
    
    # instantiating the parameters
    i = 1
    list = []
    while i < calendar.monthrange(year, month)[1]:
        if datetime.date(year, month, i).isoweekday() == 7:
            list.append(datetime.date(year, month, i).isoformat())
        if datetime.date(year, month, i) == goodFriday:
            list.append(datetime.date(year, month, i).isoformat())
        i += 1
    return list

# argc = len(sys.argv)      <- remove comment to use the program as a stand alone function
# sundays(int(sys.argv[1:][0]))