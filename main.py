from flask import Blueprint,render_template,url_for,request,redirect
from flask_login import login_required,current_user
from datetime import datetime
import itertools
from .models import Todo,Inprogress,Done,User
from . import db

main=Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('welcome.html')

@login_required
@main.route('/home')
def home():
    user = current_user.username
    categories = ['Marketting', 'Design', 'Development']
    tables= ['todo','inprogress','done']
    category_row = []
    for category in categories:
        table_row=[]
        for table in tables:
            if table == 'todo':
                row = Todo.query.filter_by(username=user,category=category)
                table_row.append(row)

            elif table == 'inprogress':
                row = Inprogress.query.filter_by(username=user,category=category)
                table_row.append(row)

            elif table == 'done':
                row = Done.query.filter_by(username=user,category=category)
                table_row.append(row)

        category_row.append(table_row)
    return render_template('index.html',category_row=category_row,user=user,categories=categories,tables=tables)

@login_required
@main.route('/statistics')
def statistics():
    user = current_user.username
    categories = ['Marketting', 'Design', 'Development']
    tables= ['todo','inprogress','done']
    barcolor = ['#4CAF50', '#2196F3', '#f44336']

    row = Todo.query.filter_by(username=user)
    c1 = row.count()
    row = Inprogress.query.filter_by(username=user)
    c2 = row.count()
    row = Done.query.filter_by(username=user)
    c3 = row.count()
    print(c1,c2,c3)
    category_row = []
    for category in categories:
        table_row=[]
        for table in tables:
            if table == 'todo':
                row = Todo.query.filter_by(username=user,category=category)
                if c1==0:
                    table_row.append(0)
                else:
                    table_row.append(int((row.count()/c1)*100))

            elif table == 'inprogress':
                row = Inprogress.query.filter_by(username=user,category=category)
                if c2==0:
                    table_row.append(0)
                else:
                    table_row.append(int((row.count()/c2)*100))


            elif table == 'done':
                row = Done.query.filter_by(username=user,category=category)
                if c3==0:
                    table_row.append(0)
                else:
                    table_row.append(int((row.count()/c3)*100))

        category_row.append(table_row)
    return render_template('statistics.html',category_row=category_row,user=user,categories=categories,tables=tables,barcolor=barcolor)


@login_required
@main.route('/new',methods=['GET','POST'])
def new_task():
    category = request.args.get('category')
    table = request.args.get('table')
    if request.form.get('save'):
        title=request.form.get('task')
        desc=request.form.get('desc')
        date=datetime.now()
        date=date.strftime('%d/%m/%Y %H:%M')

        newtask = Todo(title=title, desc=desc, date=date, category=category, username=current_user.username)
        if table=='inprogress':
            newtask = Inprogress(title=title,desc=desc,date=date,category=category,username=current_user.username)

        elif table=='done':
            newtask = Done(title=title,desc=desc,date=date,category=category,username=current_user.username)

        db.session.add(newtask)
        db.session.commit()
        return redirect(url_for('main.home'))

    else:
        return render_template('newtask.html',user=current_user.username,category=category,table=table)

@login_required
@main.route('/item/<id>')
def show_task(id):
    id=id
    table = request.args.get('table')

    row = Todo.query.filter_by(id=id).first()
    if table == 'inprogress':
        row = Inprogress.query.filter_by(id=id).first()
    elif table == 'done':
        row = Done.query.filter_by(id=id).first()
    return render_template('item.html', row=row, id=id, table=table, user=current_user.username)

@login_required
@main.route('/edit',methods=['GET','POST'])
def edit_item():
    id = request.args.get('id')
    table = request.args.get('table')

    row = Todo.query.filter_by(id=id).first()

    if request.form.get('save'):
        title=request.form.get('task')
        desc=request.form.get('desc')
        date=datetime.now()

        if table == 'inprogress':
            row = Inprogress.query.filter_by(id=id).first()
        elif table == 'done':
            row = Done.query.filter_by(id=id).first()

        row.title = title
        row.desc = desc
        row.date = date
        db.session.commit()

        return redirect(url_for('main.home'))

    else:
        if table == 'todo':
            row = Todo.query.filter_by(id=id).first()
        elif table == 'inprogress':
            row = Inprogress.query.filter_by(id=id).first()
        elif table == 'done':
            row = Done.query.filter_by(id=id).first()

    return render_template('edittask.html', id=id, row=row, table=table)

@login_required
@main.route('/remove',methods=['GET','POST'])
def remove_item():
    user = current_user.username
    id = request.args.get('id')
    table = request.args.get('table')

    row = Todo.query.filter_by(id=id).first()
    if table == 'inprogress':
        row = Inprogress.query.filter_by(id=id).first()
    elif table == 'done':
        row = Done.query.filter_by(id=id).first()

    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('main.home'))

@login_required
@main.route('/move',methods=['GET','POST'])
def move_item():
    user = current_user.username
    id = request.args.get('id')
    table = request.args.get('table')
    moveto = request.args.get('moveto')

    row = Todo.query.filter_by(id=id).first()
    if table == 'inprogress':
        row = Inprogress.query.filter_by(id=id).first()

    elif table == 'done':
        row = Done.query.filter_by(id=id).first()

    title=row.title
    desc=row.desc
    date=row.date
    category=row.category
    db.session.delete(row)
    db.session.commit()

    if moveto == 'todo':
        row = Todo(title=title,desc=desc,date=date,category=category,username=current_user.username)

    elif moveto == 'inprogress':
        row = Inprogress(title=title,desc=desc,date=date,category=category,username=current_user.username)

    elif moveto == 'done':
        row = Done(title=title,desc=desc,date=date,category=category,username=current_user.username)

    db.session.add(row)
    db.session.commit()
    return redirect(url_for('main.home'))
