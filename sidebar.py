import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Side Bar")
        
        self.set_border_width(10)


        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)

        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(self.box)
        
        
        self.stack.add_titled(self.create_page1(), "CamerasPage", "Cameras")
        self.stack.add_titled(self.create_page2(), "AlertsPage", "Alerts")
        self.stack.add_titled(self.create_page3(), "RulesPage", "Rules")
        self.stack.add_titled(self.create_page4(), "SetupPage", "Setup")
        self.stack.add_titled(self.create_page5(), "SettingsPage", "Settings")
        self.stack.add_titled(self.create_page6(), "LoginPage", "Login")

        self.stack_switcher.set_orientation(Gtk.Orientation.VERTICAL)

        

        self.box.pack_start(self.stack_switcher, False, True, 0)
        self.box.pack_start(self.stack, True, True, 0)

    def create_page1(self):
        label = Gtk.Label()
        label.set_markup("Cameras")
        return label
    
    def create_page2(self):
        label = Gtk.Label()
        label.set_markup("Alerts")
        return label
    
    def create_page3(self):
        label = Gtk.Label()
        label.set_markup("Rules")
        return label
    
    def create_page4(self):
        label = Gtk.Label()
        label.set_markup("Setup")
        return label
    
    def create_page5(self):
        label = Gtk.Label()
        label.set_markup("Settings")
        return label
    
    def create_page6(self):
        label = Gtk.Label()
        label.set_markup("Login")
        return label
    

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()