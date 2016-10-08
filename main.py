# coding=utf-8
from flask import Flask, render_template
from datetime import datetime
import mongoDb
import shiyebian_worm
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/time')
def time():
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')


@app.route('/shiye')
def check():
    url = 'http://www.shiyebian.net/hebei/'
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
