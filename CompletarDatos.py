from pelisdb import PeliculasDB
from tmdbv3api import TMDb, Movie
import requests
from PIL import Image

db = PeliculasDB()
base=TMDb()
base.language = "es-ES"
base.debug = True


def Buscar_Online(id, titulo):
    
    print("buscando "+titulo+" ...")
    movie = Movie()
    busqueda = movie.search(titulo)
    elec=0
    for peli in busqueda:
        anho = peli.release_date[:4]
        try:
            caratula_link = 'https://image.tmdb.org/t/p/w200'+peli.poster_path
        except:
            caratula_link = "sin caratula"
        print(str(elec))
        print(peli.title+" "+anho)
        #print(peli.overview)
        print(caratula_link)
        elec=elec+1
    opcion = "V"
    while opcion != 'G':
        opcion = input("Elige V o G para ver o guardar: ").upper()
        eleccion = int(input("elije pelicula : "))
        if opcion == 'G':
            Guardar_Imagen("https://image.tmdb.org/t/p/w200"+busqueda[eleccion].poster_path, str(id) + busqueda[eleccion].poster_path[-4:])
            Completar_Datos(str(busqueda[eleccion].release_date[:4]), 'pelis/'+str(id) + busqueda[eleccion].poster_path[-4:],id)
        elif opcion == 'V':
            Ver_Imagen("https://image.tmdb.org/t/p/w200"+busqueda[eleccion].poster_path)
        else:
            print("Opcion no valida!!")

def Guardar_Imagen(link, imagen):
    
    print("Guardando "+link+" en "+imagen)
    response = requests.get(link, stream=True)
    response.raw.decode_content = True
    photo = Image.open(response.raw)
    photo.save('pelis/'+imagen)

def Ver_Imagen(url):

    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    photo = Image.open(response.raw)
    photo.show()

def Completar_Datos(anho, caratula, id):
    
    db.editar_pelicula("anho", anho, id)
    db.editar_pelicula("caratula", caratula, id)


datos = db.consulta_peliculas()

for dato in datos:
    if dato[3] == '':
        print(str(dato[0])+' '+dato[1])
        Buscar_Online(dato[0], dato[1])