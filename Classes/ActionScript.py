

import os
import threading


from keras.models import load_model
import pyttsx3
from Classes.NewVolumeChanger import VolumeManager
from Classes.windowManager import minimizeOpenWindow
from Classes.singleFramePredictor import take_command

from Classes.MouseNKeyboard import KeyPressManager, scroll
import Classes.Notifications as n


def take_queries():
    volume_manager = VolumeManager(0)
    kpm = KeyPressManager()
    speak("Hello user")
    model = load_model("./TrainedModel.h5")
    while True:
        #speak("checking for new command")

        query, _ = take_command("./TrainedModel.h5", model)
        Hello()
        if query is not None:
            query = query.lower()

        if query == "minimize":
            speak("minimizing window")
            n.notify(n.enumNotifications.Minimize)
            minimizeOpenWindow()


            pass
        elif query == "scrollup" or query == "scrolldown":
            speak("scrolling")
            n.notify(n.enumNotifications.ScrollS)
            scroll(model)
            n.notify(n.enumNotifications.ScrollF)

            pass

        elif query == "next":

            n.notify(n.enumNotifications.Next)
            kpm.nextPage()

            pass
        elif query == "previous":

            n.notify(n.enumNotifications.Previous)
            kpm.lastPage()

            pass
        elif query == "volume":
            speak("adjusting volume")

            n.notify(n.enumNotifications.VolumeS)
            volume_manager.captureChangeVolume()
            n.notify(n.enumNotifications.VolumeF)

            pass
        elif query == "exit" or query is None:
            speak("Good bye user")
            break
            pass

        pass
    pass


def Hello():
    """
    start up function to greet user
    """
    n.notify(n.enumNotifications.Ready)

    pass


def speak(dialogue: str):
    threading.Thread(target=speakAndWait, args=(dialogue,)).start()
    pass


def speakAndWait(dialogue: str):
    """
    :param dialogue: the text to be read using text to speach
    :return: none
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # setter method .[0]=male voice and
    # [1]=female voice in set Property.
    engine.setProperty('voice', voices[1].id)

    # Method for the speaking of the assistant
    engine.say(dialogue)

    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()
    pass
