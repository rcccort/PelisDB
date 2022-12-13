from pelisdb import PeliculasDB

db = PeliculasDB()

# para insertar pelicula:
# titulo
# caratula
# ubicacion

pelicula = ('300','','carpeta 1')
pelicula2 = ('willow','','carpeta 1')
pelicula3 = ('casi 300','','carpeta 1')

#INSERTAR
#db.insertar_datos(pelicula)
#db.insertar_datos(pelicula2)
#db.insertar_datos(pelicula3)

#BUSCAR
print(db.buscar_pelicula("300"))

#MODIFICAR
#db.editar_pelicula("titulo","Willow",2)

#BORRAR
#db.borrar_pelicula(1)

#IMPRIMIR ENTERA
#print (db)