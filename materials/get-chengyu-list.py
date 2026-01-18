import os, csv
from zhconv import convert

# Set working directory to the location of this .py file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('four-cha-words.csv', 'r', encoding = 'utf-8') as inputfile1:
    cr = csv.reader(inputfile1)
    sublex_content = [line for line in cr]

with open('chengyu.txt', 'r', encoding = 'utf-8') as inputfile2:
    chengyu_list_2 = [convert(x.replace("\n", ""), 'zh-hans') for x in inputfile2]
    chengyu_list_2 = list(set(chengyu_list_2))

with open('idiom.csv', 'r', encoding = 'utf-8') as inputfile3:
    cr = csv.reader(inputfile3)
    chengyu_list_temp = [line[4] for line in cr]
    chengyu_list_temp.remove("word")
    chengyu_list_3 = []
    for element in chengyu_list_temp:
        if len(element) == 4:
            chengyu_list_3.append(element)
    # random.shuffle(chengyu_list_3)
    chengyu_list_3 = list(set(chengyu_list_3))
    # print(len(chengyu_list_3))

with open('additional.csv', 'r', encoding='utf-8') as inputfile4:
    cr = csv.reader(inputfile4)
    chengyu_list_4 = [line[0] for line in cr]

chengyu_ciku = list(set(chengyu_list_3 + chengyu_list_2 + chengyu_list_4))
chengyu_list_1 = [line[:2] for line in sublex_content if line[0] in chengyu_ciku]
#print(chengyu_list_1)

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

subtlex_list = [row[0] for row in chengyu_list_1]
chengyu_list = subtlex_list + chengyu_list_2 + chengyu_list_3 + chengyu_list_4
# print(chengyu_list[:100])

print(chengyu_list[:10])

# check whether all characters used in chengyus are in the character corpus
all_chengyu_char = list(set(''.join(chengyu_list)))
not_in = []
for i in range(len(all_chengyu_char)):
    if all_chengyu_char[i] not in [c[1] for c in filecontents]:
        not_in.append(all_chengyu_char[i])
not_in = list(set(not_in))
print(not_in)

# order chengyu_lists
frequency_ranks = dict()
for c in filecontents:
    frequency_ranks[c[1]] = c[0]
# print(frequency_ranks)
frequency_dictionary = dict()
for chengyu in chengyu_ciku:
    chars = list(chengyu)
    score = 0
    for char in chars:
        try:
            frequency = float(frequency_ranks[char])
        except:
            frequency = 14976
        score += frequency
    frequency_dictionary[chengyu] = score

print(len(chengyu_ciku))
chengyu_ciku = [element[0] for element in sorted(frequency_dictionary.items(), key=lambda item: item[1])]
print(chengyu_ciku[:10])
print(len(chengyu_ciku))

with open('chengyu-list.csv', 'w', encoding = 'utf-8') as outputfile:
    cw = csv.writer(outputfile, lineterminator = '\n')
    for row in chengyu_list_1:
        cw.writerow(row)
    for chengyu in chengyu_ciku:
        if chengyu not in subtlex_list:
            if not any(char in chengyu for char in not_in):
                cw.writerow([chengyu, 0])
    # for chengyu in chengyu_list_3:
    #     if chengyu not in subtlex_list and chengyu not in chengyu_list_4:
    #         if not any(char in chengyu for char in not_in):
    #             cw.writerow([chengyu, 0])
    # for chengyu in chengyu_list_2:
    #     if chengyu not in subtlex_list and chengyu not in chengyu_list_3:
    #         if not any(char in chengyu for char in not_in):
    #             cw.writerow([chengyu, 0])

with open('character-rank.csv', 'a', encoding='utf-8') as output:
        cw = csv.writer(output, lineterminator = '\n')
        # i = 14975
        # for item in set(not_in):
        #     cw.writerow([i+1, item])
        #     i += 1