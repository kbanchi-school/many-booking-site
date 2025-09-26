from flask import render_template, request, redirect, url_for
from . import top_bp

from database import Person

# Person画面表示
@top_bp.route('/')
def top():
    persons = Person.select()
    return render_template('top.html', persons=persons)

# Person登録
@top_bp.route('/person', methods=['POST'])
def person():
    name = request.form['name']
    age = request.form['age']
    Person.create(name=name, age=age)
    return redirect("/top")

# Person 詳細画面表示
@top_bp.route('/detail/<id>')
def detail(id):
    person = Person.get(Person.id == id)
    return render_template('top_detail.html', person=person)
