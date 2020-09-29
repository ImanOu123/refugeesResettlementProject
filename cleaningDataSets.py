import csv
from openpyxl import load_workbook
import shutil

def cleanHousingData():
    def columnAverages(filepath, sheetName, column1, column2, cellStartRow):

        workbook = load_workbook(filename=filepath, data_only=True)

        spreadsheet = workbook[sheetName]

        # creates dictionary of Oct 18 cells

        cellsOct18 = {}

        cellRow = cellStartRow

        for i in range(72):
            cellsOct18["18cell" + str(i)] = spreadsheet[column1 + str(cellRow)].value
            cellRow += 1

        # creates dictionary of Oct 19 cells

        cellsOct19 = {}

        cellRow = cellStartRow

        for i in range(72):
            cellsOct19["19cell" + str(i)] = spreadsheet[column2 + str(cellRow)].value
            cellRow += 1

        # combine column as averages

        averagesList = {}

        n = 0

        for (i, e) in zip(cellsOct18.values(), cellsOct19.values()):

            if i == '**' and e == '**':
                averagesList["averagecell" + str(n)] = 0

            elif i == '**':
                averagesList["averagecell" + str(n)] = e

            elif e == '**':
                averagesList["averagecell" + str(n)] = i

            else:
                averagesList["averagecell" + str(n)] = round((i + e)/2, 2)

            n += 1

        return averagesList.values()

    def locationDic(filepath, sheetName, cellStartRow):
        workbook = load_workbook(filename=filepath, data_only=True)

        spreadsheet = workbook[sheetName]

        locationDic = {}

        for i in range(72):
            locationDic["location" + str(i)] = spreadsheet["A" + str(cellStartRow)].value
            cellStartRow += 1

        return locationDic.values()


    housingDataPath = "workingData/HousingData/OntarioHousingData.xlsx"

    def convertHousingVR():
        housingSheet1 = "Table 3.1.1"
        locationVR = locationDic(housingDataPath, housingSheet1, 8)

        sheetVRBachelor = columnAverages(housingDataPath, housingSheet1, "B", "D", 8)
        sheetVROneB = columnAverages(housingDataPath, housingSheet1, "G", "I", 8)
        sheetVRTwoB = columnAverages(housingDataPath, housingSheet1, "L", "N", 8)
        sheetVRThreeB = columnAverages(housingDataPath, housingSheet1, "Q", "S", 8)

        with open('housingVacancyRates.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Location", "Bachelor", "1 Bedroom", "2 Bedroom", "3 Bedroom +"])

            for (loc, Bach, OneB, TwoB, ThreeB) in zip(locationVR, sheetVRBachelor, sheetVROneB, sheetVRTwoB,
                                                       sheetVRThreeB):
                writer.writerow([loc, Bach, OneB, TwoB, ThreeB])

        shutil.move("housingVacancyRates.csv", "workingData/HousingData/housingVacancyRates.csv")


    def convertHousingRP():
        housingSheet2 = "Table 3.1.2"
        locationRP = locationDic(housingDataPath, housingSheet2, 7)

        sheetRPBachelor = columnAverages(housingDataPath, housingSheet2, "B", "D", 7)
        sheetRPOneB = columnAverages(housingDataPath, housingSheet2, "F", "H", 7)
        sheetRPTwoB = columnAverages(housingDataPath, housingSheet2, "J", "L", 7)
        sheetRPThreeB = columnAverages(housingDataPath, housingSheet2, "N", "P", 7)

        with open('housingRentPrices.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Location", "Bachelor", "1 Bedroom", "2 Bedroom", "3 Bedroom +"])

            for (loc, Bach, OneB, TwoB, ThreeB) in zip(locationRP, sheetRPBachelor, sheetRPOneB, sheetRPTwoB, sheetRPThreeB):
                writer.writerow([loc, Bach, OneB, TwoB, ThreeB])

        shutil.move("housingRentPrices.csv", "workingData/HousingData/housingRentPrices.csv")

    convertHousingVR()
    convertHousingRP()

cleanHousingData()