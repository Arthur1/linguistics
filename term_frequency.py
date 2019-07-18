__author__ = 'Kazuki Asakura'

import csv
import MeCab
import os

# 定数
KARAOKE_RANKINGS_DIR = './karaoke_rankings/'
USEN_RANKINGS_DIR = './usen_rankings/'
LYRICS_DIR = './lyrics/'
LOGS_DIR = './logs/'
RANKING_NUM = 20
BEGIN_YEAR = 1980
END_YEAR = 2018

tagger = MeCab.Tagger('-Ochasen')
tagger.parse('')

# 2つのランキングについてループ
for ranking_type in ['karaoke', 'usen']:
    term_frequency_list = {}
    # 開始年から終了年までループ
    for year in range(BEGIN_YEAR, END_YEAR + 1):
        f_rank = open('./' + ranking_type + '_rankings/' + str(year) + '.csv', 'r')
        r_rank = csv.reader(f_rank, lineterminator='\n')
        # ランキングの各レコードについてループ
        for row in r_rank:
            try:
                f_lyric = open(LYRICS_DIR + row[1].replace('/', '') + '_' + row[2].replace('/', '')  + '.txt', 'r')
            except:
                continue
            # 歌詞の各行についてループ
            for line in f_lyric:
                node = tagger.parseToNode(line)
                while node:
                    wclass = node.feature.split(',')
                    term = wclass[6]
                    # print(wclass)
                    node = node.next
                    if wclass[0] in ['BOS/EOS', '助詞', '助動詞', '接続詞', '記号', '連体詞']:
                        continue
                    if term in ['くり返し', '　', '*']:
                        continue
                    # tfリストに追加
                    if term in term_frequency_list:
                        term_frequency_list[term] += 1
                    else:
                        term_frequency_list[term] = 1
            f_lyric.close()
        f_rank.close()
    f_result = open('./term_frequency/' + ranking_type + '.csv', 'w')
    writer = csv.writer(f_result, lineterminator='\n')
    print(term_frequency_list)
    for term, count in term_frequency_list.items():
        writer.writerow([str(count), term])
    f_result.close()
