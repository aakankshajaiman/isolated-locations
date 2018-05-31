# Using haversine formula to complete the task
# I have identified the most isolated locations Location Id for each country at first
# After that I have identified the most isolated locations Location Id in the data set
# Calculation is taking time to complete for some countries like US.
# Please update the physical path (INPUT_URL) of file before executing the code

from math import radians, cos, sin, asin, sqrt
from csv import DictReader

# Physical location and name of the file in computer
INPUT_URL = "/Users/aakanksha/Downloads/Data_Scientist_Product.csv"

drows = []      # List to add data rows after reading csv file
Countries = []  # List to hold distinct country names
finalList = []  # List that will hold top most isolated location in each country



# Function to calculate distance between latitude longitude pairs
def haversine_on_rows(a, b):
    lon1 = radians(a['Longitude'])
    lon2 = radians(b['Longitude'])
    lat1 = radians(a['Latitude'])
    lat2 = radians(b['Latitude'])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    r = 6371 # Radius of earth in kilometers.
    # return the final calculation
    return c * r


# Reading csv file
with open(INPUT_URL, 'r') as rf:
    for row in DictReader(rf):
        try:
            row['Longitude'] = float(row['Longitude'])
            row['Latitude'] = float(row['Latitude'])
            drows.append(row)

            if row['Country'] not in Countries:
                Countries.append(row['Country'])
        except ValueError:
            pass

# Loop through the data and calculate the distance
# Calculating for each country
for j, country in enumerate(Countries):
    print "Calculating isolated location for country \'" + country + "\' Please wait..."
    countryList = []
    for i, row in enumerate(drows):
        if row['Country'].__eq__(country):
            n_row = sorted(drows, key=lambda x: haversine_on_rows(row, x))[1]
            row['nearest_LocationId'] = n_row['LocationId']
            row['nearest_location_distance_km'] = round(haversine_on_rows(row, n_row), 1)
            countryList.append(row)

    # sorting the list for a country based on location
    countryList = sorted(countryList,
                         key=lambda x: float(x['nearest_location_distance_km']),
                         reverse=True)

    print("The most isolated Locationid in " + country + " is: ")

    # picking the first location from the list
    for i, row in enumerate(countryList[0:1]):
        print("%s with %s km distance-- , Longitude:%s Latitude:%s" % (row['LocationId'],
                                                                       row['nearest_location_distance_km'],
                                                                       row['Longitude'],
                                                                       row['Latitude']))

        finalList.append(row)
        print " "

print " "
print " "

# Sorting list of all countries to get the most isolated location
finalList = sorted(finalList,
                   key=lambda x: float(x['nearest_location_distance_km']),
                   reverse=True)
print("The most isolated Locationid in world is: ")
print("%s with %s km distance-- , Longitude:%s Latitude:%s" % (finalList[0]['LocationId'],
                                                               finalList[0]['nearest_location_distance_km'],
                                                               finalList[0]['Longitude'],
                                                               finalList[0]['Latitude']))



