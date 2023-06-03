import gi
from pelisdb import PeliculasDB
from VentanaMeta import win3
from VentanaEdicion import win4

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio

db = PeliculasDB()


class win2(Gtk.Window):
    
    def __init__(self, pelicula):
        super().__init__()
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(10)
        self.set_default_size(400, 200)
        self.pelicula=pelicula
                
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.pelicula[1]
        self.set_titlebar(hb)
        
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="search-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_start(button)
        button.connect("clicked", self.completar)
        
        button2 = Gtk.Button()
        icon2 = Gio.ThemedIcon(name="document-edit-symbolic")
        image2 = Gtk.Image.new_from_gicon(icon2, Gtk.IconSize.BUTTON)
        button2.add(image2)
        hb.pack_start(button2)
        button2.connect("clicked", self.editar)
        
        button3 = Gtk.Button()
        icon3 = Gio.ThemedIcon(name="edit-delete-symbolic")
        image3 = Gtk.Image.new_from_gicon(icon3, Gtk.IconSize.BUTTON)
        button3.add(image3)
        hb.pack_start(button3)
        button3.connect("clicked", self.borrar)
        
        box = Gtk.Box(spacing=10)
        self.add(box)
        
        if self.pelicula[3] == "":
            caratula="pelis/sin_caratula.jpg"
        else:
            caratula=self.pelicula[3]    
        
        image = Gtk.Image()
        image.set_from_file(caratula)
        box.add(image)

        vbox=Gtk.Box(spacing=10)
        vbox.set_orientation(Gtk.Orientation.VERTICAL)
        box.add(vbox)

        titulo_label = Gtk.Label()
        titulo_entry = Gtk.Label()
        anho_label = Gtk.Label()
        anho_entry = Gtk.Label()
        sitio_label = Gtk.Label()
        sitio_entry = Gtk.Label()

        titulo_label.set_label("Titulo:")
        titulo_label.set_xalign(0)
        anho_label.set_label("Año:")
        anho_label.set_xalign(0)
        sitio_label.set_label("Sitio:")
        sitio_label.set_xalign(0)

        titulo_entry.set_markup('<span size="x-large"><b>'+str(self.pelicula[1])+'</b></span>')
        anho_entry.set_markup('<span size="x-large"><b>'+str(self.pelicula[2])+'</b></span>')
        sitio_entry.set_markup('<span size="x-large"><b>'+str(self.pelicula[4])+'</b></span>')
        titulo_entry.set_xalign(0)
        anho_entry.set_xalign(0)
        sitio_entry.set_xalign(0)

        vbox.add(titulo_label)
        vbox.add(titulo_entry)
        vbox.add(anho_label)
        vbox.add(anho_entry)
        vbox.add(sitio_label)
        vbox.add(sitio_entry)

        self.show_all()

    def completar(self, button):
        window = win3(self.pelicula)
        self.destroy()
        
    def editar(self, widget):
        win4(self.pelicula, self.pelicula[4])
        self.destroy()
    
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
            self.destroy()
        elif response == Gtk.ResponseType.NO:
            print("Abortando borrado de la pelicula")

        dialog.destroy()

#if __name__=='__main__':
#    
#    busqueda = db.consulta_indibidual(82)
#    win = win2(busqueda)
#    win.connect("destroy", Gtk.main_quit)
#    Gtk.main()