# encoding=utf-8

import logging
import re

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
            r.encoding = 'gbk'
            html = r.text
            return BeautifulSoup(html, 'html.parser')
        else:
            raise RequestException('url:' + str(url) + ',status code:' + str(r.status_code))
    except requests.RequestException as e:
        raise RequestException(e)


def parse_shengshi(soup, keyword=''):
    lie1 = soup.find('ul', attrs={'class', 'lie1'})
    if lie1 == None:
        return parse_quxian(soup, keyword=keyword)
    my_list = []
    for li in lie1.find_all('li'):
        content = li.getText()
        if keyword in content:
            my_dict = {}
            content_url = li.find('a')['href']
            my_dict['url'] = content_url
            my_list.append(my_dict)
            #  获取链接内容
            # soup = BeautifulSoup(download_html(content_url))
            # div = soup.find('div', attrs={'class', 'zhengwen'})
            # for p in div.find_all('p'):
            #     print(p.getText())
            # 查找时间
            date_regex = re.compile(r'\d\d-\d\d\d\d\d\d')
            date = date_regex.search(content)
            if date is not None:
                date = date.group()
                # %Y-%m-%d
                str_date = date[5:] + '-' + date[:5]
                my_dict['date'] = str_date
                my_dict['title'] = content[10:]
            else:
                my_dict['date'] = ''
                my_dict['title'] = content
    return my_list


def parse_quxian(soup, keyword=''):
    lie_qx = soup.find('div', attrs={'class', 'lie_qx'})
    my_list = []
    for a in lie_qx.find_all('a'):
        content = a.getText()
        if not '查看详情' in content:
            if keyword in content:
                href = a['href']
                my_dict = {}
                my_dict['url'] = href
                # 查找时间
                date_regex = re.compile(r'\d\d-\d\d\d\d\d\d')
                date = date_regex.search(content)
                if isinstance(date, str):
                    # %Y-%m-%d
                    str_date = date[5, :] + '-' + date[:5]
                    my_dict['date'] = str_date
                    my_dict['title'] = content[10:]
                else:
                    my_dict['date'] = ''
                    my_dict['title'] = content
                my_list.append(my_dict)
    return my_list


def get_list_province(soup):
    province_list = []
    diqu = soup.find('div', attrs={'class', 'diqu'})
    for a in diqu.find_all('a'):
        province = {}
        province['province'] = a.getText()
        province['href'] = a['href']
        province_list.append(province)
    return province_list


def main():
    url = 'http://www.shiyebian.net/hebei/'
    parse_shengshi(download_html(url))


if __name__ == '__main__':
    main()
