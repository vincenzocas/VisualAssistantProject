from win10toast import ToastNotifier
from enum import Enum


enumNotifications = Enum("NotificationsEnum", [("Ready", "Ready to capture"),
                                               ("Previous", "Go Back to the previous page"),
                                               ("Next", "Go to the next page"),
                                               ("VolumeF", "Volume adjusted"),
                                               ("VolumeS", "Volume adjusting"),
                                               ("ScrollF", "Scroll performed"),
                                               ("ScrollS", "Scrolling"),
                                               ("Minimize", "Windows minimized")])



def notify(notification):
    try:
        toaster = ToastNotifier()
        toaster.show_toast(notification.name,
                           notification.value,
                           duration=2, icon_path="")
        pass
    except:
        print("could not execute the toast")
        pass



if __name__ == "__main__":
    # Passa un elemento dell'enumerazione alla funzione
    notification = enumNotifications.Previous
    notify(notification)
