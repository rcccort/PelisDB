#! /bin/python3
# -*- coding: utf-8 -*-

import gi
#from comfiguracion import Comfiguracion
from pelisdb import PeliculasDB
from tmdbv3api import TMDb, Movie
import requests
from PIL import Image

#APP = "pelisdb"
#config = f"{APP}.conf"
#config_base = {'ultimo_lugar':'Carpeta 1', 'dir_caratulas':'pelis', 'tmdb_api_key':''}

#cf = Comfiguracion(APP, config, config_base)

base=TMDb()
base.language = "es-ES"
base.debug = True

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio

class VentanaMeta(Gtk.Window):
    
    def __init__(self, pelicula, cf):
        super().__init__()
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(10)
        self.set_default_size(400, 500)
        self.pelicula=pelicula
        self.db = PeliculasDB(cf.get_dir())
        self.caratulas_dir = cf.read_conf()['dir_caratulas']
        self.cf = cf
        
        if cf.read_conf()['tmdb_api_key'] == '':
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Falta Clave para TMDB!!",
            )
            dialog.format_secondary_text(
                "edite archivo pelisdb.conf para añadirla"
            )
            dialog.run()

            dialog.destroy()
        else:
            base.api_key = cf.read_conf()['tmdb_api_key']
                
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.pelicula[1]
        self.set_titlebar(hb)
        
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="list-add-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_start(button)
        button.connect("clicked", self.Boton_Pulsado)
        
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.box = Gtk.Box(spacing=10)
        self.box.set_orientation(Gtk.Orientation.VERTICAL)
        
        self.add(self.scrolled)
        self.scrolled.add(self.box)
        self.radiobutton = Gtk.RadioButton()
        self.check =''
        self.elccion = []
        
        self.Buscar_Online(self.pelicula[1])
        
        self.show_all()
        
    def Buscar_Online(self,titulo):
        
        movie = Movie()
        busqueda = movie.search(titulo)

        if len(busqueda) == 1:
            self.crear_lista(busqueda)
            self.check='0'
            self.Boton_Pulsado(None)
        
        elif len(busqueda) == 0:
            print('No Encontró nada')
            self.mesaje_error()
            self.destroy()
            
        else:
            self.crear_lista(busqueda)
            #elec=0
            #for peli in busqueda:
            #    anho = peli.release_date[:4]
            #    try:
            #        caratula_link = 'https://image.tmdb.org/t/p/w200'+peli.poster_path
            #    except:
            #        caratula_link = "pelis/sin_caratula.jpg"
            #    #print(str(elec))
            #    #print(peli.title+" "+anho)
            #    #print(peli.overview)
            #    #print(caratula_link+"\n")
            #    pelicula=(elec, peli.title, anho, caratula_link)
            #    self.elccion.append(pelicula)
            #    elec=elec+1
            #    self.Caja_Peli(pelicula)
    
    def mesaje_error(self):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="No Hay Coincidencias!!",
        )
        dialog.format_secondary_text(
            "Pruebe a cambiar el titulo de la pelicula"
        )
        dialog.run()

        dialog.destroy()
    
    def crear_lista(self, busqueda):
        elec=0
        for peli in busqueda:
            
            if elec == 5:
                break
            
            try:
                anho = peli.release_date[:4]
            except:
                anho = ""
            
            try:
                caratula_link = 'https://image.tmdb.org/t/p/w200'+peli.poster_path
            except:
                caratula_link = str(self.caratulas_dir)+"/sin_caratula.jpg"
            
            pelicula=(elec, peli.title, anho, caratula_link)
            self.elccion.append(pelicula)
            elec=elec+1
            
            if len(busqueda) > 1:
                self.Caja_Peli(pelicula)
    
    def Caja_Peli(self, Peli):
        #print(Peli)
        hbox = Gtk.Box(spacing=10)
        hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        
        link=Peli[3]
        
        image = Gtk.Image()
        if link != str(self.caratulas_dir)+"/sin_caratula.jpg":
            response = requests.get(Peli[3], stream=True)
            response.raw.decode_content = True
            photo = Image.open(response.raw)
            link2 = '/tmp/'+str(Peli[0])+link[-4:]
            photo.save(link2)
            image.set_from_file(link2)
        else:
            image.set_from_file(str(self.cf.get_dir() / link))
        
        label = Gtk.Label()
        label.set_markup('<span size="x-large"><b>'+Peli[1]+'\n'+Peli[2]+'</b></span>')
        
        radiobutton = Gtk.RadioButton(group=self.radiobutton)
        radiobutton.connect("toggled", self.Elegir_opcion)
        radiobutton.set_name(str(Peli[0]))
        
        hbox.add(radiobutton)
        hbox.add(image)
        hbox.add(label)
        self.box.add(hbox)
    
    def Elegir_opcion(self, radiobutton):
        
        if radiobutton.get_active():
            self.check = radiobutton.get_name()
    
    def Guardar_Imagen(self, link, imagen, check):
    
        if link != str(self.caratulas_dir)+"/sin_caratula.jpg":
            #print(self.elccion[int(check)])
            #print("Guardando "+link+" en "+imagen+"\n")
            response = requests.get(link, stream=True)
            response.raw.decode_content = True
            photo = Image.open(response.raw)
            #photo.save(str(self.cf.get_dir())+'/pelis/'+imagen)
            photo.save(str(self.cf.get_dir())+'/'+self.cf.read_conf()['dir_caratulas']+'/'+imagen)
    
    def Boton_Pulsado(self, event):
        if self.check != '':    
            #self.Completar_Datos(self.normalize(self.elccion[int(self.check)][1]),
            #                     self.elccion[int(self.check)][2],
            #                     "pelis/"+str(self.pelicula[0])+self.elccion[int(self.check)][3][-4:],
            #                     self.pelicula[0])
            self.Completar_Datos(self.normalize(self.elccion[int(self.check)][1]),
                                 self.elccion[int(self.check)][2],
                                 self.cf.read_conf()['dir_caratulas']+"/"+str(self.pelicula[0])+self.elccion[int(self.check)][3][-4:],
                                 self.pelicula[0])
            self.Guardar_Imagen(self.elccion[int(self.check)][3],
                                str(self.pelicula[0])+self.elccion[int(self.check)][3][-4:],
                                self.check)
            self.destroy()
                    
    def Completar_Datos(self, titulo, anho, caratula, id):
        
        if id != "" and anho != "" and caratula != "" and titulo != "":    
            #print(str(id), titulo, anho, caratula)
            self.db.editar_pelicula("anho", anho, id)
            if caratula != str(self.caratulas_dir)+"/sin_caratula.jpg":
                #print("Esto tambien funciona")
                self.db.editar_pelicula("caratula", caratula, id)
            self.db.editar_pelicula("titulo", titulo, id)
    
    def normalize(self, s):
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
        
#if __name__=='__main__':
#    #busqueda = (7, 'Doble Filo', '', '', 'Carpeta 1')
#    busqueda = self.db.consulta_indibidual(71)
#    win = win3(busqueda)
#    win.connect("destroy", Gtk.main_quit)
#    win.show_all()
#    Gtk.main()