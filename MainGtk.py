
from pelisdb import PeliculasDB
from VentanaInfo import win2
import gi

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf
db = PeliculasDB()

class MyWin(Gtk.Window):
    
    def __init__(self):
        super().__init__()
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(10)
        self.set_default_size(1000, 500)
        
        pelis = db.consulta_peliculas()
        
        #imagenes = []
        #
        #for peli in pelis:
        #    if peli[3] != "":
        #        imagenes.append(peli[3])
        #    else:
        #        imagenes.append("pelis/1.jpg")
        
        #imagenes = [
        #    "pelis/57.jpg",
        #    "pelis/58.jpg",
        #    "pelis/59.jpg",
        #    "pelis/60.jpg",
        #    "pelis/61.jpg",
        #    "pelis/62.jpg",
        #    "pelis/63.jpg",
        #    "pelis/64.jpg",
        #    "pelis/65.jpg",
        #    "pelis/66.jpg",
        #    "pelis/67.jpg",
        #    "pelis/68.jpg"
        #]
        
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Pelis"
        self.set_titlebar(hb)
        
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="system-shutdown-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_start(button)
        button.connect("clicked", Gtk.main_quit)
        
        busqueda = Gtk.SearchEntry()
        busqueda.set_text("Titulo")
        busqueda.connect("event", self.borrar_entry)
        busqueda.connect("activate", self.buscar_pelicula)
        hb.add(busqueda)
        
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(10)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.crear_flowbox(self.flowbox, pelis)

        self.scrolled.add(self.flowbox)

        self.add(self.scrolled)
        
        #box = Gtk.Box()
        #self.add(box)    
        
        #button = Gtk.Button()
        #button.connect("clicked", self.pulsar_boton)
        #box.add(button)
        #button2 = Gtk.Button()
        #button2.connect("clicked", self.pulsar_boton)
        #box.add(button2)
        #
        #self.imagen = Gtk.Image()
        #self.imagen.set_from_file("pelis/68.jpg")
        #button.set_name("68")
        #button.set_image(self.imagen)
        #self.imagen2 = Gtk.Image()
        #self.imagen2.set_from_file("pelis/67.jpg")
        #button2.set_name("67")
        #button2.set_image(self.imagen2)
        
                                                               
    def pulsar_boton(self, widget):
        print("Boton "+widget.get_name()+" Pulsado")
        id = db.consulta_indibidual(int(widget.get_name()))
        print(id)
        ventana2=win2(id)
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
                button.set_image(self.redimensionar_imagen(peli[3]))
            else:
                button.set_image(self.redimensionar_imagen("pelis/sin_caratula.jpg"))
            button.connect("clicked", self.pulsar_boton)
            box.add(button)

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
    
    win = MyWin()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()