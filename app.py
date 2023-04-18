from flask import Flask,render_template,url_for,request,g,session
from collections import deque
from datetime import datetime
import sqlite3
import re
app=Flask(__name__)
app.config['DEBUG']=True
app.secret_key="xyz"
def getTotal(date):
    total_dict={}
    sql=get_db()
    c=sql.cursor()
    food_items=dict(c.execute('SELECT fooditem FROM tdiet WHERE date=?',(date,)).fetchall(),['fooditem'])
    
    food_list=list()
    for food_item in food_items:
        food_list.append(food_item['fooditem'])
    food_Items_dict=[]
    sql=get_db()
    c=sql.cursor()
    for food_item in food_list:
        food_Items_dict.append(dict(c.execute('SELECT PROTEIN,CARBOHYDRATES,FAT,CALORIES FROM FOODS_LIST WHERE FOOD_NAME=?',(food_item,)).fetchall(),["PROTEIN","CARBOHYDRATES","FAT","CALORIES"]))
    string_data=str(food_Items_dict)
    total_dict['protein']=sum_data(re.findall("'PROTEIN':\s*(\d+)",string_data))
    total_dict['carbohydrates']=sum_data(re.findall("'CARBOHYDRATES':\s*(\d+)",string_data))
    total_dict['fat']=sum_data(re.findall("'FAT':\s*(\d+)",string_data))
    total_dict['calories']=sum_data(re.findall("'CALORIES':\s*(\d+)",string_data))
    session[date]=total_dict

def sum_data(string_list):
    sum=0
    for num in string_list:
        sum+=int(num)
    return sum
def getFoodListData(food_list):
    food_Items_dict={}
    sql=get_db()
    c=sql.cursor()
    for food_item in food_list:
        food_Items_dict[food_item]=dict(c.execute('SELECT PROTEIN,CARBOHYDRATES,FAT,CALORIES FROM FOODS_LIST WHERE FOOD_NAME=?',(food_item,)).fetchall(),["PROTEIN","CARBOHYDRATES","FAT","CALORIES"])
    return food_Items_dict
def getFoodItems(food_items):
    food_list=set()
    for food_item in food_items:
        food_list.add(food_item['fooditem'])
    return food_list
def dateformat(date)->"formatterdate" :
    date_obj=datetime.strptime(date,'%B %d,%Y')
    return date_obj.strftime('%Y-%m-%d')
def dateFormatting(home_data)->'dict':
    for data in home_data:
        pre_date=datetime.strptime(data['date'],'%Y-%m-%d').date()
        data['date']="{month} {day},{year}".format(month=pre_date.strftime('%B'),day=pre_date.day,year=pre_date.year)
    return home_data 

def getTablesList()->'tables_list':
    sql=get_db()
    cursor=sql.cursor()
    cursor_data=cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables=cursor_data.fetchall()
    tables_list=[x for y in tables for x in y]
    return tables_list
def dict(food_list,food_table_column):
    
    list=[]
    dicrt={}
    for i in food_list:
        headings=deque(food_table_column)
        for j in i:
            for k in headings:
                dicrt.setdefault(k,j)
                headings.popleft()
                break
        list.append(dicrt)
        dicrt={}
    return list

def connect_db()->'object':
    sql=sqlite3.connect('food_tracker')
    return sql

def get_db():
    if not hasattr(g,'sqlite3_db'):
        g.sqlite3_db=connect_db()
        '''g.sqlite3_db.row_factory=sqlite3.Row'''
    return g.sqlite3_db
@app.teardown_appcontext
def close_db(error):
    if hasattr('g','sqlite3_db'):
        g.sqlite3_db.close()   
    
@app.route('/')
@app.route('/home',methods=['POST','GET'])
def home()->'html':
    sql=get_db()
    cursor=sql.cursor()
    if 'diet' in getTablesList():
            print('exception handled')
    else:
        diet_tableQ="""CREATE TABLE diet(
            date TIMESTAMP PRIMARY KEY NOT NULL,
            tot_protein INTEGER NOT NULL,
            tot_carbohydrates INTEGER NOT NULL,
            tot_fat INTEGER NOT NULL,
            tot_calories INTEGER NOT NULL
        );"""
        cursor.execute(diet_tableQ)
        create_table_queary="""CREATE TABLE FOODS_LIST
        (SNO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        FOOD_NAME TEXT VARCHAR(30) UNIQUE NOT NULL,
        PROTEIN INTEGER NOT NULL,
        CARBOHYDRATES INTEGER NOT NULL,
        FAT INTEGER NOT NULL,
        CALORIES INTEGER NOR NULL);"""
        cursor.execute(create_table_queary)
    if request.method=='POST':
        data=request.get_json()
        diet_insertQ="""INSERT INTO diet(date,tot_protein,tot_carbohydrates,tot_fat,tot_calories) VALUES(
            ?,?,?,?,?);"""
        date=datetime.strptime(data['date'],'%Y-%m-%d').date()
        cursor.execute(diet_insertQ,(date,0,0,0,0))
        sql.commit()
        return 'success'
    diet_table_data=cursor.execute('SELECT * FROM diet').fetchall()
    g.home_data=dateFormatting(dict(diet_table_data,['date','tot_protein','tot_carbohydrates','tot_fat','tot_calories']))
    sql.close()
    return render_template('home.html')


@app.route('/view/',methods=["POST","GET"])
def view()->'html':
    sql=get_db()
    c=sql.cursor()
    if 'tdiet' in getTablesList():
        print('exception handled')
    else:
        table_query="""CREATE TABLE tdiet(
            date TIMESTAMP NOT NULL,
            fooditem TEXT NOT NULL,
            FOREIGN KEY(date)
            REFERENCES diet(date)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        ); """
        c.execute(table_query)
    try:
        session['get_date']=request.args.get('date',default=None,type=str)
        session["request_date"]=dateformat(session['get_date'])
        '''print(type(dateformat(request_date)))
         date_list=c.execute('SELECT date from diet WHERE date=?',(request_date,)).fetchall()
         if bool(date_list):'''
        print('iam here')
    except:
        print('exception overridded')
    
    if request.method=="POST":
            c.execute("INSERT INTO tdiet(date,fooditem) VALUES(?,?)",(session["request_date"],request.form['food']))
            sql.commit()
            dates=dict(c.execute("SELECT date FROM diet").fetchall(),['date'])
            for date in dates:
                getTotal(date['date'])
            diet_insertQ="""INSERT INTO diet(tot_protein,tot_carbohydrates,tot_fat,tot_calories) VALUES(
                ?,?,?,?) WHERE date=?;"""
            diet_insertQ="""UPDATE diet 
            SET tot_protein=?,tot_carbohydrates=?,tot_fat=?,tot_calories=? WHERE date=?;"""
            date=session["request_date"]
            c.execute(diet_insertQ,(session[str(date)]['protein'],session[str(date)]['carbohydrates'],session[str(date)]['fat'],session[str(date)]['calories'],date))
            sql.commit()
    diet_table_data=c.execute('SELECT tot_protein,tot_carbohydrates,tot_fat,tot_calories FROM diet WHERE date=?',(session["request_date"],)).fetchall()
    g.home_data=dict(diet_table_data,['tot_protein','tot_carbohydrates','tot_fat','tot_calories'])
    g.food_items=dict(c.execute('SELECT fooditem FROM tdiet WHERE date=?',(session["request_date"],)).fetchall(),['fooditem'])
    food_list=getFoodItems(g.food_items)
    g.food_items_data=getFoodListData(food_list)
    food_list_obj=c.execute('SELECT FOOD_NAME FROM FOODS_LIST')
    food_list=food_list_obj.fetchall()
    g.food_list=food_list
    sql.close()
    return render_template('view.html',list=bool(g.food_list))


@app.route('/add_food',methods=['POST','GET'])
@app.route('/add_food/data.json',methods=['POST'])
def add_food()->'html':
    sql=get_db()
    c=sql.cursor()
    if 'FOODS_LIST' in getTablesList():
                print('exception handled')

    else:
        create_table_queary="""CREATE TABLE FOODS_LIST
        (SNO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        FOOD_NAME TEXT VARCHAR(30) UNIQUE NOT NULL,
        PROTEIN INTEGER NOT NULL,
        CARBOHYDRATES INTEGER NOT NULL,
        FAT INTEGER NOT NULL,
        CALORIES INTEGER NOR NULL);"""
        c.execute(create_table_queary)

    if request.method=='POST':
        data=request.get_json()
        food_name=data['food']
        carbohydrates=data['carbohydrates']
        protein=data['proteins']
        fat=data['fats']
        calories=data['calories']
        try:
            c.execute("INSERT INTO FOODS_LIST(FOOD_NAME,PROTEIN,CARBOHYDRATES,FAT,CALORIES) \
            VALUES(?,?,?,?,?)",(food_name,protein,fat,carbohydrates,calories))
            sql.commit()
            sql.close()
            return 'success'
        except:
            return 'repeat'

        
    cursor=c.execute("SELECT SUM(PROTEIN),SUM(CARBOHYDRATES),SUM(FAT),SUM(CALORIES) FROM FOODS_LIST")
    food_total_columns=["PROTEIN","CARBOHYDRATES","FAT","CALORIES"]
    g.food_data_total=dict(cursor.fetchall(),food_total_columns)
    cursor=c.execute('SELECT * FROM FOODS_LIST')
    food_data=cursor.fetchall()
    food_list_columns=['SNO','FOOD_NAME','PROTEIN','CARBOHYDRATES','FAT','CALORIES']
    g.food_data=dict(food_data,food_list_columns)
    sql.close()
    return render_template('add_food.html')

