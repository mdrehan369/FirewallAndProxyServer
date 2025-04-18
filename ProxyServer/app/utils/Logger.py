from termcolor import colored, cprint
from datetime import datetime

class Logger:
    def __init__(self):
        pass
    def print(self, text: str, color: str):
        print(colored(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {text}", color))
    def printWithBg(self, text: str, color: str, bg: str = "on_black"):
        cprint(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {text}", color, bg)
    def success(self, text: str):
        cprint(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {text}", "white", "on_green")
    def error(self, text: str):
        cprint(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {text}", "white", "on_red")
    def info(self, text: str):
        cprint(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {text}", "white", "on_cyan")