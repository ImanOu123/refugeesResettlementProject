import csv

def formFunction(resettleCountry, familySize): # YNchildren, numberChildren, agesChildren, YNdisabilities, typeDisabilities, YNelderly, religion, firstLang, secondLang):
    """This function ..."""
    # part one = housing

    # directing function to data

    if resettleCountry == 'Canada':  # if data placed in database, will be directed to place in database
        housingRPFilePath = "workingData/HousingData/housingRentPrices.csv"
        housingVRFilePath = "workingData/HousingData/housingVacancyRates.csv"

    else:
        housingRPFilePath = " "
        housingVRFilePath = " "

    # specify house locations

    canadaFinancalAid = 2065

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
                    if 0 < j <= canadaFinancalAid:
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

    idealLocations = []

    for loc in idealLocationRP:
        if loc in idealLocationVR:
            idealLocations.append(loc)



formFunction('Canada', '6+')
