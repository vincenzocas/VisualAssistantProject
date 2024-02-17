import math

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER


class VolumeManager:
    volume_levels = 5
    volume_delta = 0.015 * volume_levels  # approx. #volume_levels points in percent

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        # self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)
        pass

    def change_volume(self, amount: float):
        self.volume.SetMasterVolumeLevel(amount, None)
        pass

    def raise_volume(self):
        t = self.volume.GetMasterVolumeLevel()
        # transform from dB scale to 0.0-1.0 "linear" function
        t = math.pow(10.0, (t / 20))

        # change by predetermined amount the volume
        t = t + self.volume_delta
        # chceck to make sure is not >100%
        if t > 1.0:
            t = 0.9999
        # transform back again to dB
        t = 20 * math.log10(t)
        # change it
        self.change_volume(t)

        pass

    def lower_volume(self):
        # same as raise_volume but instead of adding the amount we subtract it
        t = self.volume.GetMasterVolumeLevel()
        t = math.pow(10.0, (t / 20))
        t = t - self.volume_delta

        #check to make sure best it can do is ~ 1%
        if t <= 0.001:
            t = 0.0015
        t = 20 * math.log10(t)
        self.change_volume(t)
        pass

    pass
