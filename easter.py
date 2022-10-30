##Easter.py##

#   Given Year, calculates the date of Good Friday and Easter Sunday for the Year
#   Outputs: List of date in the order Easter Sunday and Good Friday


import sys
argc = len(sys.argv)

def easter(year):

    year = int(sys.argv[1])

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