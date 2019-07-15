# カラオケランキング情報を取得し、その歌詞をtxtファイルで取得する

__author__ = 'Kazuki Asakura'

import urllib.request
from bs4 import BeautifulSoup
import re
import time

# 曲名とからJ-LyricのURLを得る
def get_lyric_url(title, artist):
    # 検索用URL生成
    query = {'kt': title, 'ct': 2, 'ka': artist, 'ca': 2, 'kl': '', 'cl': 2,}
    query_str = urllib.parse.urlencode(query)
    search_url = 'http://search.j-lyric.net/index.php?' + query_str
    # URLにアクセス
    response = urllib.request.urlopen(search_url)
    bs = BeautifulSoup(response.read(), 'lxml')
    time.sleep(1)
    # URLが含まれる要素を選択
    element = bs.find('div', id='mnb').find('div', class_='bdy').find('p', class_='mid').find('a')
    # 属性値からURLを得る
    url = element.get('href')
    return url


# 歌詞をtxtファイルに保存する
def get_lyric(url):
    # URLにアクセス
    response = urllib.request.urlopen(url)
    bs = BeautifulSoup(response.read(), 'lxml')
    # 歌詞が含まれる要素を選択
    element = bs.find('div', id='mnb').find('div', class_='lbdy').find('p', id='Lyric')
    # 対象要素から不要なタグを削除
    lyric = str(element).replace('<p id="Lyric">', '').replace('</p>', '').replace('<br/>', '\n')
    # ファイルに出力
    f = open('test.txt', 'w')
    f.write(lyric)
    f.close()

url = get_lyric_url(title='真夏の夜の夢', artist='松任谷由実')
print(url)
get_lyric(url)
