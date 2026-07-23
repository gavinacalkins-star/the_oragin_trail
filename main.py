# =====================================================================
# THE OREGON TRAIL (text edition)
# =====================================================================
#
# TODO / ideas for future features:
#  river crossings: ford, caulk & float, or pay a ferry; risk losing supplies
#  weather/seasons: derive month from `day`, slow travel and drain stamina in winter
#  random named landmarks: flavor text/ASCII art at distance_traveled milestones
#  better hunting minigame: pick weapon/ammo, add a skill-check instead of flat food_gained

version_hear = "1.2.6"

import time
import random
from playsound import playsound
import json
import os
import msvcrt
import sys, requests
import webbrowser
from colorama import Fore, Style



try:
    remote = requests.get(
        "https://raw.githubusercontent.com/gavinacalkins-star/the_oragin_trail/master/VERSION",
        timeout=5
    ).text.strip()
    if remote != version_hear:
        print("Out of date — please update.")
        input("Press ENTER to download, if the file is marked as suspicious, click allow download")
        print(Fore.RED + "once downloaded, extract the zip and run the new version")
        print("select download dangores file and open the zip archive.")
        print("once open run the_oregon_trail.exe, select extract all and then extract")
        print("in the downloaded folder run the_oregon_trail.exe file and if windows says they protected yore pc click more opshons and then run anyway.")
        webbrowser.open_new_tab("https://gitfolderdownloader.github.io/?=https://github.com/gavinacalkins-star/the_oragin_trail/tree/master/dist")
        sys.exit("Out of date — please update.")
except requests.RequestException:
    pass


# ---------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------
# These are the "live" values that change as the player plays. They get
# written out to `save_file` when the player exits, and read back in
# when a save is resumed (see the save/load section below).

wagon_name = None          # name of the player's wagon, set at game start
pioner_name = None         # name of the player character (sic - kept for save-file compatibility)
distance_needed = 2170     # total miles to travel to "win" the game
distance_traveled = 0       # miles traveled so far
food = 100                 # food supply (units)
stamina = 100                # player stamina (0 = dead)
wagon_damage = 0           # wagon damage (higher = worse, slows travel)
alive = True                # main loop keeps running while this is True
day = 0                     # current day count
save_file = "saves/save.json"
goto_next_day = True        # whether the current action should advance the day
money = 1000                 # money (sic - kept for save-file compatibility)
inventory = {"wood": 0, "water": 0, "axes": 0, "clothing": 0}
difficulty = None
travel_max = None
travel_min = None
repair_max = None
repair_min = None
stamina_per_hunt_max = None
stamina_per_hunt_min = None
food_per_hunt_max = None
food_per_hunt_min = None
thirst = 0
health = 100
newday = True

os.makedirs("saves", exist_ok=True)

# List existing save files so the player can choose one to resume.
saves_list = [f for f in os.listdir("saves") if os.path.isfile(os.path.join("saves", f))]


# ---------------------------------------------------------------------
# Save / load helpers
# ---------------------------------------------------------------------
# Saves are stored as a single JSON dict in `save_file`. Each call to
# `save_variable` reads whatever is already there, updates one key, and
# writes the whole dict back out - so multiple variables can be saved
# one at a time without clobbering each other.

def save_variable(var_name, value):
    """Update a single variable in the save file, preserving the rest."""
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
    """Retrieve a single variable's value from the save file, or None if missing."""
    if not os.path.exists(save_file):
        return None

    with open(save_file, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return None

    return data.get(var_name, None)


def info():
    """Print the current game status (day, distance, food, stamina, etc.)."""
    print("--------------------------------------------------")
    time.sleep(0.05)
    print(f"Day {day}:")
    print("--------------------------------------------------")
    time.sleep(0.05)
    print(f"Distance traveled: {distance_traveled} miles")
    time.sleep(0.05)
    print(f"Distance remaining: {distance_needed - distance_traveled} miles")
    time.sleep(0.05)
    print(f"you are {round((distance_traveled / distance_needed) * 100 , 2)}% of the way to oregon")
    time.sleep(0.05)
    print("--------------------------------------------------")
    if food <= 20:
        print(Fore.RED + f"Food remaining: {food} units")
    else:
        print(Fore.WHITE + f"Food remaining: {food} units")
    time.sleep(0.05)
    if stamina <= 20:
        print(Fore.RED + f"stamina: {stamina}")
    else:
        print(Fore.WHITE + f"stamina: {stamina}")
    if health <= 20:
        print(Fore.RED + f"health: {health}")
    else:
        print(Fore.WHITE + f"health: {health}")

    time.sleep(0.05)
    if thirst >= 20:
        print(Fore.RED + f"Thirst: {thirst}")
    else:
        print(Fore.WHITE + f"Thirst: {thirst}")

    time.sleep(0.05)
    print(Fore.WHITE + "--------------------------------------------------")
    if wagon_damage > 10:
        print(Fore.RED + f"Wagon damage: {wagon_damage}")
    else:
        print(Fore.WHITE + f"Wagon damage: {wagon_damage}")
    time.sleep(0.05)
    print(Fore.WHITE + f"wagon name: {wagon_name}")
    time.sleep(0.05)
    print(f"pioner name: {pioner_name}")
    time.sleep(0.05)
    print("--------------------------------------------------")
    if money < 200:
        print(Fore.RED + f"money: {money}")
    else:
        print(Fore.WHITE + f"money: {money}")
    time.sleep(0.05)
    print(Fore.WHITE + f"inventory: {inventory}")
    time.sleep(0.05)
    print("--------------------------------------------------")
    print(f"Difficulty: {difficulty}")
    time.sleep(0.05)

    if wagon_damage > 0:
        print(Fore.RED + "you will travel slower because your wagon is damaged")
        time.sleep(0.05)
    print(Fore.WHITE + "--------------------------------------------------")


def hunt_minigame(speed=0.05, tolerance=0):
    """
    speed: seconds between each number update (lower = faster/harder)
    tolerance: how close to 0 counts as a hit (0 = must be exact)
    """
    value = -15
    direction = 1  # 1 = counting up, -1 = counting down

    print("Press ENTER when the number hits 0!")
    time.sleep(1)  # short pause so the player can get ready

    while True:
        # show the current number, overwriting the same line
        print(f"\r{value:>4}", end="", flush=True)

        # check if a key was pressed WITHOUT blocking the loop
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b"\r":  # Enter key
                print()  # move to a new line after the game ends
                return abs(value) <= tolerance

        time.sleep(speed)

        # move the number and flip direction at the ends
        value += direction
        if value >= 15 or value <= -15:
            direction *= -1


def save_all():
    save_variable("distance_traveled", distance_traveled)
    print("saved distance traveled")
    time.sleep(0.05)

    save_variable("food", food)
    print("saved food")
    time.sleep(0.05)

    save_variable("stamina", stamina)
    print("saved stamina")
    time.sleep(0.05)

    save_variable("wagon_damage", wagon_damage)
    print("saved wagon_damage")
    time.sleep(0.05)

    save_variable("day", day)
    print("saved day")
    time.sleep(0.05)

    save_variable("wagon_name", wagon_name)
    print("saved wagon_name")
    time.sleep(0.05)

    save_variable("pioner_name", pioner_name)
    print("saved pioner_name")
    time.sleep(0.05)

    save_variable("alive", alive)
    print("saved alive")
    time.sleep(0.05)

    save_variable("money", money)
    print("saved money")
    time.sleep(0.05)

    save_variable("inventory", inventory)
    print("saved inventory")
    time.sleep(0.05)

    save_variable("difficulty", difficulty)
    print("saved difficulty")
    time.sleep(0.05)

    save_variable("travel_min", travel_min)
    save_variable("travel_max", travel_max)
    save_variable("repair_min", repair_min)
    save_variable("repair_max", repair_max)
    save_variable("food_per_hunt_min", food_per_hunt_min)
    save_variable("food_per_hunt_max", food_per_hunt_max)
    save_variable("stamina_per_hunt_min", stamina_per_hunt_min)
    save_variable("stamina_per_hunt_max", stamina_per_hunt_max)
    save_variable("health", health)
    print("saved difficulty settings")


def load_all():

    global distance_traveled, food, stamina, wagon_damage, day, wagon_name, pioner_name, alive, money, inventory, difficulty, health
    global travel_min, travel_max, repair_min, repair_max, food_per_hunt_min, food_per_hunt_max, stamina_per_hunt_min, stamina_per_hunt_max

    distance_traveled = get_saved_value("distance_traveled")
    food = get_saved_value("food")
    stamina = get_saved_value("stamina")
    wagon_damage = get_saved_value("wagon_damage")
    day = get_saved_value("day")
    wagon_name = get_saved_value("wagon_name")
    pioner_name = get_saved_value("pioner_name")
    alive = get_saved_value("alive")
    health = get_saved_value("health")
    money = get_saved_value("money")
    inventory = get_saved_value("inventory")
    difficulty = get_saved_value("difficulty")
    travel_min = get_saved_value("travel_min")
    travel_max = get_saved_value("travel_max")
    repair_min = get_saved_value("repair_min")
    repair_max = get_saved_value("repair_max")
    food_per_hunt_min = get_saved_value("food_per_hunt_min")
    food_per_hunt_max = get_saved_value("food_per_hunt_max")
    stamina_per_hunt_min = get_saved_value("stamina_per_hunt_min")
    stamina_per_hunt_max = get_saved_value("stamina_per_hunt_max")


# ---------------------------------------------------------------------
# Intro screen
# ---------------------------------------------------------------------
# Plays a startup sound and prints the wagon ASCII art + title banner.
# The `time.sleep(0.05)` calls between prints give the intro a slow,
# line-by-line "typing" reveal effect.
print("made by Gavin c")
print("version: " + str(version_hear))
playsound("media/sound/game start.mp3")

print(Style.DIM + Fore.YELLOW + Style.BRIGHT + '                        _.--.')
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

print(Fore.RESET + Style.RESET_ALL + Fore.WHITE+ '==================================================================')
time.sleep(0.05)
# "THE OREGON" banner (block letters)
print(Fore.GREEN + '#   # ##### #      ####  ###  #   # #####       #####  ###  ')
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
# "TRAIL" banner (block letters, continued)
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
print(Fore.WHITE + '==================================================================')
print('                  A game of grit, grass, and dysentery.           ')
input("                    Press Enter to start your journey            ")
print('==================================================================')


# ---------------------------------------------------------------------
# Start menu: resume a save or start a new game
# ---------------------------------------------------------------------

print(Fore.YELLOW + "do you want to resume save game or start fresh")
print(Fore.WHITE + "--------------------------------------------------")
print("Available save files:")
print(Fore.YELLOW + str(saves_list))
print(Fore.WHITE + "only enter the file name, not the extension")
print("--------------------------------------------------")
print("1. Resume save game")
print("2. Start fresh")

if input() == "1":
    # Rename the chosen save file to the "active" save file, then load
    # each variable back out of it into the game state.
    os.replace(f"saves/{input('Enter the name of the save file you want to load: ')}.json", "saves/save.json")

    load_all()


    print("Resuming saved game...")
    time.sleep(1)  # Simulate the passage of time
    print(Fore.RED + ".")
    time.sleep(1)  # Simulate the passage of time
    print(Fore.RED + ".")
    print(Fore.WHITE + "save gave restored")
    info()

else:
    # Fresh start: ask for names and show the welcome message.
    wagon_name = input(Fore.YELLOW + "Wagon name: ")
    pioner_name = input("Pioner name: ")
    difficulty = input("Difficulty, 1,2,3: ")

    if difficulty == "1":
        travel_min = 15
        travel_max = 18
        repair_min = 10
        repair_max = 20
        food_per_hunt_min = 20
        food_per_hunt_max = 30
        stamina_per_hunt_min = 1
        stamina_per_hunt_max = 5

    elif difficulty == "2":
        travel_min = 12
        travel_max = 15
        repair_min = 5
        repair_max = 15
        food_per_hunt_min = 15
        food_per_hunt_max = 25
        stamina_per_hunt_min = 1
        stamina_per_hunt_max = 10

    elif difficulty == "3":
        travel_min = 9
        travel_max = 12
        repair_min = 2
        repair_max = 8
        food_per_hunt_min = 10
        food_per_hunt_max = 18
        stamina_per_hunt_min = 5
        stamina_per_hunt_max = 15

    print(Fore.RED +
        f"Welcome {pioner_name} to the Oregon Trail! Your wagon is named {wagon_name}. "
        f"You have {food} units of food and {stamina} stamina. Your goal is to travel "
        f"{distance_needed} miles to reach your destination. Good luck!"
    )
    print(Fore.WHITE)


# =====================================================================
# Main game loop
# =====================================================================
# Each iteration of this loop represents one "turn". A turn may or may
# not advance the day counter, depending on which action the player
# picks (`goto_next_day` controls that). The loop keeps running until
# the player dies (`alive` becomes False) or reaches the destination
# (`distance_traveled >= distance_needed`).

while alive and distance_traveled < distance_needed:
    info()

    # -----------------------------------------------------------------
    # Random encounters (~1 in 11 chance per turn)
    # -----------------------------------------------------------------
    if random.randint(0, 10) == 0:
        encounter = random.choice(["bandits", "storm", "sickness"])

        if encounter == "bandits":
            print(Fore.RED + "You encountered bandits! They stole some of your food and damaged the wagon.")
            if food > 21:
                food -= random.randint(10, 20)
                wagon_damage += random.randint(10, 20)
            else:
                print(Fore.RED + "You don't have enough food to lose. The bandits hit you instead")
                health -= random.randint(1, 20)
                wagon_damage += random.randint(1, 20)

        elif encounter == "storm":
            print(Fore.RED + "A storm has hit! You lost some food and your stamina decreased.")
            playsound("media/sound/storm.mp3")
            food -= random.randint(5, 15)
            stamina -= random.randint(5, 15)
            wagon_damage += random.randint(5, 15)

        elif encounter == "sickness":
            print(Fore.RED + "You have fallen ill! Your health has decreased.")
            health -= random.randint(10, 20)

        print(Fore.YELLOW + f"After the encounter, you have {food} units of food and {stamina} stamina.")
        input(Fore.WHITE + "Press Enter to continue...")
        time.sleep(1)  # Simulate the passage of time
        print(".")
        time.sleep(1)  # Simulate the passage of time
        print(".")

    # -----------------------------------------------------------------
    # Trading post (~1 in 15 chance per turn)
    # -----------------------------------------------------------------
    if newday:
        if random.randint(0, 15) == 0:

            while True:
                time.sleep(0.5)  # Simulate the passage of time
                print(Fore.WHITE + ".")
                time.sleep(0.5)  # Simulate the passage of time
                print(".")
                print("You found a trading post! You can buy food, spare parts, medicine, axes, or sell items here.")
                time.sleep(0.05)
                print("1. Buy food (10 units for $50)")
                time.sleep(0.05)
                print("2. Buy spare parts (1 unit for $100)")
                time.sleep(0.05)
                print("3. Buy medicine (1 unit for $75)")
                time.sleep(0.05)
                print("4. Buy axes (1 unit for $200)")
                time.sleep(0.05)
                print("5. Sell items")
                time.sleep(0.05)
                print("6. Leave the trading post")
                time.sleep(0.05)
                choice = input("What would you like to do? (1/2/3/4/5/6): ")

                if choice == "1":
                    if money >= 50:
                        food += 10
                        money -= 50
                        print(Fore.GREEN + "You bought 10 units of food.")
                    else:
                        print(Fore.RED + "You don't have enough money to buy food.")

                elif choice == "2":
                    if money >= 100:
                        wagon_damage -= 10
                        money -= 100
                        print(Fore.GREEN + "You bought spare parts and repaired your wagon.")
                    else:
                        print(Fore.RED + "You don't have enough money to buy spare parts.")

                elif choice == "3":
                    if money >= 75:
                        health += 10
                        money -= 75
                        print(Fore.GREEN + "You bought medicine and improved your health.")
                    else:
                        print(Fore.RED + "You don't have enough money to buy medicine.")

                elif choice == "4":
                    if money >= 200:
                        inventory["axes"] += 1
                        money -= 200
                        print(Fore.GREEN + "You bought an axe.")
                    else:
                        print(Fore.RED + "You don't have enough money to buy an axe.")

                elif choice == "5":
                    sell_prices = {"wood": 5, "water": 5, "axes": 100, "clothing": 30}
                    print("What do you want to sell?")
                    print(inventory)
                    print(f"Sell prices (per unit): {sell_prices}")
                    item_to_sell = input("Item: ").lower()

                    if item_to_sell not in inventory:
                        print(Fore.RED + "You don't have that item.")
                    elif inventory[item_to_sell] <= 0:
                        print(Fore.RED + f"You don't have any {item_to_sell} to sell.")
                    else:
                        quantity = input(f"How many {item_to_sell} do you want to sell (you have {inventory[item_to_sell]})? ")
                        if not quantity.isdigit() or int(quantity) <= 0:
                            print(Fore.RED + "Invalid quantity.")
                        else:
                            quantity = int(quantity)
                            if quantity > inventory[item_to_sell]:
                                print(Fore.RED + f"You only have {inventory[item_to_sell]} {item_to_sell}.")
                            else:
                                earnings = quantity * sell_prices[item_to_sell]
                                inventory[item_to_sell] -= quantity
                                money += earnings
                                print(Fore.RED + f"You sold {quantity} {item_to_sell} for ${earnings}.")

                elif choice == "6":
                    print(Fore.WHITE + "You left the trading post.")
                    print(".")
                    print(".")
                    print(".")
                    break

    # -----------------------------------------------------------------
    # Player action for this turn
    # -----------------------------------------------------------------
    action = input("What would you like to do? (travel/rest/hunt/status/repair/gather/drink/exit): ").lower()

    if action == "travel":
        if stamina < 30:
            print(Fore.RED + "You are too exhausted to travel, you must rest first.")
            print(Fore.WHITE)
        else:
            if wagon_damage > 50:
                print("Your wagon is too damaged to travel. You need to repair it first.")
                goto_next_day = False
            else:

                playsound("media/sound/traveling.mp3")
                travel_distance = round(random.randint(travel_min, travel_max) - (wagon_damage / 10))  # miles traveled per day
                distance_traveled += travel_distance
                food -= random.randint(5, 15)          # food consumed per day of travel
                stamina -= random.randint(1, 10)        # stamina decreases due to travel
                wagon_damage += random.randint(1, 5)   # wagon damage increases due to travel
                print(f"You traveled {travel_distance} miles.")
                goto_next_day = True

    elif action == "repair":
        if stamina <= 50:
            print(Fore.RED + "You are too exhausted to repair, you must rest first")
            print(Fore.WHITE)
        else:
            if wagon_damage >= 15:
                print(Fore.RED + "The wagon is too damaged, you must buy spare parts at the trading post to repair it")
                print(Fore.WHITE)
                goto_next_day = False
            else:
                wagon_damage -= random.randint(repair_min, repair_max)
                food -= random.randint(5, 15)
                stamina -= random.randint(1, 10)
                print(f"You repaired the wagon but lost some food and your stamina decreases.")
                goto_next_day = False

    elif action == "rest":
        food -= random.randint(5, 10)      # food consumed while resting
        stamina += random.randint(5, 15)    # health improves while resting
        print("You rested for the day.")
        goto_next_day = True

    elif action == "hunt":
        if stamina <= 20:
            print(Fore.RED + "You are too exhausted to hunt. You must rest first.")
            print(Fore.WHITE)
            goto_next_day = False
        else:
            if hunt_minigame(0.3 , 0):
                print("You hit the animal!")
                food_gained = random.randint(food_per_hunt_min, food_per_hunt_max)   # food gained from hunting
                food += food_gained
                stamina -= random.randint(stamina_per_hunt_min, stamina_per_hunt_max)        # stamina decreases due to hunting effort
                print(f"You hunted and gained {food_gained} units of food.")
                goto_next_day = False
            else:
                print("You missed the animal.")
                food -= random.randint(5, 10)          # food consumed while hunting
                stamina -= random.randint(1, 10)        # stamina decreases due to hunting effort
                goto_next_day = False
    elif action == "status":
        info()
        goto_next_day = False

    elif action == "gather":
        if stamina <= 20:
            print(Fore.RED + "You are too exhausted to gather, you must rest first.")
            print(Fore.WHITE)
        else:
            item_to_gather = input("what do you want to gather? (wood, water)")
            if item_to_gather == "wood":
                if inventory["axes"] >= 1:
                    inventory["wood"] += 10
                    food -= random.randint(10, 15)
                    stamina -= random.randint(1, 10)
                    print(Fore.GREEN + "you gathered 10 wood")
                    print(Fore.WHITE)
                else:
                    print(Fore.RED + "you need a axe first")
                    print(Fore.WHITE)

            elif item_to_gather == "water":
                if random.random() > 0.5:
                    inventory["water"] += 10
                    food -= random.randint(10, 15)
                    stamina -= random.randint(1, 10)
                    print(Fore.GREEN + "you gathered 10 water")
                    print(Fore.WHITE)

                else:
                    print(Fore.RED + "there is no water to gather")
                    print(Fore.WHITE)
                goto_next_day = True

    elif action == "drink":
        if inventory["water"] >= 1:
            inventory["water"] -= 1
            thirst -= 20
            print("you drank some water")
        else:
            print("you have no water to drink")
        goto_next_day = False


    elif action == "exit":
        # Save every piece of game state to the save file, one variable
        # at a time, then rename the save file to whatever name the
        # player chooses before quitting.
        print("Exiting the game. Goodbye!")

        save_all()

        os.replace("saves/save.json", f"saves/{input('Enter the name for your savegame: ')}.json")
        print("saved save")
        raise SystemExit

    elif action == "debug":
        if input("enter debug password") == "gavinacalkinsstar1590":
            var_name = input("variable to set: ")

            value = input("value: ")

            globals()[var_name] = eval(value)
        else:
            print(Fore.RED + "Invalid debug password.")
            print(Fore.WHITE)
            time.sleep(2)
            raise SystemExit

    else:
        print("Invalid action. Please choose again.")
        goto_next_day = False

    # -----------------------------------------------------------------
    # Death checks
    # -----------------------------------------------------------------
    if food <= 0:
        alive = False
        print("You have run out of food and cannot continue. You have died.")
    if thirst > 100:
        alive = False
        print("You have died of dehydration.")
    if health <= 0:
        alive = False
        print("You have died of low health.")
    # -----------------------------------------------------------------
    # Clamp stats to their valid ranges
    # -----------------------------------------------------------------
    if wagon_damage <= 0:
        wagon_damage = 0
    if stamina >= 100:
        stamina = 100
    if food >= 100:
        food = 100
    if stamina <= 0:
        stamina = 0
    if wagon_damage <= 0:
        wagon_damage = 0
    if health <= 0:
        health = 0
    if thirst <= 0:
        thirst = 0

    # -----------------------------------------------------------------
    # Advance to the next day (if the chosen action allows it)
    # -----------------------------------------------------------------
    if goto_next_day:
        newday = True
        day += 1
        thirst += 5
        time.sleep(1)  # Simulate the passage of time
        print(".")
        time.sleep(1)  # Simulate the passage of time
        print(".")
        time.sleep(1)  # Simulate the passage of time
        print(".")
        time.sleep(1)  # Simulate the passage of time
        print(".")
        time.sleep(1)  # Simulate the passage of time
    else:
        newday = False


# ---------------------------------------------------------------------
# Game over
# ---------------------------------------------------------------------
print("auto exit in 10 seconds...")
time.sleep(10)
