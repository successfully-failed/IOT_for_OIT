import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk



class Mainwindow (gtk.Window):
    def __init__ (self):
        super().__init__(title="IOT for OIOM")





window = Mainwindow()
window.connect("destroy", gtk.main_quit)
window.show_all()
gtk.main()

