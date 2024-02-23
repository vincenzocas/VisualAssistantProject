from Classes.actions import actions
import pyttsx3
from Classes.volumeManager import VolumeManager
from Classes.tellTime import tell_current_time
from Classes.windowManager import minimizeOpenWindow
from Classes.singleFramePredictor import take_command
from Classes.MouseNKeyboard import KeyPressManager, scrollUp, scrollDown


def take_queries():
    volume_manager = VolumeManager(0)
    kpm = KeyPressManager()

    Hello()
    while True:
        query = take_command("./TrainedModel.h5").lower()

        if query == "minimize":
            minimizeOpenWindow()
            print(query)
            pass
        elif query == "scrollup":
            scrollUp()
            print(query)
            pass
        elif query == "scrolldown":
            scrollDown()
            print(query)
            pass
        elif query == "next":
            kpm.nextPage()
            print(query)
            pass
        elif query == "last":
            kpm.lastPage()
            print(query)
            pass
        elif query == "volume":
            volume_manager.captureChangeVolume()
            print(query)
            pass
        elif query == "exit":
            print(query)
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
