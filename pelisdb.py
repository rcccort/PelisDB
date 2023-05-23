import sqlite3

class PeliculasDB:
    
    def __init__(self):
        self.cnn = sqlite3.connect('pelisdb.db')
        self.cur = self.cnn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS peliculas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            anho TEXT,
            caratula TEXT,
            ubicacion TEXT
            )""")
        self.cur.close()
        
    def __str__(self):
        datos = self.consulta_peliculas()
        aux = ''
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux
    
    def consulta_peliculas(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM peliculas")
        datos = cur.fetchall()
        cur.close()    
        return datos
    
    def insertar_datos(self,pelicula):
        cur = self.cnn.cursor()
        cur.execute("""INSERT OR IGNORE INTO peliculas VALUES(NULL,?,?,?,?)""",pelicula)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
    
    def buscar_pelicula(self,titulo):
        cur=self.cnn.cursor()
        cur.execute("SELECT * FROM peliculas WHERE titulo LIKE '%{}%'".format(titulo))
        dato = cur.fetchall()
        cur.close()
        #Depurar impresion
        #aux = ''
        #for row in dato:
        #    aux = aux + str(row) + "\n"
        #return aux
        return dato
    
    def editar_pelicula(self,atrivuto,valor,id):
        cur=self.cnn.cursor()
        cur.execute("UPDATE peliculas SET {} = '{}' WHERE id = '{}'".format(atrivuto,valor,id))
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
    
    def borrar_pelicula(self,id):
        cur=self.cnn.cursor()
        cur.execute("DELETE FROM peliculas WHERE id = '{}'".format(id))
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
    
    def consulta_indibidual(self,id):
        cur=self.cnn.cursor()
        cur.execute("SELECT * FROM peliculas WHERE id = '{}'".format(id))
        dato = cur.fetchone()
        cur.close()
        return dato