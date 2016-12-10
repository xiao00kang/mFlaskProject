# coding=utf-8
import json

from flask import Flask, render_template, jsonify
from datetime import datetime
import mongoDb
import shiyebian_worm
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
URL_SHIYE = 'http://www.shiyebian.net/'


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/time')
def time():
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')


@app.route('/shiye/')
def shiye_search():
    t = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return render_template('result.html', time=t)


def search_default():
    return search_default_index('')


@app.route('/shiye/<string:keyword>/')
def search_default_index(keyword):
    return search_with_index(keyword=keyword, index=1)


@app.route('/shiye/<string:keyword>/<int:index>')
def search_with_index(keyword, index):
    url = 'http://www.shiyebian.net/' + keyword
    if index != 1:
        url = url + 'index_' + str(index) + '.html'
    my_dict = shiyebian_worm.parse_shengshi(shiyebian_worm.download_html(url))
    coll = mongoDb.get_collection(mongoDb.get_db())
    old_dict = {}
    new_dict = {}
    for key in my_dict:
        if mongoDb.find(coll, key):
            logging.info('此条信息数据库以含有')
            old_dict[key] = my_dict[key]
        else:
            mongoDb.insert_doc(coll, key, my_dict[key])
            new_dict[key] = my_dict[key]

    return render_template('result.html', old_dict=old_dict, new_dict=new_dict)


# 获取json数据 api
@app.route('/api/shiye', methods=["GET"])
def get_list_province():
    my_dict = shiyebian_worm.get_list_province(shiyebian_worm.download_html(URL_SHIYE))
    return json.dumps(my_dict, ensure_ascii=False)


@app.route('/api/shiye/<string:province>/', methods=["GET"])
def get_first_page_province(province):
    return get_province(province, index=1)


@app.route('/api/shiye/<string:province>/<int:index>', methods=["GET"])
def get_province(province, index):
    url = URL_SHIYE + province
    if index > 1:
        url = url + '/index_' + str(index) + '.html'
    my_dict = shiyebian_worm.parse_shengshi(shiyebian_worm.download_html(url))
    return json.dumps(my_dict, ensure_ascii=False)


@app.route('/api/shiye/<string:province>/<string:city>/', methods=["GET"])
def get_first_page_city_or_county(province, city):
    return get_city_or_county(province, city, index=1)


@app.route('/api/shiye/<string:province>/<string:city>/<int:index>', methods=["GET"])
def get_city_or_county(province, city, index):
    url = URL_SHIYE + province+'/'+city
    if index > 1:
        url = url + '/index_' + str(index) + '.html'
    my_dict = shiyebian_worm.parse_shengshi(shiyebian_worm.download_html(url))
    return json.dumps(my_dict,ensure_ascii=False)


if __name__ == '__main__':
    app.run()
