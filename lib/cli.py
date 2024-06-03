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


##################################################### Functions for choices 
def view_all_games(games):
    if len(games)>0:
        for game in games:
            print(game)
    else:
        print("No games...")
    
    print('-'*30)
    print("\nPlease enter the game ID to view more details (type 'back' to go back):")

    id_input = input()

    if id_input == "back":
        clear()
        return
    else:
        try:
            game_id = int(id_input)
            game = [ g for g in games if g.id == game_id ]

            if len(game)>0:
                game = game[0]
                
                clear()

                #Print and display game info for selected ID
                print(f"{game.title.upper()}")
                print(f"GENRE: {game.genre}")
                print(f"DESCRIPTION: {game.description}")

                print("Other Details")
                print(f"Rating: {game.rating}")
                print(f"Platform: {game.platform}")
                print(f"Trailer: {game.trailer}")
            else:
                print("No game found! Try again.")
        
        except ValueError:
            print("Invalid input. Please enter a valid game ID or 'back' to return to previous selection.")
           

def all():
    clear()
    games = session.query(Game).all()
    view_all_games(games)

#####################################################
def start():
    greet()

    loop = True

    while loop:
        choice = main_menu()
        if choice == "1":
            clear()
            all()
            # print("Do you want to view games in general or by genre?")
        elif choice == "2":
            clear()
        elif choice == "3":
            clear()
            loop = False
        else:
            print("Please enter a valid selection")
            choice = main_menu()

    print("Thank you for using Crux Games App, see you again!")


#############################################################

if __name__ == "__main__":
    start()