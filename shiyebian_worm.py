# encoding=utf-8

import logging
import requests
from bs4 import BeautifulSoup
from exception import *

logging.basicConfig(level=logging.INFO)


def download_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    try:
        r = requests.get(url, headers)
        if r.ok:
            html = r.content
            return BeautifulSoup(html, 'html.parser')
        else:
            raise RequestException('url:'+str(url)+',status code:'+r.status_code)
    except requests.RequestException as e:
        raise RequestException(e)


def parse_shengshi(soup, keyword=''):
    print(get_list_province(soup))
    lie1 = soup.find('ul', attrs={'class', 'lie1'})
    i = 0
    for li in lie1.find_all('li'):
        content = li.getText()
        my_list = []
        if keyword in content:
            i += 1
            my_dict = {}
            content_url = li.find('a')['href']
            my_dict['title'] = content
            my_dict['url'] = content_url
            my_list.append(my_dict)
            #  获取链接内容
            # soup = BeautifulSoup(download_html(content_url))
            # div = soup.find('div', attrs={'class', 'zhengwen'})
            # for p in div.find_all('p'):
            #     print(p.getText())
    return my_list


def get_list_province(soup):
    province_list = []
    diqu = soup.find('div', attrs={'class', 'diqu'})
    for a in diqu.find_all('a'):
        province ={}
        province['province'] = a.getText()
        province['href'] = a['href']
        province_list.append(province)
    return province_list


def main():
    url = 'http://www.shiyebian.net/hebei/'
    parse_shengshi(download_html(url))


if __name__ == '__main__':
    main()
