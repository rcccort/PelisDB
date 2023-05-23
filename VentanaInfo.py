import gi

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio

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
        button.connect("clicked", Gtk.main_quit)
        
        box = Gtk.Box(spacing=10)
        self.add(box)
        
        if self.pelicula[3] == "":
            caratula="pelis/sin_caratula.jpg"
        else:
            caratula=self.pelicula[3]    
        
        image = Gtk.Image()
        image.set_from_file(caratula)
        box.add(image)
        
        #label = Gtk.Label()
        #label.set_label("Titulo:\n"+
        #        self.pelicula[1]+"\n"+
        #        "Año:\n"+
        #        self.pelicula[2]+"\n"+
        #        "Sitio:\n"+
        #        self.pelicula[4])
        #box.add(label)
        
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
        
        #titulo_entry.set_text(self.pelicula[1])
        #titulo_entry.set_editable(False)
        #anho_entry.set_text(self.pelicula[2])
        #anho_entry.set_editable(False)
        #sitio_entry.set_text(self.pelicula[4])
        #sitio_entry.set_editable(False)
                
        vbox.add(titulo_label)
        vbox.add(titulo_entry)
        vbox.add(anho_label)
        vbox.add(anho_entry)
        vbox.add(sitio_label)
        vbox.add(sitio_entry)
        
        #sitio_entry.grab_focus()
        
                
        self.show_all()
