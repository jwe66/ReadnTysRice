import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

class NotificationDaemon(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName("org.example.NotificationDaemon", bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/example/NotificationDaemon')

    @dbus.service.method("org.example.NotificationDaemon", in_signature='ss', out_signature='u')
    def Notify(self, title, message):
        print(f"Notification: {title}\n{message}\n")
        return 0

def main():
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("org.example.NotificationDaemon", bus=session_bus)
    daemon = NotificationDaemon()

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()
