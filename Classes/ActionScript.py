from keras.models import load_model
import pyttsx3
from Classes.volumeManager import VolumeManager
from Classes.tellTime import tell_current_time
from Classes.windowManager import minimizeOpenWindow
from Classes.singleFramePredictor import take_command
from Classes.MouseNKeyboard import KeyPressManager, scrollUp, scrollDown, scroll
import Classes.Notifications as n

def take_queries():
    volume_manager = VolumeManager(0)
    kpm = KeyPressManager()
    model = load_model("./TrainedModel.h5")
    Hello()
    while True:
        #speak("checking for new command")
        query, _ = take_command("./TrainedModel.h5", model)
        if query is not None:
            query = query.lower()

        if query == "minimize":
            #speak("minimizing window")
            n.notify(n.enumNotifications.Minimize)
            minimizeOpenWindow()
            # print(query)
            pass
        elif query == "scrollup" or query == "scrolldown":
            #speak("scrolling")
            n.notify(n.enumNotifications.ScrollS)
            scroll(model)
            n.notify(n.enumNotifications.ScrollF)
            #speak("end of scrolling")
            # print(query)
            pass

        elif query == "next":
            #speak("next page")
            n.notify(n.enumNotifications.Next)
            kpm.nextPage()
            # print(query)
            pass
        elif query == "previous":
            #speak("last page")
            n.notify(n.enumNotifications.Previous)
            kpm.lastPage()
            # print(query)
            pass
        elif query == "volume":
            #speak("adjusting volume")
            n.notify(n.enumNotifications.VolumeS)
            volume_manager.captureChangeVolume()
            n.notify(n.enumNotifications.VolumeF)
            #speak("Setting new volume")

            # print(query)
            pass
        elif query == "exit" or query is None:
            #speak("Good bye User")
            # print(query)
            break
            pass

        pass
    pass


def Hello():
    """
    start up function to greet user
    """
    speak("Hello user")
    pass


def speak(dialogue: str):
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
