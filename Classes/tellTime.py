import time


def tell_current_time():
    from Classes.ActionScript import speak
    t = time.localtime()
    current_time = time.strftime("%H %M", t)
    current_time = "its currently " + current_time
    speak(current_time)
    pass
