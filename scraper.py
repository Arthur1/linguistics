# カラオケランキング情報を取得し、その歌詞をtxtファイルで取得する
__author__ = 'Kazuki Asakura'

import csv
import os
import re
import time
import urllib.request
from bs4 import BeautifulSoup

# 定数
KARAOKE_RANKINGS_DIR = './karaoke_rankings/'
USEN_RANKINGS_DIR = './usen_rankings/'
LYRICS_DIR = './lyrics/'
LOGS_DIR = './logs/'
RANKING_NUM = 20
BEGIN_YEAR = 1980
END_YEAR = 2018

# ランキングを取得し、CSVに書き出す
def get_ranking(term):
    if term == 'karaoke':
        url_term = 'karaoke'
    elif term == 'usen':
        url_term = 'usen_rank_'
    else:
        raise Exception
    # 開始年から終了年までループ
    for year in range(BEGIN_YEAR, END_YEAR + 1):
        print('Download Ranking Table: ' + term + '/' + str(year) + '年')
        # 書き込むCSVを開く
        f = open(KARAOKE_RANKINGS_DIR + str(year) + '.csv', 'w')
        writer = csv.writer(f, lineterminator='\n')
        # URLにアクセス
        url = 'https://entamedata.web.fc2.com/music2/' + url_term + str(year) + '.html'
        response = urllib.request.urlopen(url)
        bs = BeautifulSoup(response.read(), 'lxml')
        time.sleep(1)
        # ランキングの要素を選択
        table = bs.find('table', attrs={'cellpadding': '5'})
        rows = table.findAll('tr')
        # 各行のデータを取得しCSVに書き込む
        for rank in range(1, RANKING_NUM + 1):
            row = rows[rank]
            cells = row.findAll('td', class_='sample3')
            title = cells[0].find('a').string
            artist = cells[1].find('a').string
            writer.writerow([str(rank), title, artist])
            # まだその曲の歌詞を取得していないなら取得
            lyric_path = LYRICS_DIR + title.replace('/', '') + '_' + artist.replace('/', '') + '.txt'
            if not os.path.exists(lyric_path):
                print('    Download Lyric: ' + title + '/' + artist)
                get_lyric(title, artist)
        f.close()

# URLを指定したcsvを利用して歌詞を取得
def get_lyrics_static():
    f = open(LOGS_DIR + 'uniq_get_lyric.csv', 'r')
    reader = csv.reader(f, lineterminator='\n')
    for row in reader:
        if row[2] is '':
            continue
        print('    Download Lyric: ' + row[0] + '/' + row[1])
        get_lyric(row[0], row[1], row[2])
    f.close()

# 曲名とからJ-LyricのURLを得る
def get_lyric_url(title, artist):
    # 検索用URL生成
    query = {
        'kt': payload_filter(title),
        'ct': 2,
        'ka': payload_filter(artist),
        'ca': 2,
        'kl': '',
        'cl': 2,
    }
    query_str = urllib.parse.urlencode(query)
    search_url = 'http://search.j-lyric.net/index.php?' + query_str
    # URLにアクセス
    response = urllib.request.urlopen(search_url)
    bs = BeautifulSoup(response.read(), 'lxml')
    time.sleep(1)
    # URLが含まれる要素を選択
    element = bs.find('div', id='mnb').find('div', class_='bdy').find('p', class_='mid').find('a')
    # 属性値からURLを得る
    lyric_url = element.get('href')
    return lyric_url

# 検索時に不要な記号などを取り除く
def payload_filter(str):
    str = re.sub('[(-〜].+?[)-〜]', '', str)
    str = str.replace('･', '').replace('…', '').replace('＆', '').replace('.', '')
    return str

# 歌詞をtxtファイルに書き出す
def get_lyric(title, artist, url=None):
    # URLにアクセス
    try:
        if url is None:
            url = get_lyric_url(title=title, artist=artist)
        response = urllib.request.urlopen(url)
        bs = BeautifulSoup(response.read(), 'lxml')
        time.sleep(1)
        # 歌詞が含まれる要素を選択
        element = bs.find('div', id='mnb').find('div', class_='lbdy').find('p', id='Lyric')
    except AttributeError:
        print('        Not Found.')
        # エラーログ
        f = open(LOGS_DIR + 'get_lyric.csv', 'a')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([title, artist])
        f.close()
        return
    # 対象要素から不要なタグを削除
    lyric = str(element).replace('<p id="Lyric">', '').replace('</p>', '').replace('<br/>', '\n')
    # ファイルに出力
    f = open(LYRICS_DIR + title.replace('/', '') + '_' + artist.replace('/', '') + '.txt', 'w')
    f.write(lyric)
    f.close()

get_ranking('karaoke')
get_ranking('usen')
# get_lyrics_static()
