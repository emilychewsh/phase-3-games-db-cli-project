from config import session
from models import User, Game, Favourite
from colorama import Back, Fore, Style
import os

logged_user = None

def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

