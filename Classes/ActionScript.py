from Classes.actions import actions
import pyttsx3
from Classes.volumeManager import VolumeManager
from Classes.tellTime import tell_current_time

def take_queries():
    volume_manager = VolumeManager()
    Hello()

    # while True:
    #     query = take_command().lower()
    #     # TODO: create switch statement to check actions that can be realized
    #     pass
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


def take_command() -> str:
    """
    check what command to issue using the AI previously trained
    :return: a str with the predicted command from the hand movements
    """
    return ""
