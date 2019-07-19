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

def term_frequency_by_type(ranking_type):
    music_list = []
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')

    # 2つのランキングについてループ
    term_frequency_dict = {}
    # 開始年から終了年までループ
    for year in range(BEGIN_YEAR, END_YEAR + 1):
        f_rank = open('./' + ranking_type + '_rankings/' + str(year) + '.csv', 'r')
        r_rank = csv.reader(f_rank, lineterminator='\n')
        # ランキングの各レコードについてループ
        for row in r_rank:
            lyric_file_name = row[1].replace('/', '') + '_' + row[2].replace('/', '')
            if lyric_file_name in music_list:
                continue
            music_list.append(lyric_file_name)
            try:
                f_lyric = open(LYRICS_DIR + lyric_file_name  + '.txt', 'r')
            except:
                continue
            # 歌詞の各行についてループ
            for line in f_lyric:
                node = tagger.parseToNode(line)
                while node:
                    wclass = node.feature.split(',')
                    term = wclass[6]
                    node = node.next
                    if wclass[0] in ['BOS/EOS', '助詞', '助動詞', '接続詞', '記号', '連体詞', 'フィラー', '感動詞']:
                        continue
                    if wclass[1] in ['接尾', '非自立']:
                        continue
                    if term in ['くり返し', '　', '*']:
                        continue
                    # tfリストに追加
                    if term in term_frequency_dict:
                        term_frequency_dict[term] += 1
                    else:
                        term_frequency_dict[term] = 1
            f_lyric.close()
        f_rank.close()
    f_result = open('./term_frequency/' + ranking_type + '.csv', 'w')
    writer = csv.writer(f_result, lineterminator='\n')
    for term, count in term_frequency_dict.items():
        writer.writerow([str(count), term])
    f_result.close()

term_frequency_by_type('karaoke')
term_frequency_by_type('usen')
