from Classes.actions import actions
import pyttsx3
from Classes.volumeManager import VolumeManager
from Classes.tellTime import tell_current_time
from Classes.windowManager import minimizeOpenWindow
from Classes.singleFramePredictor import take_command
from Classes.MouseNKeyboard import KeyPressManager, scrollUp, scrollDown, scroll


def take_queries():
    volume_manager = VolumeManager(0)
    kpm = KeyPressManager()

    Hello()
    query, model = take_command("./TrainedModel.h5", None)

    while True:
        query, model = take_command("./TrainedModel.h5", model)
        if query is not None:
            query= query.lower()

        if query == "minimize":
            speak("minimizing window")
            minimizeOpenWindow()

            # print(query)
            pass
        elif query == "scrollup":
            speak("scrolling")
            scrollUp()
            scroll(model)

            speak("end of scrolling")
            # print(query)
            pass
        elif query == "scrolldown":
            speak("scrolling")
            scrollDown()
            scroll(model)

            speak("end of scrolling")

            # print(query)
            pass
        elif query == "next":
            speak("next page")
            kpm.nextPage()
            # print(query)
            pass
        elif query == "previous":
            speak("last page")
            kpm.lastPage()
            # print(query)
            pass
        elif query == "volume":
            speak("adjusting volume")
            volume_manager.captureChangeVolume()

            speak("Setting new volume")

            # print(query)
            pass
        elif query == "exit":
            speak("Good bye User")
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
