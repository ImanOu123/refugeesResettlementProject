import csv
from openpyxl import load_workbook

def columnAverages(filepath, sheetName, column1, column2):

    workbook = load_workbook(filename=filepath, data_only=True)

    spreadsheet = workbook[sheetName]

    # creates dictionary of Oct 18 cells

    cellsOct18 = {}

    cellRow = 11

    for i in range(72):
        cellsOct18["18cell" + str(i)] = spreadsheet[column1 + str(cellRow)].value
        cellRow += 1

    # creates dictionary of Oct 19 cells

    cellsOct19 = {}

    cellRow = 11
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
            averagesList["averagecell" + str(n)] = (i + e)/2

        n += 1

    return averagesList

housingDataPath = "workingData/HousingData/OntarioHousingData.xlsx"

housingSheet1 = "Table 3.1.1"
housingSheet2 = "Table 3.1.2"

sheetVRBachelor = columnAverages(housingDataPath, housingSheet1, "B", "D")
sheetVROneB = columnAverages(housingDataPath, housingSheet1, "G", "I")
sheetVRTwoB = columnAverages(housingDataPath, housingSheet1, "L", "N")
sheetVRThreeB = columnAverages(housingDataPath, housingSheet1, "Q", "S")

sheetRPBachelor = columnAverages(housingDataPath, housingSheet2, "B", "D")
sheetRPOneB = columnAverages(housingDataPath, housingSheet2, "F", "H")
sheetRPTwoB = columnAverages(housingDataPath, housingSheet2, "J", "L")
sheetRPThreeB = columnAverages(housingDataPath, housingSheet2, "N", "P")

with open('housingVacancyRates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Location", "Bachelor", "1 Bedroom", "2 Bedroom", "3 Bedroom +"])

