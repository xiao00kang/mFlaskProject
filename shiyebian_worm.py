# encoding=utf-8

import logging
import requests
from bs4 import BeautifulSoup
from collections import Iterator

logging.basicConfig(level=logging.INFO)


def download_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }

    html = requests.get(url, headers).content
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def parse_html(soup, keyword=''):
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
    for i in my_dict:
        logging.info(i)
        logging.info(my_dict[i])
    return my_dict


def get_list_diqu(soup):
    diqu_dict = {}
    diqu = soup.find('div', attrs={'class', 'diqu'})
    for a in diqu.find_all('a'):
       diqu_dict[a.getText()] = '/shiye'+a['href']
    return diqu_dict


def main():
    url = 'http://www.shiyebian.net/hebei/'
    parse_html(download_html(url))


if __name__ == '__main__':
    main()
