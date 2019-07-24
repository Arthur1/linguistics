__author__ = 'Kazuki Asakura'

import csv

BEGIN_YEAR = 1980
END_YEAR = 2018
PICKUP_NUMBER = 100

def count_songs(ranking_type):
    count = 0
    songs_list = []
    for year in range(BEGIN_YEAR, END_YEAR + 1):
        f = open('./' + ranking_type + '_rankings/' + str(year) + '.csv', 'r')
        r = csv.reader(f)
        for row in r:
            key = row[1] + '_' + row[2]
            if key not in songs_list:
                songs_list.append(key)
                count += 1
        f.close()
    return count

term_dict = {}

f_karaoke = open('./term_frequency/sorted_karaoke.csv', 'r')
r_karaoke = csv.reader(f_karaoke)

count = 0
for row in r_karaoke:
    if count >= PICKUP_NUMBER:
        break
    count += 1
    if row[1] not in term_dict.keys():
        term_dict[row[1]] = [0, 0]
    term_dict[row[1]][0] = row[0]
    f_usen = open('./term_frequency/sorted_usen.csv', 'r')
    r_usen = csv.reader(f_usen)
    for row2 in r_usen:
        if row2[1] == row[1]:
            term_dict[row[1]][1] = row2[0]
            break
    f_usen.close()
f_karaoke.close()

f_usen = open('./term_frequency/sorted_usen.csv', 'r')
r_usen = csv.reader(f_usen)
count = 0
for row in r_usen:
    if count >= PICKUP_NUMBER:
        break
    count += 1
    if row[1] not in term_dict.keys():
        term_dict[row[1]] = [0, 0]
    term_dict[row[1]][1] = row[0]
    if not term_dict[row[1]][0] == 0:
        continue
    f_karaoke = open('./term_frequency/sorted_karaoke.csv', 'r')
    r_karaoke = csv.reader(f_karaoke)
    for row2 in r_karaoke:
        if row2[1] == row[1]:
            term_dict[row2[1]][0] = row2[0]
            break
    f_karaoke.close()
f_usen.close()

count_karaoke = count_songs('karaoke')
count_usen = count_songs('usen')

f_result = open('./pickup/result.csv', 'w')
w_result = csv.writer(f_result)
for term, values in term_dict.items():
    w_result.writerow([term, int(values[0]) / float(count_karaoke), int(values[1]) / float(count_usen)])
f_result.close()
