from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
import time
import re


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

            # imgを取得
            img_src = movieDetail['src']
            big_img_url = re.sub('2\.jpg$', '4.jpg', img_src)
            f.write(str(title) + ',' + str(big_img_url) + '\n')
        except AttributeError as e:
            print(e)

def main():
    geo_url = 'http://rental.geo-online.co.jp/search2/q/c-dvd/d-desc/o-rating/p-'
    geo_param = '/st-2/stk-1/'
    csv_file_name = 'geo.csv'
    page = 1
    try:
        f = open('geo.csv', mode='a', encoding='utf8')

        # while(page < 10):
        resource = get_web_esource(geo_url + str(page) + geo_param)
        read_resource = resource.read()
        bs_obj = BeautifulSoup(read_resource, 'lxml')
        imgs = bs_obj.find('ul', {'id': 'searchResultItem'}).findAll('img')
        get_movie_title_and_img(imgs, f)
        time.sleep(1)
        page = page + 1
    except AttributeError as e:
        print(e)
    except IOError as e:
        print(e)

    f.close()

if __name__ == '__main__':
    main()

