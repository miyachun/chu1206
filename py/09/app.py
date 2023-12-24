from flask import Flask, render_template,request, url_for, flash, redirect, abort
import json,urllib.request
from itertools import zip_longest
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sqlite3
import datetime
from werkzeug.utils import secure_filename
import pandas as pd





app = Flask(__name__, static_url_path='/static')

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
upload_folder = os.path.join('static', 'uploads') 
app.config['UPLOAD'] = upload_folder
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

Mnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=(api_key)&format=JSON'
df = pd.read_csv('static/people108.csv')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
upload_folder = os.path.join('static', 'uploads') 
app.config['UPLOAD'] = upload_folder
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

Mnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tree = ET.parse('bus02.xml')
root = tree.getroot()




getAll={"PlateNumb":[],"PositionLon":[],"PositionLat":[]}
PlateNumb = {"PlateNumb":[]}
PositionLon={"PositionLon":[]}
PositionLat={"PositionLat":[]}

Bus=[]
ansA=[]
bb=[]
Lon=[]
Lat=[]


@app.route('/', methods=('GET', 'POST'))
def index():
    ansA=[]
    ansAll = {}
    Anscity = []
    Answx = []
    AnsmintT=[]
    AnsmaxtT = []
    ansCity=[]

    
    if request.method == 'POST':
        dropdownval = request.form.get('Gcity')
        data = urllib.request.urlopen(url).read()
        output = json.loads(data)
        location=output['records']['location']
        for i in location:
            city = i['locationName']
            if city==dropdownval:
                wx = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
                maxtT = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
                mintT = i['weatherElement'][2]['time'][0]['parameter']['parameterName']                
                ansA.append(city)
                ansA.append(wx)
                ansA.append(mintT)
                ansA.append(maxtT)
       
    data = urllib.request.urlopen(url).read()
    output = json.loads(data)
    location=output['records']['location']
        
    for i in location:
        city0 = i['locationName'] 
        wx0 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
        maxtT0 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
        mintT0 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
        Anscity.append(city0)
        Answx.append(wx0)
        AnsmaxtT.append(maxtT0)
        AnsmintT.append(mintT0)
        ansCity.append(city0)
    
    for elem1, elem2, elem3, elem4  in zip_longest(Anscity, Answx, AnsmintT, AnsmaxtT):
        ansAll.setdefault(elem1, []).append(elem2)
        ansAll.setdefault(elem1, []).append(elem3)
        ansAll.setdefault(elem1, []).append(elem4)  
   
    return render_template('index.html',ansAll=ansAll,ansA=ansA,ansCity=ansCity)

@app.route('/car', methods=('GET', 'POST'))
def car():
    
    if request.method == 'POST':
        
        dropdownval = request.form.get('Gcity')
        bb.append(dropdownval)
 

        #print(getAll['PlateNumb'])

        
        for No in root.iter('{https://ptx.transportdata.tw/standard/schema/}BusA1Data'):
            ansA.append(No[0].text)




        for key, value in getAll.items():
            for i in value:
                if i == dropdownval:
                    print(value.index(i))

                    Lon.append(getAll['PositionLon'][value.index(i)])
                    Lat.append(getAll['PositionLat'][value.index(i)])
                    print(Lon,Lat)
                    
                 


        #for i in getAll['PlateNumb']:
        #    if i==dropdownval:
        #        print(getAll['PositionLon'][i]) 
                 
            #if No.text==dropdownval:
            #    ansA.append(No[0].text)


  

        render_template('car.html',bb=bb,Bus=Bus,Lon=Lon,Lat=Lat)

    for No in root.iter('{https://ptx.transportdata.tw/standard/schema/}BusA1Data'):    
        getAll['PlateNumb'].append(No[0].text)
        Bus.append(No[0].text) 
    for No in root.iter('{https://ptx.transportdata.tw/standard/schema/}BusPosition'):    
        getAll['PositionLon'].append(No[0].text)
    for No in root.iter('{https://ptx.transportdata.tw/standard/schema/}BusPosition'):    
        getAll['PositionLat'].append(No[1].text)
        
    return render_template('car.html',aa='0', Lon=Lon,Lat=Lat,getAll=getAll,Bus=Bus,bb=bb)


@app.route('/dblist', methods=('GET', 'POST'))
def dblist():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM COMPANY ORDER BY time DESC').fetchall()
    conn.close()
    return render_template('db.html', posts=posts)

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM COMPANY WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/dbcreate', methods=('GET', 'POST'))
def dbcreate():
    
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        price = request.form['price']   
        image = request.files['image']
        filename = secure_filename(image.filename) 

        if not id:
            flash('id無填')
        elif not name :
            flash('name無填')
        elif not price :
            flash('price無填')
        elif not filename:
            nopic='no.jpg'
            conn = get_db_connection()
            conn.execute('INSERT INTO COMPANY (id, name, price, image, time ) VALUES (?, ?, ?, ?, ?)',
                         (id, name, price, nopic, Mnow ))
            conn.commit()
            conn.close()
            return redirect(url_for('dblist'))
        else:
            image.save(os.path.join(app.config['UPLOAD'], filename))
            conn = get_db_connection()
            conn.execute('INSERT INTO COMPANY (id, name, price, image, time ) VALUES (?, ?, ?, ?, ?)',
                         (id, name, price, filename, Mnow ))
            conn.commit()
            conn.close()
            return redirect(url_for('dblist'))

    return render_template('create.html')





@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    
    post = get_post(id)

    if request.method == 'POST':        
        name = request.form['name']
        price = request.form['price']        
        image = request.files['image']
        filename = secure_filename(image.filename)
        
        print(filename)
        if not filename:
            conn = get_db_connection()
            conn.execute('UPDATE COMPANY SET name = ?, price = ?'
                         ' WHERE id = ?',
                         ( name, price, id))

            conn.commit()
            conn.close()
            return redirect(url_for('dblist'))
        
        else:
            image.save(os.path.join(app.config['UPLOAD'], filename))
            conn = get_db_connection()
            conn.execute('UPDATE COMPANY SET name = ?, price = ?, image = ?'
                         ' WHERE id = ?',
                         ( name, price, filename, id))

            conn.commit()
            conn.close()
            return redirect(url_for('dblist'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM COMPANY WHERE id = ?', (id,))
    conn.commit()
    conn.close()    
    return redirect(url_for('dblist'))

@app.route('/echarts01')
def echarts01():
    data=[{ 'name': '10801','value': 138881  },
        { 'name': '10802','value': 137512  },
        { 'name': '10803','value': 101301  },
        { 'name': '10804','value': 186020  },
        { 'name': '10805','value': 160695  },
        { 'name': '10806','value': 169084  },
        { 'name': '10807','value': 144669  },
        { 'name': '10808','value': 135557  },
        { 'name': '10809','value': 127176  },
        { 'name': '10810','value': 180991  },
        { 'name': '10811','value': 180144  },
        { 'name': '10812','value': 147301  }]
    return render_template("echarts01.html", data=data)

@app.route('/echarts02')
def echarts02():
    Nlist=df.iloc[:,2].tolist()
    Alist=df.iloc[:,3] .tolist()
    Blist=df.iloc[:,4] .tolist()
    Clist=df.iloc[:,5] .tolist()
    Dlist=df.iloc[:,6] .tolist()
    Elist=df.iloc[:,7] .tolist()
    Flist=df.iloc[:,8] .tolist()
    Glist=df.iloc[:,9] .tolist()
    Hlist=df.iloc[:,10] .tolist()
    return render_template("echarts02.html", xdata=Nlist,ydata01=Alist,ydata02=Blist,ydata03=Clist,ydata04=Dlist,ydata05=Elist)
 
@app.route('/echarts03')
def echarts03(): 
    Nlist=df.iloc[:,2].tolist()
    Alist=df.iloc[:,3] .tolist()
    Blist=df.iloc[:,4] .tolist()
    Clist=df.iloc[:,5] .tolist()
    Dlist=df.iloc[:,6] .tolist()
    Elist=df.iloc[:,7] .tolist()
    Flist=df.iloc[:,8] .tolist()
    Glist=df.iloc[:,9] .tolist()
    Hlist=df.iloc[:,10] .tolist()

    return render_template("echarts03.html", xdata=Nlist,ydata01=Alist,ydata02=Blist,ydata03=Clist,ydata04=Dlist,ydata05=Elist,ydata06=Flist,ydata07=Glist,ydata08=Hlist)
 
@app.route('/echarts04')
def echarts04(): 
    Nlist=df.iloc[:,2].tolist()
    Alist=df.iloc[:,3] .tolist()
    Blist=df.iloc[:,4] .tolist()
    Clist=df.iloc[:,5] .tolist()
    Dlist=df.iloc[:,6] .tolist()
    Elist=df.iloc[:,7] .tolist()
    Flist=df.iloc[:,8] .tolist()
    Glist=df.iloc[:,9] .tolist()
    Hlist=df.iloc[:,10] .tolist()

    return render_template("echarts04.html", xdata=Nlist,ydata01=Alist,ydata02=Blist,ydata03=Clist,ydata04=Dlist,ydata05=Elist,ydata06=Flist,ydata07=Glist,ydata08=Hlist)
  

if __name__ == '__main__':
    app.run()
