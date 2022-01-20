import random
import csv
import math
from fpdf import FPDF

totalTables = 100


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
    validLines = []

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
                validTables.append(generatedTable)

    except KeyboardInterrupt:
        print('The generation of Quinto tables has been interrupted.')

    print('The total number of generated tables is:', len(validTables))

    return validTables

def table2lines(table):

    lines= []

    for l in range(9):
        line = table[int(l/3)*2][l%3] + table[int(l/3)*2+1][l%3]
        lines.append(line)

    return lines

def quintoTables2CSV(tables):

    for t in range(len(tables)):

        quintoLines = table2lines(tables[t])        
        
        filename = './output/quinto_'+ str(t+1).zfill(math.floor(math.log10(len(tables))+1)) +'.csv'

        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(quintoLines)
        except:
            print('Error writing CSV file:', filename)
            return False

    return True


if __name__ == '__main__':
    validTables = generateValidTables(totalTables)
    quintoTables2CSV(validTables)

    # A5 dimensions: 210 x 148 mm
    # Margins: 10 (left) x 2 (top) x 10 (right) x 10 (bottom) mm
    # Title height: 10 mm
    # Available space for the table: 190 x 126 mm
    # Cells: 19 x 14 mm

    cellW = 19
    cellH = 14

    # Set up the page    
    pdf = FPDF(orientation='l', unit='mm', format='a5')
    pdf.set_auto_page_break(False)

    for t in range(len(validTables)):
        
        pdf.add_page()

        # Title
        pdf.set_xy(10, 2)
        pdf.set_font('helvetica', 'B', 18)
        pdf.cell(w=190, h=10, txt='Quinto nº' + str(t+1), border=0, ln=2, align='C')
        
        lines = table2lines(validTables[t])

        # Table
        pdf.set_font('helvetica', 'B', 24)
        pdf.set_line_width(0.2)
        for line in lines:
            for number in line:
                pdf.cell(w=cellW, h=cellH, txt=str(number), border=1, ln=0, align='C')
            pdf.cell(w=0, h=cellH, ln=1)
        
        pdf.set_xy(10,12)
        pdf.set_line_width(1)
        for col in range(2):
            for row in range(3):
                pdf.rect(x=10+col*cellW*5, y=12+row*cellH*3, w=cellW*5, h=cellH*3)

    pdf.output('./output/quinto.pdf', 'F')
    exit()


