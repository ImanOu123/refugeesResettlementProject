import csv
import json
import requests
import re

def formFunction(resettleCountry, familySize, YNchildren, numberChildren, agesChildren): # YNdisabilities, typeDisabilities, YNelderly, religion, firstLang, secondLang):
    """This function ..."""
    # directing function to data

    if resettleCountry == 'Canada':  # if data placed in database, will be directed to place in database
        housingRPFilePath = "workingData/HousingData/housingRentPrices.csv"
        housingVRFilePath = "workingData/HousingData/housingVacancyRates.csv"

        educationFilePath = "workingData/SchoolsData/educationData.csv"

        healthcareFilePath = "workingData/HealthcareData/HealthcareData.csv"

    # part one = housing

    # specify house locations

    locationsANDsizes = []

    with open(housingRPFilePath) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        for row in reader:

            if row == ["Location", "Bachelor", "1 Bedroom", "2 Bedroom", "3 Bedroom +"]:
                continue

            rowArray = [["location", row[0]], ["Bachelor", float(row[1])], ["1B", float(row[2])], ["2B", float(row[3])], ["3B+", float(row[4])]]

            availableType = []

            for (i, j) in rowArray:
                if isinstance(j, str):
                    location = j
                elif isinstance(j, float):
                    if 0 < j:
                        availableType.append(i)

            locationsANDsizes.append([location, availableType])

    locationsANDvacancies = []

    with open(housingVRFilePath) as csv_file:

        reader = csv.reader(csv_file, delimiter=',')

        for row in reader:
            if row == ["Location", "Bachelor", "1 Bedroom", "2 Bedroom", "3 Bedroom +"]:
                continue

            rowArray = [["location", row[0]], ["Bachelor", float(row[1])], ["1B", float(row[2])], ["2B", float(row[3])], ["3B+", float(row[4])]]

            availableType = []

            for (i, j) in rowArray:
                if isinstance(j, str):
                    location = j
                elif isinstance(j, float):
                    if j > 0:
                        availableType.append(i)

            locationsANDvacancies.append([location, availableType])


    # specify ideal locations for houses

    idealLocationRP = []
    idealLocationVR = []

    if familySize == "1to2":
        for (loc, size) in locationsANDsizes:
            for types in size:
                # if the bedroom size in the type list is available in a location, stores location in array
                if types == '1B':
                    idealLocationRP.append(loc)

        for (loc, size) in locationsANDvacancies:
            for types in size:
                if types == '1B':
                    idealLocationVR.append(loc)

    if familySize == "3to5":
        for (i, j) in locationsANDsizes:
            for e in j:
                # if the bedroom size in the type list is available in a location, stores location in array
                if e == '2B':
                    idealLocationRP.append(i)

            for (loc, size) in locationsANDvacancies:
                for types in size:
                    if types == '2B':
                        idealLocationVR.append(loc)

    if familySize == "6+":
        for (i, j) in locationsANDsizes:
            for e in j:
                # if the bedroom size in the type list is available in a location, stores location in array
                if e == '3B+':
                    idealLocationRP.append(i)

        for (loc, size) in locationsANDvacancies:
            for types in size:
                if types == '3B+':
                    idealLocationVR.append(loc)

    # compare RP and VR lists & combine

    idealHousingLocations = []


    for loc in idealLocationRP:
        if loc in idealLocationVR:
            idealHousingLocations.append(loc)

    # clean housing location names

    oldidealHousingLocations = idealHousingLocations
    idealHousingLocations = []
    strList = []

    for loc in oldidealHousingLocations:
        strList = re.split('[-\s]', loc)

        if 'CMA' in strList or 'CA' in strList:
            strList.pop(-1)

        print(strList)





    # part two = education

    # specify school locations



    schoolInfo = []

    with open(educationFilePath) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        for row in reader:

            if row == ["schoolLocation, schoolName, schoolType, schoolLevel, gradeRange"]:
                continue

            rowArray = [["location", row[0]], ["name", row[1]], ["type", row[2]], ["level", row[3]], ["graderange", row[4]]]

            schoolInfo.append(rowArray)

    schoolInfo.pop(0)

    elemSchools = []
    seconSchools = []

    for (loc, name, type, level, range) in schoolInfo:

        if level[1] == 'Elementary':
            EschoolInfoRow = [loc[1], name[1]]
            elemSchools.append(EschoolInfoRow)

        if level[1] == 'Secondary':
            SschoolInfoRow = [loc[1], name[1]]
            seconSchools.append(SschoolInfoRow)

    idealSchoolNameandLocations = []
    schoolLevel = []

    if YNchildren == 'Y':
        # match children to schools based on age
        if 6 in agesChildren or 7 in agesChildren or 8 in agesChildren or 9 in agesChildren or 10 in agesChildren:
            schoolLevel.append('elem')

        if 11 in agesChildren or 12 in agesChildren or 13 in agesChildren or 14 in agesChildren or 15 in agesChildren \
                or 16 in agesChildren or 17 in agesChildren or 18 in agesChildren:
            schoolLevel.append('secon')

    if schoolLevel == ['elem']:
        idealSchoolNameandLocations = elemSchools

    elif schoolLevel == ['secon']:
        idealSchoolNameandLocations = seconSchools

    elif schoolLevel == ['elem', 'secon']:
        idealSchoolNameandLocations = elemSchools + seconSchools

    else:
        idealSchoolNameandLocations = ['NO SCHOOL']


    # part three = healthcare

    HealthcareInfo = []

    with open(healthcareFilePath) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        for row in reader:

            if row == ["Location,HealthcareName,ServiceType"]:
                continue

            rowArray = [["location", row[0]], ["name", row[1]], ["type", row[2]]]

            HealthcareInfo.append(rowArray)

    HealthcareInfo.pop(0)

    idealHealthcare = []

    for (loc, name, type) in HealthcareInfo:
        HealthcareInfoRow = [loc[1], name[1], type[1]]
        idealHealthcare.append(HealthcareInfoRow)

    #creating dictionary with ideal places within locations

    idealPlacesDict = {}

    for loc in idealHousingLocations:
        idealPlacesDict[loc] = []

    print(idealPlacesDict)

print(formFunction('Canada', '3to5', 'Y', 3, [10, 14]))


def cityNameFunction(location):
    """This function inputs a location of any classfication (city or neighbourhood) and returns the city that the location is in"""

    # get OSM data from OSM API

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
        [out:json];
        area(3600068841) -> .a;
        (
            node["place"="city"](area.a);
            node["place"="neighbourhood"](area.a);
        );
        out;

        """
    OSMdata = requests.get(overpass_url, params={'data': overpass_query}).json()

    with open('OSMdata.txt', 'w') as outfile:
        json.dump(OSMdata, outfile)

    locationsList = []
    locationsDict = {}

    # organize OSM data into helpful lists/dict

    with open('OSMdata.txt') as json_file:
        data = json.load(json_file)

        # create list with info on location (name, type of place, is_in (for neighbourhoods))

        for element in data['elements']:
            # print(element)
            if 'is_in' in element['tags']:
                locationsList.append([element['tags']['name'], element['tags']['place'], element['tags']['is_in']])
            elif element['tags']['place'] == 'neighbourhood':
                continue
            else:
                locationsList.append([element['tags']['name'], element['tags']['place']])

        # print(locationsList)

        # create a dictionary that categorizes each location under a city

        for loc in locationsList:
            if 'city' in loc:
                locationsDict[loc[0]] = [loc[0]]

            elif 'neighbourhood' in loc:
                # classify neighbourhood under city
                isInCity = loc[2]

                for cityName in locationsDict:
                    if isInCity == cityName:
                        locationsDict[cityName] = [cityName, loc[0]]

                    elif cityName in isInCity: # for city names that are Toronto but longer
                        locationsDict[cityName].append(loc[0])

        print(locationsDict)

        # main task of function

        for city, names in locationsDict.items():
            if location in names:
                return city

# print(cityNameFunction('Heritage Green'))
