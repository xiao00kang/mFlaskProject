# coding=utf-8
from flask import Flask, render_template
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
    my_dict  = shiyebian_worm.get_list_diqu(shiyebian_worm.download_html(URL_SHIYE))
    return render_template('result.html', old_dict=my_dict)


def search_default():
    return search_default_index('')


@app.route('/shiye/<string:keyword>/')
def search_default_index(keyword):
    return search_with_index(keyword=keyword, index=1)


@app.route('/shiye/<string:keyword>/<int:index>')
def search_with_index(keyword, index):
    url = 'http://www.shiyebian.net/'+keyword
    if index != 1:
        url = url + 'index_' + str(index) + '.html'
    my_dict = shiyebian_worm.parse_html(shiyebian_worm.download_html(url))
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


if __name__ == '__main__':
    app.run()
