from pelisdb import PeliculasDB

db = PeliculasDB()

# para insertar pelicula:
# titulo
# caratula
# ubicacion

#pelicula = ('300','','carpeta 1')
#pelicula2 = ('willow','','carpeta 1')
#pelicula3 = ('casi 300','','carpeta 1')

#INSERTAR
#db.insertar_datos(pelicula)
#db.insertar_datos(pelicula2)
#db.insertar_datos(pelicula3)

#BUSCAR
#print(db.buscar_pelicula("300"))

#MODIFICAR
#db.editar_pelicula("titulo","Willow",2)

#BORRAR
#db.borrar_pelicula(1)

#IMPRIMIR ENTERA
#print (db)

ayuda="""
(I)nsertar Pelicula
(E)liminar Pelicula
(M)odificar Pelicula
(B)uscar Pelicula
(L)istar Peliculas
(Q)uit Salir
"""

def main():
    
    opcion = 'H'
    while opcion != 'Q':
        
        opcion = input("\nElige opcion o (H) para Ayuda: ").upper()
        
        if opcion == 'H':
            print(ayuda)
        
        elif opcion == 'Q':
            print("***  Saliendo del Sistema  ***\n")
        
        elif opcion == 'L':
            print("\n( Id, Pelicula, Caratula, Ubicacion )\n")
            print(db)
        
        elif opcion == 'I':
            print("***  Insertar Pelicula  ***\n")
            titulo=input("Titulo de la Pelicula: ")
            caratula=input("Ubicacion y nombre de la cartula: ")
            ubicacion=input("Ubicacion de la Pelicula: ")
            pelicula=(titulo,caratula,ubicacion)
            n = db.insertar_datos(pelicula)
            if n==0:
                print("Imposible Añadir Pelicula\n")
            else:
                print("Pelicula Añadida con exito!!!\n")
        
        elif opcion == 'B':
            print("***  Buscar Pelicula  ***\n")
            peli=input("Nombre de la Pelicula a Localizar: ")
            dato=db.buscar_pelicula(peli)
            for row in dato:
                print(str(row))
        
        elif opcion == 'M':
            print("***  Modificar Pelicula  ***\n")
            peli=int(input("Id de la Pelicula a Modificar: "))
            atributo_n=0
            while atributo_n != 't' and atributo_n != 'c' and atributo_n != 'u':
                atributo_n=input("que parametro vas a Modificar ( 't'titulo, 'c'caratula, 'u'ubicacion):")
                if atributo_n=='t':
                    atributo="titulo"
                elif atributo_n=='c':
                    atributo="caratula"
                elif atributo_n=='u':
                    atributo="ubicacion"
                else:
                    print("Parametro no valido elije otro!! ")
            valor=input("Nuevo Valor: ")
            n = db.editar_pelicula(atributo,valor,peli)
            if n==0:
                print("Imposible Modificar Pelicula comprobar Id\n")
            else:
                print("Pelicula Modificada con exito!!!\n")
                            

        elif opcion == 'E':
            print("***  Eliminar Pelicula  ***\n")
            peli=int(input("escribe id de la pelicula a eliminar: "))
            n = db.borrar_pelicula(peli)
            if n==0:
                print("Id no Existe\n")
            else:
                print("Pelicula Borrada con exito!!!\n")
        
        else:
            print("***Opcion no Soportada***\n")
    
    pass

if __name__ == "__main__":
    main()