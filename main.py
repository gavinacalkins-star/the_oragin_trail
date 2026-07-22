#todo
#   add famly members




import time
import random
from playsound import playsound
import json
import os


wagon_name = None
pioner_name = None
distance_needed = 2170
distance_traveled = 0
food =100
health = 100
wagon_damage = 0
alive = True
day = 0
save_file = "saves/save.json"
saves_list = [f for f in os.listdir("saves") if os.path.isfile(os.path.join("saves", f))]
goto_next_day = True
children = 0
child1_name = None
child2_name = None
child3_name = None


def save_variable(var_name, value):
    """Updates a single variable in the save file, preserving the rest."""
    data = {}
    if os.path.exists(save_file):
        with open(save_file, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    data[var_name] = value
    with open(save_file, "w") as file:
        json.dump(data, file, indent=4)


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

def info():
    print("--------------------------------------------------")
    time.sleep(0.05)
    print(f"Day {day}:")
    time.sleep(0.05)
    print(f"Distance traveled: {distance_traveled} miles")
    time.sleep(0.05)
    print(f"Food remaining: {food} units")
    time.sleep(0.05)
    print(f"Health: {health}")
    time.sleep(0.05)
    print(f"Wagon damage: {wagon_damage}")
    time.sleep(0.05)
    print(f"wagon name: {wagon_name}")
    time.sleep(0.05)
    print(f"pioner name: {pioner_name}")
    time.sleep(0.05)
    print(f"Children: {children}")
    print(f"    Child 1: {child1_name}")
    print(f"    Child 2: {child2_name}")
    print(f"    Child 3: {child3_name}")
    time.sleep(0.05)
    if wagon_damage > 0:
        print("you will travel slower because your wagon is damaged")
        time.sleep(0.05)
    print("--------------------------------------------------")


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
input("                    Press Enter to start your journey            ")
print('==================================================================')

print("do you want to resume save game or start fresh")
print("--------------------------------------------------")
print("Available save files:")
print(saves_list)
print("only enter the file name, not the extension")
print("--------------------------------------------------")
print("1. Resume save game")
print("2. Start fresh")

if input() == "1":
    os.rename(f"saves/{input('Enter the name of the save file you want to load: ')}.json", "saves/save.json")
    distance_traveled = get_saved_value("distance_traveled")
    food = get_saved_value("food")
    health = get_saved_value("health")
    wagon_damage = get_saved_value("wagon_damage")
    day = get_saved_value("day")
    wagon_name = get_saved_value("wagon_name")
    pioner_name = get_saved_value("pioner_name")
    alive = get_saved_value("alive")
    children = get_saved_value("children")
    child1_name = get_saved_value("child1_name")
    child2_name = get_saved_value("child2_name")
    child3_name = get_saved_value("child3_name")
    print("Resuming saved game...")
    time.sleep(1)  # Simulate the passage of time
    print(".")
    time.sleep(1)  # Simulate the passage of time
    print(".")
    print("save gave restored")
    info()



else:
    wagon_name = input("Wagon name: ")
    pioner_name = input("Pioner name: ")
    print(
        f"Welcome {pioner_name} to the Oregon Trail! Your wagon is named {wagon_name}. You have {food} units of food and {health} health. Your goal is to travel {distance_needed} miles to reach your destination. Good luck!")



while alive and distance_traveled < distance_needed:
    info()


    if random.randint(0, 10) == 0:
        encounter = random.choice(["bandits", "storm", "sickness"])

        if encounter == "bandits":
            print("You encountered bandits! They stole some of your food and damaged the wagon.")
            if food > 21:
                food -= random.randint(10, 20)
                wagon_damage += random.randint(10, 20)
            else:
                print("You don't have enough food to lose. The bandits hit you instead")
                health -= random.randint(1, 20)
                wagon_damage += random.randint(1, 20)

        elif encounter == "storm":
            playsound("media/sound/storm.mp3")
            print("A storm has hit! You lost some food and your health decreased.")
            food -= random.randint(5, 15)
            health -= random.randint(5, 15)
            wagon_damage += random.randint(5, 15)

        elif encounter == "sickness":
            playsound("media/sound/sic.mp3")
            print("You have fallen ill! Your health has decreased.")
            health -= random.randint(10, 20)

        print(f"After the encounter, you have {food} units of food and {health} health.")
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
                goto_next_day = False

            else:
                playsound("media/sound/traveling.mp3")
                travel_distance = round(random.randint(12, 15) - (wagon_damage / 10))  # miles traveled per day
                distance_traveled += travel_distance
                food -= random.randint(5, 15)  # food consumed per day of travel
                health -= random.randint(1, 10)  # health decreases due to travel
                wagon_damage += random.randint(1, 5)  # wagon damage increases due to travel
                print(f"You traveled {travel_distance} miles.")
                goto_next_day = True

        elif action == "repair":
            wagon_damage -= random.randint(5, 15)
            food -= random.randint(5, 15)
            health -= random.randint(1, 10)
            print(f"You repaired the wagon but lost some food and your health decreases.")
            goto_next_day = False

        elif action == "rest":
            food -= random.randint(5, 10)  # food consumed while resting
            health += random.randint(5, 15)  # health improves while resting
            print("You rested for the day.")
            goto_next_day = True

        elif action == "hunt":
            food_gained = random.randint(15, 25)  # food gained from hunting
            food += food_gained
            health -= random.randint(1, 10)  # health decreases due to hunting effort
            print(f"You hunted and gained {food_gained} units of food.")
            goto_next_day = False

        elif action == "status":
            info()

            goto_next_day = False

        elif action == "exit":
            print("Exiting the game. Goodbye!")
            (save_variable("distance_traveled", distance_traveled))
            print("saved distance traveled")
            time.sleep(0.05)
            (save_variable("food", food))
            print("saved food")
            time.sleep(0.05)
            (save_variable("health", health))
            print("saved health")
            time.sleep(0.05)
            (save_variable("wagon_damage", wagon_damage))
            print("saved wagon_damage")
            time.sleep(0.05)
            (save_variable("day", day))
            print("saved day")
            time.sleep(0.05)
            (save_variable("wagon_name", wagon_name))
            print("saved wagon_name")
            time.sleep(0.05)
            (save_variable("pioner_name", pioner_name))
            print("saved pioner_name")
            time.sleep(0.05)
            (save_variable("alive", alive))
            print("saved alive")
            (save_variable("children", children))
            print("saved children")
            (save_variable("child1_name", child1_name))
            print("saved child1_name")
            (save_variable("child2_name", child2_name))
            print("saved child2_name")
            (save_variable("child3_name", child3_name))
            print("saved child3_name")
            time.sleep(0.05)
            os.rename("saves/save.json", f"saves/{input('Enter the name for your savegame: ')}.json")
            print("saved save")
            raise SystemExit
        else:
            print("Invalid action. Please choose again.")
            goto_next_day = False

        if food <= 0:
            alive = False
            print("You have run out of food and cannot continue. You have died.")

        if health <= 0:
            alive = False
            print("Your health has deteriorated too much. You have died.")

        #
        # add cap's for variables
        #
        if wagon_damage <= 0:
            wagon_damage = 0

        if health >= 100:
            health = 100

        if food >= 100:
            food = 100
    if goto_next_day:

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


print("auto exit in 10 seconds...")
time.sleep(10)


