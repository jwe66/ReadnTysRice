import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import json

class NotificationDaemon(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName("org.example.NotificationDaemon", bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/example/NotificationDaemon')

    @dbus.service.method("org.example.NotificationDaemon", in_signature='ssv', out_signature='u')
    def Notify(self, title, message, image_data):
        notification_data = {
            'title': title,
            'message': message,
            'image_data': image_data
        }
        json_notification = json.dumps(notification_data, indent=2)
        print(json_notification)
        return 0

def on_properties_changed(interface, changed, invalidated):
    if "org.freedesktop.Notifications" in invalidated:
        return

    if "org.mpris.MediaPlayer2.Player" in interface:
        metadata = changed.get("Metadata", {})
        title = metadata.get("xesam:title", "")
        artist = metadata.get("xesam:artist", [""])[0]

        if title and artist:
            image_data = None  # Adjust this based on how image data is available in MPRIS notifications
            notification_data = {
                'title': f"Spotify - {artist}",
                'message': title,
                'image_data': image_data
            }
            json_notification = json.dumps(notification_data, indent=2)
            print(json_notification)

def on_notification_action(notification, action_key, user_data):
    title = notification.get("title", "")
    message = notification.get("body", "")
    image_data = None  # Adjust this based on how image data is available in generic notifications

    notification_data = {
        'title': title,
        'message': message,
        'image_data': image_data
    }
    json_notification = json.dumps(notification_data, indent=2)
    print(json_notification)

def main():
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()

    # Add MPRIS signal receiver
    session_bus.add_signal_receiver(on_properties_changed, dbus_interface="org.freedesktop.DBus.Properties")

    # Add generic notification receiver
    notifications_proxy = session_bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    notifications_proxy.connect_to_signal('NotificationClosed', on_notification_action, sender_keyword='sender', interface_keyword='interface')
    notifications_proxy.connect_to_signal('ActionInvoked', on_notification_action, interface_keyword='interface')

    name = dbus.service.BusName("org.example.NotificationDaemon", bus=session_bus)
    daemon = NotificationDaemon()

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()

