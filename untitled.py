from flask import Flask
from datetime import datetime
import mongoDb
import shiyebian_worm
app = Flask(__name__)


@app.route('/')
def hello_world():
    return '''
    <html>
      <head>
        <title>hello python</title>
      </head>
      <body>
        <a href=\'/shiye\'>查询事业单位</a><br>
        <a href=\'/time\'>time</a>
      </body>
    </html>
    '''


@app.route('/time')
def time():
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')


@app.route('/shiye')
def check():
    url = 'http://www.shiyebian.net/hebei/'
    my_dict = shiyebian_worm.parse_html(shiyebian_worm.download_html(url))
    res = ''
    coll = mongoDb.get_collection(mongoDb.get_db())
    for key in my_dict:
        if mongoDb.find(coll, key):
            print('有了')
            res = res + '<li><a href =\'' + my_dict[key] + '\' target=\'_blank\'>' + key + '</a></li>'
        else:
            mongoDb.insert_doc(coll, key, my_dict[key])
            res = res + '<li><a href =\'' + my_dict[key] + '\' target=\'_blank\'>[new]' + key + '</a></li>'

    print(res)
    for item in coll.find():
        print(item)
    html = '''
    <html>
      <head>
        <title>邯郸事业单位</title>
      </head>
      <body>
        <ol>
        ''' + res + '''
        </ol>
      </body>
    </html>
    '''
    return html


if __name__ == '__main__':
    app.run()
