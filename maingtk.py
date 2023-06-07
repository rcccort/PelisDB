#! /bin/python3
# -*- coding: utf-8 -*-

from pelisdb import PeliculasDB
from ventana_info import VentanaInfo
from ventana_meta import VentanaMeta
from ventana_edicion import VentanaEdicion
from comfiguracion import Comfiguracion
from shutil import copy
import gi
import os

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf

APP = "pelisdb"
config = f"{APP}.conf"
config_base = {'ultimo_lugar':'Carpeta 1', 'dir_caratulas':'pelis', 'tmdb_api_key':''}

cf = Comfiguracion(APP, config, config_base)

caratulas_dir = cf.get_dir() / cf.read_conf()['dir_caratulas']
if not caratulas_dir.exists():
    os.makedirs(caratulas_dir)
    copy('sin_caratula.jpg', caratulas_dir / 'sin_caratula.jpg')

db = PeliculasDB(cf.get_dir())

#base = cf.read_conf()
#base['opcion3'] = 'Opcion 3'
#cf.escribir_datos(base)

class VentanaPrincipal(Gtk.Window):
    
    def __init__(self):
        super().__init__()
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(10)
        self.set_default_size(1000, 500)
        
        pelis = db.consulta_peliculas()
        
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Pelis"
        self.set_titlebar(hb)
        
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="system-restart-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_start(button)
        button.connect("clicked", self.actulizar_metadatos)
        
        busqueda = Gtk.SearchEntry()
        busqueda.set_text("Titulo")
        busqueda.connect("event", self.borrar_entry)
        busqueda.connect("activate", self.buscar_pelicula)
        hb.add(busqueda)
        
        button = Gtk.Button()
        #icon = Gio.ThemedIcon(name="system-shutdown-symbolic")
        icon = Gio.ThemedIcon(name="list-add-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_start(button)
        button.connect("clicked", self.anadir_pelicula)
        
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(10)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.crear_flowbox(self.flowbox, pelis)

        self.scrolled.add(self.flowbox)

        self.add(self.scrolled)
        
    def anadir_pelicula(self, widget):
        eleccion_anterior = cf.read_conf()['ultimo_lugar']
        ventana4=VentanaEdicion('',eleccion_anterior)
        ventana4.connect("destroy", self.refrescar)
        #self.refrescar(widget)
                                                                       
    def pulsar_boton(self, widget):
        print("Boton "+widget.get_name()+" Pulsado")
        id = db.consulta_indibidual(int(widget.get_name()))
        print(id)
        ventana2=VentanaInfo(id)
        ventana2.connect("destroy", self.refrescar)
        self.refrescar(widget)
        #ventana2.show_all()
            
    def borrar_entry(self, busqueda, event):
        if event.type == Gdk.EventType.FOCUS_CHANGE:
            if busqueda.get_text() == "Titulo":
                busqueda.set_text("")
            elif busqueda.get_text() == "":
                busqueda.set_text("Titulo")

    def buscar_pelicula(self, widget):
        busqueda = widget.get_text()
        if busqueda != "":
            resultado=db.buscar_pelicula(busqueda)
            self.scrolled.remove(self.flowbox)
            self.crear_flowbox(self.flowbox, resultado)
            self.scrolled.add(self.flowbox)
            self.scrolled.show_all()
        elif busqueda == "":
            resultado=db.consulta_peliculas()
            self.scrolled.remove(self.flowbox)
            self.crear_flowbox(self.flowbox, resultado)
            self.scrolled.add(self.flowbox)
            self.scrolled.show_all()
                        
    def redimensionar_imagen(self, imagen):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=imagen, 
            width=200, 
            height=200, 
            preserve_aspect_ratio=True)

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        return image
            
    def crear_flowbox(self, box, pelis):
                        
        box.destroy()
        for peli in pelis:
            button = Gtk.Button()
            button.set_name(str(peli[0]))
            if peli[3] != "":
                button.set_image(self.redimensionar_imagen(str(cf.get_dir() / peli[3])))
            else:
                button.set_image(self.redimensionar_imagen(str(cf.get_dir() / "pelis/sin_caratula.jpg")))
            button.connect("clicked", self.pulsar_boton)
            box.add(button)
    
    def actulizar_metadatos(self, widget):
        for peli in db.consulta_peliculas():
            if peli[3] == '':
                ventana_meta = VentanaMeta(peli)
                ventana_meta.connect("destroy", self.refrescar)
        self.refrescar(widget)
    
    def refrescar(self, button):
        resultado=db.consulta_peliculas()
        self.scrolled.remove(self.flowbox)
        self.crear_flowbox(self.flowbox, resultado)
        self.scrolled.add(self.flowbox)
        self.scrolled.show_all()

#class win2(Gtk.Window):
#    
#    def __init__(self, pelicula):
#        super().__init__()
#        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
#        self.set_border_width(10)
#        self.set_default_size(400, 200)
#                
#        hb = Gtk.HeaderBar()
#        hb.set_show_close_button(True)
#        hb.props.title = pelicula[1]
#        self.set_titlebar(hb)
#        
#        box = Gtk.Box(spacing=10)
#        self.add(box)
#        
#        image = Gtk.Image()
#        image.set_from_file(pelicula[3])
#        box.add(image)
#        
#        label = Gtk.Label()
#        label.set_label("Titulo:\n"+pelicula[1]+"\n"+"Año:\n"+pelicula[2]+"\n"+"Sitio:\n"+pelicula[4])
#        box.add(label)
        
if __name__=='__main__':
    
    win = VentanaPrincipal()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()