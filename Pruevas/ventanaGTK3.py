import gi

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio

class MyWin(Gtk.Window):
    def __init__(self)  :
        super().__init__()
        self.set_border_width(10)
        self.set_default_size(400, 200)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Hello World!!"
        self.set_titlebar(hb)

        self.button2 = Gtk.Button()
        iconluna = Gio.ThemedIcon(name="weather-clear-night-symbolic")
        self.imageluna = Gtk.Image.new_from_gicon(iconluna, Gtk.IconSize.BUTTON)
        iconsol = Gio.ThemedIcon(name="weather-clear-symbolic")
        self.imagesol = Gtk.Image.new_from_gicon(iconsol, Gtk.IconSize.BUTTON)
        self.button2.add(self.imageluna)
        self.button2.connect("clicked", self.pulsar_boton)
        hb.pack_end(self.button2)
        
        self.box = Gtk.Box()
        #self.box.set_size(60, 60)
        self.add(self.box)
        
        self.button = Gtk.Button(label="Pulsame")
        #self.button.set_alignment(0, 0)
        self.button.connect("clicked", self.pulsar_boton)
        self.box.pack_start(self.button, True, True, 0)
                        
    def pulsar_boton(self, widget):
        print("Boton Pulsado")
        # Forzar el tema oscuro usando gtk-application-prefer-dark-theme
        settings = Gtk.Settings.get_default()
        current_theme = settings.get_property("gtk-application-prefer-dark-theme")
        if current_theme:
            self.button2.set_image(self.imageluna)
            settings.set_property("gtk-application-prefer-dark-theme", False)
        else:
            self.button2.set_image(self.imagesol)
            settings.set_property("gtk-application-prefer-dark-theme", True)

win = MyWin()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
