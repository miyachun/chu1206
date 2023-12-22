from flask import Flask, render_template,request
import json,urllib.request
from itertools import zip_longest
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

app = Flask(__name__, static_url_path='/static')

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=(api_key)&format=JSON'

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


if __name__ == '__main__':
    app.run()
