import os
from gi.repository import GLib
import json

class NotificationDaemon:
    def __init__(self):
        GLib.timeout_add(5000, self.check_notifications)
    
    def check_notifications(self):
        # Simulate MPRIS notification
        title = "Spotify - Artist Name"
        message = "Song Title"
        image_data = None  # Replace with actual image data if available

        notification_data = {
            'title': title,
            'message': message,
            'image_data': image_data
        }
        json_notification = json.dumps(notification_data, indent=2)
        print(json_notification)

        # Send notification using dunstify
        command = f'dunstify -r 1337 -i 0 -a "Notification" "{json_notification}"'
        os.system(command)
        
        return True

def main():
    NotificationDaemon()
    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()

