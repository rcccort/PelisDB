#!/bin/python3
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
config_base = {'ultimo_lugar':'Carpeta 1', 'dir_caratulas':'pelis', 'tmdb_api_key':'', 'dark_theme': False}

cf = Comfiguracion(APP, config, config_base)

caratulas_dir = cf.get_dir() / cf.read_conf()['dir_caratulas']
if not caratulas_dir.exists():
    os.makedirs(caratulas_dir)
    copy('sin_caratula.jpg', caratulas_dir / 'sin_caratula.jpg')

db = PeliculasDB(cf.get_dir())

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
        
        # --- Botón para cambiar de tema (claro/oscuro) ---
        self.theme_button = Gtk.ToggleButton()
        self.theme_button.connect("toggled", self.on_theme_toggled)
        
        # Sincronizar el estado inicial del botón con la configuración de GTK
        settings = Gtk.Settings.get_default()
        is_dark_preferred = settings.get_property("gtk-application-prefer-dark-theme")
        self.theme_button.set_active(is_dark_preferred)
        self.actualizar_icono_tema(is_dark_preferred) # Poner el icono inicial correcto
        
        hb.pack_end(self.theme_button)
        # --- Fin del botón de tema ---
        
    def on_theme_toggled(self, button):
        # El estado del botón (activo/inactivo) determina si queremos el tema oscuro
        is_dark = button.get_active()
        
        # Aplicar la configuración a GTK
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", is_dark)
        
        # Guardar el estado en el fichero de configuración
        config_actual = cf.read_conf()
        config_actual['dark_theme'] = is_dark
        cf.escribir_datos(config_actual)
        
        # Actualizar el icono para que refleje el estado actual
        self.actualizar_icono_tema(is_dark)

    def actualizar_icono_tema(self, is_dark):
        if is_dark:
            # El tema es oscuro, el icono es una luna
            icon_name = "weather-clear-symbolic"
        else:
            # El tema es claro, el icono es un sol
            icon_name = "weather-clear-night-symbolic"
        image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        self.theme_button.set_image(image)

    def anadir_pelicula(self, widget):
        eleccion_anterior = cf.read_conf()['ultimo_lugar']
        ventana4=VentanaEdicion('',eleccion_anterior, cf)
        ventana4.connect("destroy", self.refrescar)
        #self.refrescar(widget)
                                                                       
    def pulsar_boton(self, widget):
        print("Boton "+widget.get_name()+" Pulsado")
        id = db.consulta_indibidual(int(widget.get_name()))
        print(id)
        ventana2=VentanaInfo(id, cf)
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
        
        # Vaciamos el flowbox antes de llenarlo de nuevo
        for child in box.get_children():
            box.remove(child)
            
        for peli in pelis:
            button = Gtk.Button()
            button.get_style_context().add_class("boton-imagen")
            button.set_name(str(peli[0]))
            if peli[3] != "":
                button.set_image(self.redimensionar_imagen(str(cf.get_dir() / peli[3])))
            else:
                button.set_image(self.redimensionar_imagen(str(cf.get_dir() / caratulas_dir /"sin_caratula.jpg")))
            button.connect("clicked", self.pulsar_boton)
            box.add(button)
    
#    def actulizar_metadatos(self, widget):
#        for peli in db.consulta_peliculas():
#            if peli[3] == '':
#                ventana_meta = VentanaMeta(peli, cf)
#                ventana_meta.connect("destroy", self.refrescar)
#        self.refrescar(widget)

    def actulizar_metadatos(self, widget):
        
        def crear_lista():
            for peli in db.consulta_peliculas():
                if peli[3] == '':
                    yield peli
        
        def abrir_ventana(pelicula):
            ventana_meta = VentanaMeta(pelicula, cf)
            ventana_meta.connect("destroy", siguiente)
                        
        def siguiente(widget):
            try:
                pelicula = next(peli)
                abrir_ventana(pelicula)
            except:
                self.refrescar(None)
            
        peli = crear_lista()
        siguiente(None)
        
        self.refrescar(widget)
    
    def refrescar(self, button):
        resultado=db.consulta_peliculas()
        self.crear_flowbox(self.flowbox, resultado)
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

    # --- Cargar y aplicar el tema guardado ANTES de crear la ventana ---
    config_actual = cf.read_conf()
    # Usamos .get() para seguridad, si el valor no existiera, usaría False
    tema_oscuro = config_actual.get('dark_theme', False)
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", tema_oscuro)
    # --- Fin de la carga del tema ---
    
    # --- CSS para los botones con imágenes ---
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(b"""
    .boton-imagen {
        background: none;
        border: none;
        padding: 0;
        border-radius: 0;
    }
    .boton-imagen:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }
    """)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    # --- Fin del CSS ---
    
    win = VentanaPrincipal()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
