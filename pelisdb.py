#! /bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from pathlib import Path

class PeliculasDB:
    
    def __init__(self, directorio: Path) -> None:
        ''' Conecta con la base de datos o la crea si existe en el directorio dado'''
        self.cnn = sqlite3.connect(Path(directorio) / 'pelisdb.db') # nombre del archivo
        self.cur = self.cnn.cursor()
        # crea la tabla y los diferentes campos
        self.cur.execute("""CREATE TABLE IF NOT EXISTS peliculas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            anho TEXT,
            caratula TEXT,
            ubicacion TEXT
            )""")
        self.cur.close()
        
    def __str__(self) -> str:
        ''' formatea salida de la clase para devolver un string'''
        datos = self.consulta_peliculas()
        aux = '' # variable donde guarda el string para devolver
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux
    
    def consulta_peliculas(self):
        ''' hace una consulta de todo lo que hay en la tabla - películas y lo devuelve'''
        cur = self.cnn.cursor() # inicializa cursor
        cur.execute("SELECT * FROM peliculas") # ejecuta orden SQL
        datos = cur.fetchall() # guarda en datos lo que devuelve el cursor
        cur.close() # cierra cursor
        return datos # devuelve datos
    
    def insertar_datos(self, pelicula: tuple) -> int:
        ''' gravar datos en la tabla películas, como mínimo poner titulo y ubicación\n
        devuelve 1 si completa grabación'''
        cur = self.cnn.cursor()
        cur.execute("""INSERT OR IGNORE INTO peliculas VALUES(NULL,?,?,?,?)""",pelicula)
        n = cur.rowcount
        self.cnn.commit() # confirmar el INSERT para gravar
        cur.close()
        return n # devuelve 1 o 0 si a podido o no gravar
    
    def buscar_pelicula(self, titulo: str) -> list:
        ''' busca un titulo y devuelve todas las coincidencias'''
        cur=self.cnn.cursor()
        cur.execute("SELECT * FROM peliculas WHERE titulo LIKE '%{}%'".format(titulo))
        dato = cur.fetchall()
        cur.close()
        return dato
    
    def editar_pelicula(self, atributo: str, valor: str, id: int) -> int:
        ''' editar datos en la tabla películas, necesita el atributo a cambiar y el nuevo valor\n
        devuelve 1 si completa grabación'''
        cur=self.cnn.cursor()
        cur.execute("UPDATE peliculas SET {} = '{}' WHERE id = '{}'".format(atributo,valor,id))
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
    
    def borrar_pelicula(self,id: int) -> int:
        ''' borrar la entrada identificada por id de la tabla peliculas\n
        devuelve 1 si completa grabación'''
        cur=self.cnn.cursor()
        cur.execute("DELETE FROM peliculas WHERE id = '{}'".format(id))
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
    
    def consulta_indibidual(self,id: int) -> tuple:
        ''' devuelve una tuple con los datos almacenados con esa id'''
        cur=self.cnn.cursor()
        cur.execute("SELECT * FROM peliculas WHERE id = '{}'".format(id))
        dato = cur.fetchone()
        cur.close()
        return dato
