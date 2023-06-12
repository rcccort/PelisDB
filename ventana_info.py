#! /bin/python3
# -*- coding: utf-8 -*-

import gi
from comfiguracion import Comfiguracion
from pelisdb import PeliculasDB
from ventana_meta import VentanaMeta
from ventana_edicion import VentanaEdicion

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio

#APP = "pelisdb"
#config = f"{APP}.conf"
#config_base = {'ultimo_lugar':'Carpeta 1', 'dir_caratulas':'pelis', 'tmdb_api_key':''}

#cf = Comfiguracion(APP, config, config_base)

class VentanaInfo(Gtk.Window):
    
    def __init__(self, pelicula, cf):
        super().__init__()
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(10)
        self.set_default_size(400, 200)
        self.pelicula=pelicula
        self.db = PeliculasDB(cf.get_dir())
        self.cf = cf
                
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = self.pelicula[1]
        self.set_titlebar(self.hb)
        
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="search-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        self.hb.pack_start(button)
        button.connect("clicked", self.completar)
        
        button2 = Gtk.Button()
        icon2 = Gio.ThemedIcon(name="document-edit-symbolic")
        image2 = Gtk.Image.new_from_gicon(icon2, Gtk.IconSize.BUTTON)
        button2.add(image2)
        self.hb.pack_start(button2)
        button2.connect("clicked", self.editar)
        
        button3 = Gtk.Button()
        icon3 = Gio.ThemedIcon(name="edit-delete-symbolic")
        image3 = Gtk.Image.new_from_gicon(icon3, Gtk.IconSize.BUTTON)
        button3.add(image3)
        self.hb.pack_start(button3)
        button3.connect("clicked", self.borrar)
        
        box = Gtk.Box(spacing=10)
        self.add(box)
        
        if self.pelicula[3] == "":
            caratula=str(cf.get_dir() / cf.read_conf()['dir_caratulas'] / "sin_caratula.jpg")
        else:
            caratula=str(cf.get_dir() / self.pelicula[3])    
        
        image = Gtk.Image()
        image.set_from_file(caratula)
        box.add(image)

        vbox=Gtk.Box(spacing=10)
        vbox.set_orientation(Gtk.Orientation.VERTICAL)
        box.add(vbox)

        titulo_label = Gtk.Label()
        self.titulo_entry = Gtk.Label()
        anho_label = Gtk.Label()
        self.anho_entry = Gtk.Label()
        sitio_label = Gtk.Label()
        self.sitio_entry = Gtk.Label()

        titulo_label.set_label("Titulo:")
        titulo_label.set_xalign(0)
        anho_label.set_label("Año:")
        anho_label.set_xalign(0)
        sitio_label.set_label("Sitio:")
        sitio_label.set_xalign(0)

        self.titulo_entry.set_markup('<span size="x-large"><b>'+str(self.pelicula[1])+'</b></span>')
        self.anho_entry.set_markup('<span size="x-large"><b>'+str(self.pelicula[2])+'</b></span>')
        self.sitio_entry.set_markup('<span size="x-large"><b>'+str(self.pelicula[4])+'</b></span>')
        self.titulo_entry.set_xalign(0)
        self.anho_entry.set_xalign(0)
        self.sitio_entry.set_xalign(0)

        vbox.add(titulo_label)
        vbox.add(self.titulo_entry)
        vbox.add(anho_label)
        vbox.add(self.anho_entry)
        vbox.add(sitio_label)
        vbox.add(self.sitio_entry)

        self.show_all()
        
    def destruir(self, widget):
        self.destroy()

    def refrescar(self, widget):
        pelicula = self.db.consulta_indibidual(self.pelicula[0])
        self.hb.props.title = pelicula[1]
        self.titulo_entry.set_markup('<span size="x-large"><b>'+str(pelicula[1])+'</b></span>')
        self.anho_entry.set_markup('<span size="x-large"><b>'+str(pelicula[2])+'</b></span>')
        self.sitio_entry.set_markup('<span size="x-large"><b>'+str(pelicula[4])+'</b></span>')
        self.pelicula = pelicula

    def completar(self, button):
        window = VentanaMeta(self.pelicula, self.cf)
        window.connect("destroy", self.destruir)
        
    def editar(self, widget):
        window = VentanaEdicion(self.pelicula, self.pelicula[4], self.cf)
        window.connect('destroy', self.refrescar)
    
    def borrar(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Esta a punto de BORRAR un registro!!",
        )
        dialog.format_secondary_text(
            "Esta seguro?"
        )
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            print("Procediendo al borrado de la pelicula")
            self.db.borrar_pelicula(self.pelicula[0])
            self.destroy()
        elif response == Gtk.ResponseType.NO:
            print("Abortando borrado de la pelicula")

        dialog.destroy()

#if __name__=='__main__':
#    
#    busqueda = self.db.consulta_indibidual(82)
#    win = win2(busqueda)
#    win.connect("destroy", Gtk.main_quit)
#    Gtk.main()