from flask import Flask,render_template,request,redirect,url_for
import json
from urllib.request import urlopen

app = Flask(__name__,static_folder='')

provinciasurl = 'https://provinciasapi.herokuapp.com/provincia'
localidadesurl =' https://provinciasapi.herokuapp.com/localidades'

class mapas():
    def __init__(self,provinciasurl,localidadesurl):
        self.urlprovincias = provinciasurl
        self.urllocalidades = localidadesurl
        
    def get(self,url):
        with urlopen(url) as resource:
            return json.load(resource)

    def getmapaprovincias(self):
        self.lista = []
        for item in self.get(self.urlprovincias):
            self.lista.append([item['nombre'],item['centroide']['lat'],item['centroide']['lon'],item['id']])
        return self.lista

    def getmapalocalidades(self,id):
        self.lista = []
        for item in self.get(self.urllocalidades):
            if item['provincia_id'] == id: 
                self.lista.append([item['localidad_nombre'],float(item['localidad_centroide_lat']),float(item['localidad_centroide_lon']),item['provincia_id']])
        return self.lista

    def getlocalidad(self,nombre):
        self.lista = []
        for item in self.get(self.urllocalidades):
            if nombre.lower() in item['localidad_nombre'].lower():
                self.lista.append([item['localidad_nombre'],float(item['localidad_centroide_lat']),float(item['localidad_centroide_lon']),item['provincia_id']])
        return self.lista

@app.route("/provincias/<id>")
def get_mapalocalidades(id):
    a = h.getmapalocalidades(id)
    return render_template('mapamulti.html',a=a)


@app.route("/provincias")
def get_mapaprovincias():
    a = h.getmapaprovincias() 
    return render_template('mapamulti.html',a=a)    


@app.route('/',methods=['GET'])
def home():
    nombre = request.args.get("nombre", default=None, type=str)
    if nombre != None:
        a = h.getlocalidad(nombre)
        return render_template('mapamulti.html',a=a)
    else:
        return render_template('index.html')


h=mapas(provinciasurl,localidadesurl)
#app.run(host="localhost")
if __name__ == "__name__": app.run()
