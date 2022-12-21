from tmdbv3api import TMDb, Movie

# https://github.com/AnthonyBloomer/tmdbv3api
# para la api_key visita https://www.themoviedb.org/settings/api

base=TMDb()
base.language = "es-ES"
base.debug = True

movie = Movie()

busqueda = movie.search('una noche en la opera')

for peli in busqueda:
    anho = peli.release_date[:4]
    try:
        caratula_link = 'https://image.tmdb.org/t/p/w200'+peli.poster_path
    except:
        caratula_link = "sin caratula"
    print(peli.title+" "+anho)
    print(peli.overview)
    print(caratula_link)        

#peli = busqueda[1]
#anho = peli.release_date[:4]
#
#print(peli.title+" "+anho)
#print(peli.overview)
#print('https://image.tmdb.org/t/p/original'+peli.poster_path)
#print (res.title+" "+res.release_date+" "+str(res.id))
