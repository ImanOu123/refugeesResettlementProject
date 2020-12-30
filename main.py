import csv
import json
import re

def cityNameFunction(location):
    """This function inputs a location of any classfication (city or neighbourhood) and returns the city that the location is in"""

    locationsList = []
    locationsDict = {}

    # organize OSM data into helpful lists/dict

    with open('OSMCitydata.txt') as json_file:
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

        # main task of function

        for city, names in locationsDict.items():
            if location in names:
                return city

        return "Not Found"

def religiousInstit(religion):
    """This function inputs a religion and returns a list with names and locations of religious institutions affiliated with the religion"""

    locationsList = []
    religions = []
    locationsDict = {}

    with open('OSMReligiousInstitdata.txt') as json_file:
        data = json.load(json_file)

        # create list with info on location (location, name, religion)

        for element in data['elements']:
            # if location is written as a tag

            if 'addr:city' in element['tags'] and 'name' in element['tags'] and 'religion' in element['tags']:
                locationsList.append([element['tags']['addr:city'], element['tags']['name'], element['tags']['religion']])
                religions.append(element['tags']['religion'])

            # if location is written within the name of institution

            elif 'name' in element['tags'] and 'religion' in element['tags']:
                for loc in ['Windsor', 'Ottawa', 'London', 'Toronto', 'Kitchener', 'Hamilton']: # can expand list, but kept it to 'friendly' locations for simpicity
                    if loc in element['tags']['name']:
                        locationsList.append([loc, element['tags']['name'], element['tags']['religion']])
                        religions.append(element['tags']['religion'])

        # create a dictionary that categorizes each location under a religion

        for rel in religions:
            locationsDict[rel] = []
            for elem in locationsList:
                if rel in elem:
                    locationsDict[rel].append(elem)

        for rel, info in locationsDict.items():
            if religion == rel:
                return info


def formFunction(resettleCountry, familySize, YNchildren, numberChildren, agesChildren, YNdisabilities, typeDisabilities, YNelderly, religion):
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

    for loc in oldidealHousingLocations:
        strList = re.split('[-/\s]', loc)

        if 'CMA' in strList or 'CA' in strList or 'MU' in strList:
            strList.pop(-1)

        if "Chatham-Kent" in loc:
            idealHousingLocations.append("Chatham-Kent")

        elif "Zone" in loc:
            str1 = " ".join(strList[4:])
            idealHousingLocations.append(str1)

        elif "-" in loc:
            if "St." in loc:
                if len(strList) == 2:
                    str1 = " ".join(strList[:2])
                    idealHousingLocations.append(str1)
                elif len(strList) == 3:
                    str1 = " ".join(strList[:2])
                    str2 = strList[2]
                    idealHousingLocations = idealHousingLocations + [str1, str2]

            elif len(strList) == 3:
                str1 = strList[0]
                str2 = strList[1]
                str3 = strList[2]
                idealHousingLocations = idealHousingLocations + [str1, str2, str3]

            elif len(strList) == 2 or len(strList) == 4:
                str1 = strList[0]
                str2 = strList[1]
                idealHousingLocations = idealHousingLocations + [str1, str2]

        elif "/" in loc:
            str1 = " ".join(strList[:2])
            idealHousingLocations.append(str1)

        elif len(strList) >= 2:
            str1 = " ".join(strList[:2])
            idealHousingLocations.append(str1)

        elif "Ste." in loc:
            if len(strList) == 3:
                idealHousingLocations.append("Sault Ste. Marie")
            else:
                continue
        else:
            str1 = strList[0]
            idealHousingLocations.append(str1)

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

    # creating dictionary with ideal places within locations

    # filter locations to only those within cityNameFunction

    filteredidealHousingLoc = []

    # print(idealHousingLocations)

    for loc in idealHousingLocations:

        filteredLoc = cityNameFunction(loc)

        if filteredLoc == "Not Found":
            continue

        else:
            filteredidealHousingLoc.append(filteredLoc)

    print(filteredidealHousingLoc)

    # filter locations to those that are considered to be the most 'friendly' locations for immigrants/refugees
    friendlyHousingLoc = []

    for elem in filteredidealHousingLoc:
        if elem in ['Windsor', 'Ottawa', 'London', 'Toronto', 'Kitchener', 'Hamilton']:
            friendlyHousingLoc.append(elem)

    print(friendlyHousingLoc)

    idealPlacesDict = {}

    for loc in friendlyHousingLoc: # find a way to reduce computation time
        idealPlacesDict[loc] = {"Schools": [], "Healthcare": []}

        for (locations, name) in idealSchoolNameandLocations:
            filteredLocation = cityNameFunction(locations)
            if filteredLocation == loc:
                idealPlacesDict[loc]["Schools"].append(name)

        for (locations, name, type) in idealHealthcare:
            filteredLocation = cityNameFunction(locations)
            if filteredLocation == loc:
                idealPlacesDict[loc]["Healthcare"].append([name, type])

#print(formFunction('Canada', '3to5', 'Y', 3, [10, 14], 'yes', 'deaf', 'yes', 'islam'))
# print(cityNameFunction('Cambridge'))
print(religiousInstit('muslim'))
