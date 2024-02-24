import winreg

def get_default_browser_windows():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice") as key:
        value = winreg.QueryValueEx(key, 'ProgId')[0]
        return value

default_browser = get_default_browser_windows()
print("Il browser predefinito su Windows è:", default_browser)
