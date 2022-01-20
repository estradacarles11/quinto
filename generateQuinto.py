import random
import csv
import math


def shuffle(list, seed=None):

    if seed is not None:
        random.seed(seed)

    return random.sample(list, len(list))


def generateTable(numbers):

    table = [[[0 for c in range(5)] for r in range(3)] for q in range(6)]

    count = 0

    for quadrant in range(6):
        for row in range(3):
            for column in range(5):
                table[quadrant][row][column] = numbers[count]
                count += 1

    return table


def flattenQuadrant(quadrant):
    return [item for sublist in quadrant for item in sublist]


def checkTable(table, listOfQuadrants, listOfRows):

    for quadrant in table:
        for validQuadrant in listOfQuadrants:
            if set(flattenQuadrant(quadrant)).issubset(flattenQuadrant(validQuadrant)):
                print('Repeated quadrant', quadrant, validQuadrant)
                return False, listOfQuadrants, listOfRows

        for row in quadrant:
            for validRow in listOfRows:
                if set(row).issubset(validRow):
                    print('Repeated row', row, validRow)
                    return False, listOfQuadrants, listOfRows

    for quadrant in table:
        listOfQuadrants.append(quadrant)
        for row in quadrant:
            listOfRows.append(row)

    return True, listOfQuadrants, listOfRows


def generateValidTables(totalTables, initialSeed=0):
    print('Generation of Quinto tables started, please wait...')
    print('Press CTRL-C at any time to stop the generation and validation of Quinto tables if it takes too long.')

    possibleNumbers = list(range(1, 91))

    validTables = []

    listOfQuadrants = []
    listOfRows = []

    seed = initialSeed

    try:

        while len(validTables) < totalTables:

            shuffledNumbers = shuffle(possibleNumbers, seed)
            seed += 1

            generatedTable = generateTable(shuffledNumbers)

            check, listOfQuadrants, listOfRows = checkTable(generatedTable, listOfQuadrants, listOfRows)

            if check:
                # validTables.append(shuffledNumbers)
                validTables.append(generatedTable)

    except KeyboardInterrupt:
        print('The generation of Quinto tables has been interrupted.')

    print('The total number of generated tables is:', len(validTables))

    return validTables

def quinto2CSV(quinto):

    for t in range(len(validTables)):
        
        table4CSV = []

        for l in range(9):
            line = validTables[t][int(l/3)*2][l%3] + validTables[t][int(l/3)*2+1][l%3]
            table4CSV.append(line)
        
        filename = './output/quinto_'+ str(t+1).zfill(math.floor(math.log10(len(validTables))+1)) +'.csv'

        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(table4CSV)
        except:
            print('Error writing CSV file:', filename)
            return False

    return True


if __name__ == '__main__':
    validTables = generateValidTables(10)
    quinto2CSV(validTables)


