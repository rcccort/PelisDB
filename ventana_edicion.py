import gi
from comfiguracion import Comfiguracion
from pelisdb import PeliculasDB

APP = "pelisdb"
config = f"{APP}.conf"
config_base = {'ultimo_lugar':'Carpeta 1','dir_caratulas':'pelis'}

cf = Comfiguracion(APP, config, config_base)

db = PeliculasDB(cf.get_dir())

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio

class VentanaEdicion(Gtk.Window):
    
    def __init__(self, pelicula, ultima):
        super().__init__()
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(10)
        self.set_default_size(400, 300)
        self.pelicula=pelicula
        self.ultima=ultima
        
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        if self.pelicula != '':
            hb.props.title = 'Modificar Película'
        else:
            hb.props.title = 'Añadir Pelicula'
        
        self.set_titlebar(hb)
        
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="list-add-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_start(button)
        button.connect("clicked", self.Boton_Pulsado)
        
        box = Gtk.Box(spacing=10)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(box)
        
        self.store = Gtk.ListStore(str)
        self.llenar_store()
        
        titulo_label = Gtk.Label()
        self.titulo_entry = Gtk.Entry()
        self.titulo_entry.set_name("1")
        self.titulo_entry.connect("activate", self.cambiar_foco)
        anho_label = Gtk.Label()
        self.anho_entry = Gtk.Entry()
        self.anho_entry.set_name("2")
        self.anho_entry.connect("activate", self.cambiar_foco)
        caratula_label = Gtk.Label()
        self.caratula_entry = Gtk.Entry()
        self.caratula_entry.set_name("3")
        self.caratula_entry.connect("activate", self.cambiar_foco)
        sitio_label = Gtk.Label()
        self.sitio_combo = Gtk.ComboBox.new_with_model_and_entry(self.store)
        self.sitio_combo.set_entry_text_column(0)
        self.sitio_combo.get_child().set_text(self.ultima)

        titulo_label.set_label("Titulo:")
        titulo_label.set_xalign(0)
        anho_label.set_label("Año:")
        anho_label.set_xalign(0)
        caratula_label.set_label("Caratula:")
        caratula_label.set_xalign(0)
        sitio_label.set_label("Sitio donde esta:")
        sitio_label.set_xalign(0)

        if self.pelicula != '':
            self.titulo_entry.set_text(self.pelicula[1])
            self.anho_entry.set_text(self.pelicula[2])
            self.caratula_entry.set_text(self.pelicula[3])
            self.sitio_combo.get_child().set_text(self.pelicula[4])

        box.add(titulo_label)
        box.add(self.titulo_entry)   
        box.add(anho_label)
        box.add(self.anho_entry)
        box.add(caratula_label)
        box.add(self.caratula_entry)
        box.add(sitio_label)
        box.add(self.sitio_combo)
        
        self.show_all()
        
    def Boton_Pulsado(self, objeto):
        
        if self.pelicula == "":
            
            eleccion = self.sitio_combo.get_active_iter()
            if eleccion is not None:
                model = self.sitio_combo.get_model()
                sitio = model[eleccion][0]
            else:
                entry = self.sitio_combo.get_child()
                sitio = entry.get_text()
            pelicula = (self.titulo_entry.get_text(),
                        self.anho_entry.get_text(),
                        self.caratula_entry.get_text(),
                        sitio)
            
            if pelicula[0] != "" and pelicula[3] != "":
                
                n = db.insertar_datos(pelicula)
                if n==0:
                    print("Imposible Añadir Pelicula\n")
                    dato = cf.read_conf()
                    dato['ultimo_lugar'] = sitio
                    cf.escribir_datos(dato)
                else:
                    print("Pelicula Añadida con éxito!!!\n")
                self.destroy()
            else:
                self.mesaje_error()
                self.titulo_entry.grab_focus()
                print("falta al menos titulo o sitio")
        
        else:
            sitio = self.sitio_combo.get_child().get_text()
            pelicula = (self.titulo_entry.get_text(),
                        self.anho_entry.get_text(),
                        self.caratula_entry.get_text(),
                        sitio)
            pelicula_db = db.consulta_indibidual(self.pelicula[0])
            
            action = True
            if pelicula[0] != pelicula_db[1]:
                print("editamos titulo")
                db.editar_pelicula('titulo', pelicula[0], self.pelicula[0])
                action = False
            if pelicula[1] != pelicula_db[2]:
                print("editamos año")
                db.editar_pelicula('anho', pelicula[1], self.pelicula[0])
                action = False
            if pelicula[2] != pelicula_db[3]:
                print("editamos caratula")
                db.editar_pelicula('caratula', pelicula[2], self.pelicula[0])
                action = False
            if pelicula[3] != pelicula_db[4]:
                print("editamos sitio")
                db.editar_pelicula('ubicacion', pelicula[3], self.pelicula[0])
                dato = cf.read_conf()
                dato['ultimo_lugar'] = sitio
                cf.escribir_datos(dato)
                action = False
            if action:
                print("no se edita nada")
                
    def llenar_store(self):
        
        peliculas = db.consulta_peliculas()
        lugares = []
        for pelicula in peliculas:
            if pelicula[4] not in lugares:
                lugares.append(pelicula[4])
                self.store.append([pelicula[4]])
    
    def cambiar_foco(self, entry):

        entry_name = {1:self.titulo_entry, 2:self.anho_entry, 3:self.caratula_entry}
        name = int(entry.get_name())+1
        if name == 4:
            name = 1
        entry_name[name].grab_focus()
        if self.pelicula == "":
            self.Boton_Pulsado(entry)
            
    def mesaje_error(self):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Falta Campos por rellenar!!",
        )
        dialog.format_secondary_text(
            "Titulo y Sitio son Obligatorios"
        )
        dialog.run()

        dialog.destroy()
        
        
#if __name__=='__main__':
#    
#    busqueda = db.consulta_indibidual(95)
#    #busqueda=''
#    win = win4(busqueda,'Carpeta 1')
#    win.connect("destroy", Gtk.main_quit)
#    #win.show_all()
#    Gtk.main()