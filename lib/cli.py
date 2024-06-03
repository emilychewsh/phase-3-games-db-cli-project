from config import session
from models import User, Game, Favourite
from colorama import Back, Fore, Style
import os

logged_user = None

def clear(): #Clearing terminal
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def login(username): #Check if user exists
    user = session.query(User).filter(User.name == username).first()

    if not user:
        user = User(name=username)
        session.add(user)
        session.commit()

        print(f"Hi {user.name}, you have successfully been registered into the Crux Games App!")

    else:
        clear()
        print(f"Welcome back, {user.name}")

    global logged_user
    logged_user = user


def greet(): #Greet
    print("Welcome to Crux games database where you can look up your favourite games!")
    print("Please enter your username to log in or sign up by entering a username:")
    
    username = input()
    login(username)


def main_menu():
    print(f"-"*30)
    print("By Emily Chew | e: emilychewsh@gmail.com")
    print(f"-"*30)

    print("Please select where you want to go...")
    print("1. " + "View all games")
    print("2. " + "View your saved favourites")
    print("3. " + "Exit this app")

    choice = input()
    return choice #Return user's choice

def start():
    greet()

    loop = True

    while loop:
        choice = main_menu()
        while True:
            if choice == "1":
                clear()
                
                break
            elif choice == "2":
                clear()
                
                break
            elif choice == "3":
                clear()
                loop = False
                break
            else:
                print("Please enter a valid selection")

    print("Thank you for using Crux Games App, see you again!")




if __name__ == "__main__":
    start()