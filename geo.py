from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
import time
import re

site_url = 'http://rental.geo-online.co.jp/'

def get_web_esource(url):
    try:
        return urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print('The server could not be found!')
        return None


def get_movie_title_and_img(tag_movie_li, f):
    movie_list = []
    for movieDetail in tag_movie_li:

        try:
            # titleを取得
            title = movieDetail['alt'].strip()
            replace_title = re.sub('"', '\'', title)

            # imgを取得
            img_src = movieDetail['src']
            # f.write('"' + str(replace_title) + '",' + str(img_src) + '\n')
        except AttributeError as e:
            print(e)


def get_details_loop(links):
  for link_obj in links:
    link = link_obj['href']
    __write_csv(get_details(site_url + link))


'''
ほしいデータ
映画名
監督
ジャンル(,区切り)
主演(,区切り)
制作国
# 制作 テキスト検索する必要があるので一旦除外
# 脚本 テキスト検索する必要があるので一旦除外
# 収録時間 テキスト検索する必要があるので一旦除外
# メーカー テキスト検索する必要があるので一旦除外
画像URL
詳細ページURL
'''
def get_details(url):
  resource = get_web_esource(url)
  read_resource = resource.read()
  bs_obj = BeautifulSoup(read_resource, 'lxml')

  '''色々取得する'''
  article = bs_obj.find('article', {'id': 'item_info'})
  # 映画名
  _movie_title = article.find('h1')
  # 本題が存在しない場合がある
  if _movie_title.span:
    _movie_title.span.extract()

  movie_title = csv_format(_movie_title.text.strip())

  info_object = article.find('div', {'class': 'info'}).findAll('p')

  # 監督
  director = ''
  _director = info_object[0]
  if _director.a:
    a_list = _director.findAll('a')
    director = csv_format(a_list[0].text.strip())

  # ジャンル
  genre = ''
  _genre = info_object[1]
  if _genre.a:
    a_list = _genre.findAll('a')
    genre = csv_format(','.join([a.text.strip() for a in a_list]))

  # 主演
  actors = ''
  _actors = info_object[0]
  if _actors.a:
    a_list = _actors.findAll('a')
    # 最初の要素は監督なので、削除
    del a_list[0]
    actors = csv_format(','.join([a.text.strip() for a in a_list]))

  work_info = bs_obj.find('div', {'id': 'work_info'})
  # 制作国
  work_info_tr = work_info.findAll('tr')
  work_info_tr_1 = work_info_tr[1]
  work_info_td_a_list = work_info_tr_1.find('td').findAll('a')
  country_of_origin = csv_format(','.join([_a.text.strip() for _a in work_info_td_a_list]))

  # 画像URL
  img_obj = article.find('img', {'id': 'packageImage'})
  _img_src = img_obj['src']
  img_url = re.sub('3\.jpg', '2.jpg', _img_src)

  return [movie_title, director, genre, actors, country_of_origin, img_url, url]


def csv_format(_string):
  return '"' + re.sub('"', '\'', _string) + '"'


def __write_csv(save_lists):
  joins = ','.join(save_lists)
  f.write(joins + '\n')


def main():
    geo_url = 'http://rental.geo-online.co.jp/search2/q/c-dvd/d-desc/o-rating/p-'
    geo_param = '/st-2/stk-1/'
    csv_file_name = 'geo.csv'
    page = 1
    max_page = 2318
    try:
        global f
        f = open('geo.csv', mode='a', encoding='utf8')

        # while(page < max_page):
        resource = get_web_esource(geo_url + str(page) + geo_param)
        read_resource = resource.read()
        bs_obj = BeautifulSoup(read_resource, 'lxml')
        links = bs_obj.findAll('a', {'class': ['imagesLink', 'dvdmode']})

        get_details_loop(links)

        time.sleep(1)
        page = page + 1
    except AttributeError as e:
        print(e)
    except IOError as e:
        print(e)

    # f.close()

if __name__ == '__main__':
    main()

