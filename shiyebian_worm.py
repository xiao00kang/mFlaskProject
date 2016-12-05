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
    print(get_list_diqu(soup))
    lie1 = soup.find('ul', attrs={'class', 'lie1'})
    i = 0
    my_dict = {}
    for li in lie1.find_all('li'):
        content = li.getText()

        if keyword in content:
            i += 1
            content_url = li.find('a')['href']
            # print(i, content)
            # print(content_url)
            my_dict[content] = content_url
            #  获取链接内容
            # soup = BeautifulSoup(download_html(content_url))
            # div = soup.find('div', attrs={'class', 'zhengwen'})
            # for p in div.find_all('p'):
            #     print(p.getText())
    return my_dict


def get_list_diqu(soup):
    diqu_dict = {}
    diqu = soup.find('div', attrs={'class', 'diqu'})
    for a in diqu.find_all('a'):
       diqu_dict[a.getText()] = '/shiye'+a['href']
    return diqu_dict


def main():
    url = 'http://www.shiyebian.net/hebei/'
    parse_shengshi(download_html(url))


if __name__ == '__main__':
    main()
