
import random
import mariadb
import dbcreds

# Ask the user if they would like to sign up a new account or sign in to an existing account
#   If the signup / in is unsuccessful, ask them again
def signin():
    print("Please sign in to play!")
    username = input("Username: ")
    password = input("Password: ")
    conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password,host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    cursor = conn.cursor()
    cursor.execute("CALL login(%s, %s)", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        print("Invalid username or password")
        if input("Would you like to sign up? (y/n) ") == "y":
            signup()
        print("please signin again")
        signin()
    else:
        print("Welcome, " + user[1] + "!")
        return user[0]
def signup():
    print("Please sign up to play!")
    username = input("Username: ")
    password = input("Password: ")
    conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password,host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    cursor = conn.cursor()
    cursor.execute("CALL add_client(%s, %s)", (username, password))
    conn.commit()
    conn.close()
    return
# Give the user the option to either create a new fighter or pick an existing fighter
#   To create a new fighter, prompt the user for a name. Once given, allow the user to pick 4 moves from the moves in the DB.
def create_fighter(client_id):
    print("Please create a new fighter!")
    username = input("Name: ")
    move1 = input("Move 1: ")
    move2 = input("Move 2: ")
    move3 = input("Move 3: ")
    move4 = input("Move 4: ")
    conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password,host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    cursor = conn.cursor()
    # procedure add_fighter(client_id int, move_one int, move_two int, move_three int, move_four int, name varchar(255))
    cursor.execute("CALL add_fighter(%s, %s, %s, %s, %s, \"%s\")" % (client_id, move1, move2, move3, move4, username))
    conn.commit()
    conn.close()
    print("Fighter created!")
    return username

#   To pick an existing fighter, show the client all existing fighters, and allow them to pick which one they want to fight with
def choose_fighter(user):
    conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password,host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    cursor = conn.cursor()
    cursor.execute(f"CALL get_fighters({user})")
    fighters = cursor.fetchall()
    print("Choose a fighter to fight with:")
    for fighter in fighters:
        print(fighter[0], fighter[6])
    fighter_id = input("Fighter ID: ")
    for fighter in fighters:
        if fighter[0] == int(fighter_id):
            print("Fighter selected!", fighter[6])
            return fighter
    print("Invalid fighter ID!")
    choose_fighter(user)

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
    return int(difficulty)

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

user = signin()

#ask if user would like to create fighter
if input("Would you like to create a fighter? (y/n)") == "y":
    create_fighter(user)

#choose a fighter 
fighter = choose_fighter(user)

difficulity = choose_difficulity()

#select opponent
print("Please select an opponent: ")
conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password,host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
cursor = conn.cursor()
cursor.execute("CALL get_all_fighters()")
opponents = cursor.fetchall()

cursor.execute("CALL get_moves()")
moves = cursor.fetchall()
conn.close()

for opponent in opponents:
    print(opponent[0], opponent[5])

chosen_opponent_id = input("Please select an opponent: ")
for opponent in opponents:
    if opponent[0] == int(chosen_opponent_id):
        chosen_opponent = opponent

hp = chosen_opponent[6] + 50 * (difficulity - 1)
attacks = [[0, 0], [0, 0], [0, 0], [0, 0]]
enemy_attacks = [[0, 0], [0, 0], [0, 0], [0, 0]]

for move in moves:
    if fighter[2] == move[0]:
        attacks[0] = [move[2], move[3]]
    elif fighter[3] == move[0]:
        attacks[1] = [move[2], move[3]]
    elif fighter[4] == move[0]:
        attacks[2] = [move[2], move[3]]
    elif fighter[5] == move[0]:
        attacks[3] = [move[2], move[3]]

for move in moves:
    if opponent[1] == move[0]:
        enemy_attacks[0] = [move[2], move[3]]
    elif opponent[2] == move[0]:
        enemy_attacks[1] = [move[2], move[3]]
    elif opponent[3] == move[0]:
        enemy_attacks[2] = [move[2], move[3]]
    elif opponent[4] == move[0]:
        enemy_attacks[3] = [move[2], move[3]]

#start game
print("Starting game...")
print(f"opponent hp: {hp}")

while hp > 0:
    attack = int(input("attack (1, 2, 3, 4): "))
    dmg = random.randint(attacks[attack - 1][0], attacks[attack - 1][1])
    hp -= dmg
    print(f"attacked for: {attacks[attack - 1][0]} - {attacks[attack - 1][1]} damage, hit for: {dmg} - enemy hp: {hp}")

    #enemy attack
    enemy_roll = random.randint(0, 3)
    print(f"the enemy attacks you for {random.randint(enemy_attacks[enemy_roll][0], enemy_attacks[enemy_roll][1])} damage")

