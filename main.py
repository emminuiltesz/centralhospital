from flask import Flask, render_template, request, url_for, flash, g, abort, redirect
import sqlite3
import os
from FDataBase import FDataBase
import math
import requests
import time

DATABASE = "tmp/flsite.db"
DEBUG = True
SECRET_KEY = "fdgdfgdfggf786hfg6hfg6h7f"
con = sqlite3.connect('flsite.db')

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
r = requests.get('https://almetkvantorium@yandex.ru:d7nv39rawVobcui81'
                 'cjOUIS2am7@gate.smsaero.ru/v2/auth')


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


menu = [{"name": "Главная", "url": "major"},
        {"name": "Страница врача", "url": "doctor"},
        {"name": "Добавление записи", "url": "add_post"},
        ]


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)


@app.route("/major")
def major():
    return render_template('major.html', title="Главная", menu=menu)


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)
    tm = math.floor(time.time())
    if request.method == "POST":
        if len(request.form['surname']) > 2 and len(request.form['name']) > 1 and len(request.form['third_name']) > 2\
            and len(request.form['phone']) > 2 and len(request.form['email']) > 2 and len(request.form['times_h']) > 1 \
                and len(request.form['times_m']) > 1 and len(request.form['simptom']) > 1:
            res = dbase.addPost(request.form['surname'], request.form['name'], request.form['third_name'],
                                request.form['phone'],request.form['email'], request.form['times_h'],
                                request.form['times_m'], request.form['simptom'], 'Неизвестно')
            if not res:
                flash('Ошибка добавления записи', category='error')
            else:
                flash('Запись добавлена успешно', category='success')
                time.sleep(2)
                time_tuple = (2020, 12, 4, int(request.form['times_h']), int(request.form['times_m']), 00, 2, 317, 0)
                timestamp = time.mktime(time_tuple)
                timestmp = str(int(timestamp))  # дата пользователя в unixtime
                print(timestmp)
                print(type(timestmp))
                r = requests.get('https://almetkvantorium@yandex.ru:d7nv39rawVobcui81cjOUIS2am7@gate.smsaero.ru/v2/'
                                 'sms/send?numbers[]='+request.form['phone']+'&text=localhost/status/'+str(
                                  request.form['phone'])+'&sign=SMS Aero&dateSend='+timestmp)
                return redirect('/succses/'+request.form['phone']+'/'+request.form['name'])
        else:
            flash('Ошибка добавления записи', category='error')

    return render_template('add_post.html', menu=menu, title="Добавление записи")


@app.route('/succses/<int:phonenumber>/<name>')
def succses(phonenumber,name):
    return render_template('succses.html', phonenumber=phonenumber, name=name)  # ваш id такой то добавить


@app.route('/status/<int:phone>')
def status(phone):
    if phone:
        conn = sqlite3.connect("flsite.db")
        cursor = conn.cursor()
        sql = 'UPDATE mainmenu SET status=? WHERE phone = ?'
        data = ("Придёт", phone)
        cursor.execute(sql, data)
        conn.commit()
        return 'Успешно'


@app.route("/patient/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    surname, name, third_name, phone, email, times_h, times_m, simptom, status = dbase.getPost(id_post)
    if not surname:
        abort(404)
    return render_template('patient.html', menu=dbase.getMenu(), surname=surname, name=name, third_name=third_name,
                           phone=phone, email=email, times_h=times_h, times_m=times_h, simptom=simptom, status=status)


@app.route("/doctor", methods=["POST", "GET"])
def patient():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', title="Страница пациента", menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
