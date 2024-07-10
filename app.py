

import mariadb
import dbcreds

# Ask the user if they would like to sign up a new account or sign in to an existing account
#   If the signup / in is unsuccessful, ask them again
def signin():
    print("Please sign in to play!")
    username = input("Username: ")
    password = input("Password: ")
    mariadb.connect(user=dbcreds.user, password=dbcreds.password,host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    cursor = mariadb.connection.cursor()
    cursor.execute("CALL login(%s, %s)", (username, password))
    user = cursor.fetchone()
    if user is None:
        print("Invalid username or password")
        signin()
    else:
        print("Welcome, " + user[1] + "!")
        return user[0]
    
# Give the user the option to either create a new fighter or pick an existing fighter
#   To create a new fighter, prompt the user for a name. Once given, allow the user to pick 4 moves from the moves in the DB.
def create_fighter(client_id):
    print("Please create a new fighter!")
    username = input("Name: ")
    move1 = input("Move 1: ")
    move2 = input("Move 2: ")
    move3 = input("Move 3: ")
    move4 = input("Move 4: ")
    cursor = mariadb.connection.cursor()
    # procedure add_fighter(client_id int, move_one int, move_two int, move_three int, move_four int, name varchar(255))
    cursor.execute("CALL add_fighter(%s, %s, %s, %s, %s, %s)" % (client_id, move1, move2, move3, move4, username))
    cursor.commit()
    print("Fighter created!")
    return username

#   To pick an existing fighter, show the client all existing fighters, and allow them to pick which one they want to fight with
def choose_fighter():
    cursor = mariadb.connection.cursor()
    cursor.execute("CALL get_all_fighters()")
    fighters = cursor.fetchall()
    print("Choose a fighter to fight with:")
    for fighter in fighters:
        print(fighter[1])
    fighter_id = input("Fighter ID: ")
    cursor.commit()
    return fighter_id

# Give the user the option to either fight a weak opponent, a fair opponent, or a strong opponent
#   Beating a weak opponent will award 1 point
#   Beating a fair opponent will award 2 points
#   Beating a strong opponent  will award 4 points
def choose_difficulity():
    print("Choose a difficulty level:")
    print("1 - Weak")
    print("2 - Fair")
    print("3 - Strong")
    difficulty = input("Difficulty: ")
    return difficulty

# A fight will be turn based, meaning that it will prompt the user for a move selection each time. It will follow the flow:
#   Show the user each move available to their fighter
#   Ask the user for an input
#   Calculate the damage done to the opponent
#       This would be making a random number between the lower and upper range of the move selected
#   Check to see if you win
#       If you do, inform the user, add the appropriate amount of points to the fighter, and return to asking the user what they want to do
#   Randomly pick a move from the computer
#   Calculate the damage done to the player
#       This would be making a random number between the lower and upper range of the move
#           If the opponent is weak, subtract some damage
#           If the opponent is fair, leave their damage alone
#           If the opponent is strong, add some damage
#   Check to see if the computer wins
#       If they do, inform the user and return to asking the user what they want to do