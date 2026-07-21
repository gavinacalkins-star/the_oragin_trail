#todo:



import time
import random
from playsound import playsound
import json
import os


wagon_name = None
pioner_name = None
distance_neded = 2170
distance_traveled = 0
food =100
helth = 100
wagon_damage = 0
alive = True
day = 0
save_file = "saves/save.json"


def save_variable(var_name, value):
    """Completely overwrites the file with ONLY this single variable."""
    # Create a fresh dictionary containing only this new variable
    new_data = {var_name: value}

    # Writing with "w" clears the file before adding the new JSON data
    with open(save_file, "w") as file:
        json.dump(new_data, file, indent=4)
    #print(f"Overwrote file! Saved single variable: '{var_name}' = {value}")


def get_saved_value(var_name):
    """Retrieves the value of the variable if it matches what is in the file."""
    if not os.path.exists(save_file):
        return None

    with open(save_file, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return None

    # Return the value if it matches the requested name
    return data.get(var_name, None)


playsound("media/sound/game start.mp3")
print('                        _.--.')
time.sleep(0.05)
print("                    _.-'_:-'||")
time.sleep(0.05)
print("                _.-'_.-::::'||")
time.sleep(0.05)
print("            _.-:'_.-::::::'  ||")
time.sleep(0.05)
print("    _..._.-:'_.-::::::::'    ||")
time.sleep(0.05)
print("  .:::::::-:::::::::::'      ||")
time.sleep(0.05)
print('  |         ||          _.._ ||')
time.sleep(0.05)
print('  |         ||       .-::::::-.')
time.sleep(0.05)
print('  |    _..._||      /:::::::::::\\')
time.sleep(0.05)
print('  |  .::::::::.    |:::::::::::::|')
time.sleep(0.05)
print('  |  ::::::::::.   |:::::::::::::|')
time.sleep(0.05)
print("  '-::::::::::::-.-:::::::::::::'")
time.sleep(0.05)
print("     '-::::::::::::::::::::::-'")
time.sleep(0.05)
print("        '-::::::::::::::::-'")
time.sleep(0.05)
print("  ()       '-::::::::-'        ()")
time.sleep(0.05)
print(' /  \\       (        )        /  \\')
time.sleep(0.05)
print('|    |_____|          |______|    |')
time.sleep(0.05)
print(' \\__/                          \\__/')
time.sleep(0.1)
print('==================================================================')
time.sleep(0.05)
print('#   # ##### #      ####  ###  #   # #####       #####  ###  ')
time.sleep(0.05)
print('#   # #     #     #     #   # ## ## #             #   #   # ')
time.sleep(0.05)
print('# # # ###   #     #     #   # # # # ###           #   #   # ')
time.sleep(0.05)
print('# # # #     #     #     #   # #   # #             #   #   # ')
time.sleep(0.05)
print(' # #  ##### #####  ####  ###  #   # #####         #    ###  ')
time.sleep(0.05)
print('')
time.sleep(0.05)
print('##### #   # #####        ###  ####  #####  ####  ###  #   # ')
time.sleep(0.05)
print('  #   #   # #           #   # #   # #     #     #   # ##  # ')
time.sleep(0.05)
print('  #   ##### ###         #   # ####  ###   #  ## #   # # # # ')
time.sleep(0.05)
print('  #   #   # #           #   # #  #  #     #   # #   # #  ## ')
time.sleep(0.05)
print('  #   #   # #####        ###  #   # #####  ####  ###  #   # ')
time.sleep(0.05)
print('')
time.sleep(0.05)
print('##### ####   ###  ##### #     ')
time.sleep(0.05)
print('  #   #   # #   #   #   #     ')
time.sleep(0.05)
print('  #   ####  #####   #   #     ')
time.sleep(0.05)
print('  #   #  #  #   #   #   #     ')
time.sleep(0.05)
print('  #   #   # #   # ##### ##### ')
time.sleep(0.05)
print('==================================================================')
print('                  A game of grit, grass, and dysentery.           ')


wagon_name = input("Wagon name: ")
pioner_name = input("Pioner name: ")
print(f"Welcome {pioner_name} to the Oregon Trail! Your wagon is named {wagon_name}. You have {food} units of food and {helth} health. Your goal is to travel {distance_neded} miles to reach your destination. Good luck!")

while alive and distance_traveled < distance_neded:
    print("--------------------------------------------------")
    print(f"\nDay {day}:")
    print(f"Distance traveled: {distance_traveled} miles")
    print(f"Food remaining: {food} units")
    print(f"Health: {helth}")
    print(f"Wagon damage: {wagon_damage}")
    if wagon_damage > 0:
        print("you will travel slower because your wagon is damaged")
    print("--------------------------------------------------")

    if random.randint(0, 10) == 0:
        encounter = random.choice(["bandits", "storm", "sickness"])

        if encounter == "bandits":
            print("You encountered bandits! They stole some of your food and damaged the wagon.")
            if food > 21:
                food -= random.randint(10, 20)
                wagon_damage += random.randint(10, 20)
            else:
                print("You don't have enough food to lose. The bandits hit you instead")
                helth -= random.randint(1, 20)
                wagon_damage += random.randint(1, 20)

        elif encounter == "storm":
            print("A storm has hit! You lost some food and your health decreased.")
            food -= random.randint(5, 15)
            helth -= random.randint(5, 15)
            wagon_damage += random.randint(5, 15)

        elif encounter == "sickness":
            print("You have fallen ill! Your health has decreased.")
            helth -= random.randint(10, 20)

        print(f"After the encounter, you have {food} units of food and {helth} health.")
        input("Press Enter to continue...")
        time.sleep(1)  # Simulate the passage of time
        print(".")
        time.sleep(1)  # Simulate the passage of time
        print(".")

    else:
        action = input("What would you like to do? (travel/rest/hunt/status/repair/exit): ").lower()

        if action == "travel":
            if wagon_damage > 50:
                print("Your wagon is too damaged to travel. You need to repair it first.")

            else:

                travel_distance = round(random.randint(12, 15) - (wagon_damage / 10))  # miles traveled per day
                distance_traveled += travel_distance
                food -= random.randint(5, 15)  # food consumed per day of travel
                helth -= random.randint(1, 10)  # health decreases due to travel
                wagon_damage += random.randint(1, 5)  # wagon damage increases due to travel
                print(f"You traveled {travel_distance} miles.")

        elif action == "repair":
            wagon_damage -= random.randint(5, 15)
            food -= random.randint(5, 15)
            helth -= random.randint(1, 10)
            print(f"You repared the wagon but lost some food and your health decreases.")

        elif action == "rest":
            food -= random.randint(5, 10)  # food consumed while resting
            helth += random.randint(5, 15)  # health improves while resting
            print("You rested for the day.")

        elif action == "hunt":
            food_gained = random.randint(15, 25)  # food gained from hunting
            food += food_gained
            helth -= random.randint(1, 10)  # health decreases due to hunting effort
            print(f"You hunted and gained {food_gained} units of food.")

        elif action == "status":
            print(f"Distance traveled: {distance_traveled} miles")
            print(f"Food remaining: {food} units")
            print(f"Health: {helth}")

        elif action == "exit":
            print("Exiting the game. Goodbye!")
            save_variable("distance_traveled", distance_traveled)
            save_variable("food", food)
            save_variable("helth", helth)
            save_variable("wagon_damage", wagon_damage)
            save_variable("day", day)
            save_variable("wagon_name", wagon_name)
            save_variable("pioner_name", pioner_name)
            save_variable("alive", alive)
            raise SystemExit

        else:
            print("Invalid action. Please choose again.")

        if food <= 0:
            alive = False
            print("You have run out of food and cannot continue. You have died.")

        if helth <= 0:
            alive = False
            print("Your health has deteriorated too much. You have died.")

        #
        # add capps for varubols
        #
        if wagon_damage <= 0:
            wagon_damage = 0

        if helth >= 100:
            helth = 100

        if food >= 100:
            food = 100

    day += 1
    time.sleep(1)  # Simulate the passage of time
    print(".")
    time.sleep(1)  # Simulate the passage of time
    print(".")
    time.sleep(1)  # Simulate the passage of time
    print(".")
    time.sleep(1)  # Simulate the passage of time
    print(".")
    time.sleep(1)  # Simulate the passage of time


