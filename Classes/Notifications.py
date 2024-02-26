from win10toast import ToastNotifier
from enum import Enum

enumNotifications = Enum("NotificationsEnum", [("Previous", "Go Back to the previous page"),
                                               ("Next", "Go to the next page"),
                                               ("VolumeF", "Volume adjusted"),
                                               ("VolumeS", "Volume adjusting"),
                                               ("ScrollF", "Scroll performed"),
                                               ("ScrollS", "Scrolling"),
                                               ("Minimize", "Windows minimized")])

def notify(notification):
    toaster = ToastNotifier()
    toaster.show_toast(notification.name, notification.value, duration=1)


if __name__ == "__main__":
    # Passa un elemento dell'enumerazione alla funzione
    notification = enumNotifications.Previous
    notify(notification)