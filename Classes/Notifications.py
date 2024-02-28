import threading

from win10toast import ToastNotifier
from enum import Enum

# import plyer.platforms.win.notification
# from plyer import notification as nt

enumNotifications = Enum("NotificationsEnum", [("Ready", "Ready to capture"),
                                               ("Previous", "Go Back to the previous page"),
                                               ("Next", "Go to the next page"),
                                               ("VolumeF", "Volume adjusted"),
                                               ("VolumeS", "Adjusting volume"),
                                               ("ScrollF", "Scroll performed"),
                                               ("ScrollS", "Scrolling"),
                                               ("Minimize", "Windows minimized")])


def notify(notification):
    threading.Thread(target=notifyOnThread, args=(notification,)).start()
    pass


def notifyOnThread(notification):
    try:
        toaster = ToastNotifier()
        toaster.show_toast(notification.name,
                           notification.value,
                           duration=2,
                           icon_path=""
                           )

        # nt.notify(notification.name, notification.value, toast=True, timeout=1)
        pass
    except:
        print("could not execute the toast")
        pass
    pass


if __name__ == "__main__":
    # Passa un elemento dell'enumerazione alla funzione
    notification = enumNotifications.Previous
    notify(notification)
