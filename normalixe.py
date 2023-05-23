from pelisdb import PeliculasDB

db = PeliculasDB()

def Completar_Datos(titulo, id):
    db.editar_pelicula("titulo", titulo, id)
    
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

datos = db.consulta_peliculas()

for dato in datos:
    #print(dato[1])
    titulo=normalize(dato[1])
    #print(titulo)
    db.editar_pelicula("titulo", titulo, dato[0])