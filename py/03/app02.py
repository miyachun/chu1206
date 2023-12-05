#https://tdx.transportdata.tw/

#https://docs.python.org/zh-tw/3/library/xml.etree.elementtree.html


#https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeByFrequency/Streaming/City/Hsinchu?%24top=30&%24format=XML
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests
from flask import Flask, render_template, request
app = Flask(__name__)


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
    
    if request.method == 'POST':
        
        dropdownval = request.form.get('Gcity')
        bb.append(dropdownval)
 
        
        for No in root.iter('{https://ptx.transportdata.tw/standard/schema/}BusA1Data'):
            ansA.append(No[0].text)


        for key, value in getAll.items():
            for i in value:
                if i == dropdownval:
                    print(value.index(i))

                    Lon.append(getAll['PositionLon'][value.index(i)])
                    Lat.append(getAll['PositionLat'][value.index(i)])
                    print(Lon,Lat)
                    
  

        render_template('example.html',bb=bb,Bus=Bus,Lon=Lon,Lat=Lat)

    for No in root.iter('{https://ptx.transportdata.tw/standard/schema/}BusA1Data'):    
        getAll['PlateNumb'].append(No[0].text)
        Bus.append(No[0].text) 
    for No in root.iter('{https://ptx.transportdata.tw/standard/schema/}BusPosition'):    
        getAll['PositionLon'].append(No[0].text)
    for No in root.iter('{https://ptx.transportdata.tw/standard/schema/}BusPosition'):    
        getAll['PositionLat'].append(No[1].text)
        
    return render_template('example.html',aa='0', Lon=Lon,Lat=Lat,getAll=getAll,Bus=Bus,bb=bb)



if __name__ == '__main__':
    app.run()