import os, csv

# Set working directory to the location of this .py file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('four-cha-words.csv', 'r', encoding = 'utf-8') as inputfile1:
    cr = csv.reader(inputfile1)
    filecontents = [line for line in cr]
    with open('chengyu.txt', 'r', encoding = 'utf-8') as inputfile2:
        chengyu_list = [x.replace("\n", "") for x in inputfile2]
        #print(chengyu_list[:10])
        with open('chengyu-list.csv', 'w', encoding = 'utf-8') as outputfile:
            cw = csv.writer(outputfile, lineterminator = '\n')
            first = True
            for row in filecontents:
                if first:
                    #cw.writerow(row[:2])
                    first = False
                elif row[0] in chengyu_list:
                    cw.writerow(row[:2])

with open('character-frequency.csv', 'r', encoding='utf-8') as input:
    cr = csv.reader(input)
    filecontents = [line for line in cr]
    with open('character-rank.csv', 'w', encoding='utf-8') as output:
        cw = csv.writer(output, lineterminator = '\n')
        first = True
        for row in filecontents:
            if first:
                first = False
            elif len(row) >0:
                cw.writerow(row[:2])