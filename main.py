# =====================================================================
# THE OREGON TRAIL (text edition)
# =====================================================================
#
# TODO / ideas for future features:
# - shop/trading post: buy food/spare parts/medicine with a money stat
# - river crossings: ford, caulk & float, or pay a ferry; risk losing supplies
# - weather/seasons: derive month from `day`, slow travel and drain health in winter
# - difficulty settings: adjust starting food/health and encounter frequency
# - random named landmarks: flavor text/ASCII art at distance_traveled milestones
# - better hunting minigame: pick weapon/ammo, add a skill-check instead of flat food_gained


import time
import random
from playsound import playsound
import json
import os


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
health = 100                # player health (0 = dead)
wagon_damage = 0           # wagon damage (higher = worse, slows travel)
alive = True                # main loop keeps running while this is True
day = 0                     # current day count
save_file = "saves/save.json"
goto_next_day = True        # whether the current action should advance the day
mony = 1000                 # money (sic - kept for save-file compatibility)
inventory = {"wood": 0, "water": 0, "axes": 0, "clothing": 0}

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
    """Print the current game status (day, distance, food, health, etc.)."""
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
    print(f"money: {mony}")
    time.sleep(0.05)
    print(inventory)
    time.sleep(0.05)
    if wagon_damage > 0:
        print("you will travel slower because your wagon is damaged")
        time.sleep(0.05)
    print("--------------------------------------------------")


# ---------------------------------------------------------------------
# Intro screen
# ---------------------------------------------------------------------
# Plays a startup sound and prints the wagon ASCII art + title banner.
# The `time.sleep(0.05)` calls between prints give the intro a slow,
# line-by-line "typing" reveal effect.

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
# "THE OREGON" banner (block letters)
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
print('==================================================================')
print('                  A game of grit, grass, and dysentery.           ')
input("                    Press Enter to start your journey            ")
print('==================================================================')


# ---------------------------------------------------------------------
# Start menu: resume a save or start a new game
# ---------------------------------------------------------------------

print("do you want to resume save game or start fresh")
print("--------------------------------------------------")
print("Available save files:")
print(saves_list)
print("only enter the file name, not the extension")
print("--------------------------------------------------")
print("1. Resume save game")
print("2. Start fresh")

if input() == "1":
    # Rename the chosen save file to the "active" save file, then load
    # each variable back out of it into the game state.
    os.rename(f"saves/{input('Enter the name of the save file you want to load: ')}.json", "saves/save.json")
    distance_traveled = get_saved_value("distance_traveled")
    food = get_saved_value("food")
    health = get_saved_value("health")
    wagon_damage = get_saved_value("wagon_damage")
    day = get_saved_value("day")
    wagon_name = get_saved_value("wagon_name")
    pioner_name = get_saved_value("pioner_name")
    alive = get_saved_value("alive")
    mony = get_saved_value("mony")
    inventory = get_saved_value("inventory")

    print("Resuming saved game...")
    time.sleep(1)  # Simulate the passage of time
    print(".")
    time.sleep(1)  # Simulate the passage of time
    print(".")
    print("save gave restored")
    info()

else:
    # Fresh start: ask for names and show the welcome message.
    wagon_name = input("Wagon name: ")
    pioner_name = input("Pioner name: ")
    print(
        f"Welcome {pioner_name} to the Oregon Trail! Your wagon is named {wagon_name}. "
        f"You have {food} units of food and {health} health. Your goal is to travel "
        f"{distance_needed} miles to reach your destination. Good luck!"
    )


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

    # -----------------------------------------------------------------
    # Trading post (~1 in 10 chance per turn)
    # -----------------------------------------------------------------
    if random.randint(0, 10) == 0:

        while True:
            print("You found a trading post! You can buy food, spare parts, medicine, axes, or sell items here.")
            print("1. Buy food (10 units for $50)")
            print("2. Buy spare parts (1 unit for $100)")
            print("3. Buy medicine (1 unit for $75)")
            print("4. Buy axes (1 unit for $200)")
            print("5. Sell items")
            print("6. Leave the trading post")
            choice = input("What would you like to do? (1/2/3/4/5/6): ")

            if choice == "1":
                if mony >= 50:
                    food += 10
                    mony -= 50
                    print("You bought 10 units of food.")
                else:
                    print("You don't have enough money to buy food.")

            elif choice == "2":
                if mony >= 100:
                    wagon_damage -= 10
                    mony -= 100
                    print("You bought spare parts and repaired your wagon.")
                else:
                    print("You don't have enough money to buy spare parts.")

            elif choice == "3":
                if mony >= 75:
                    health += 10
                    mony -= 75
                    print("You bought medicine and improved your health.")
                else:
                    print("You don't have enough money to buy medicine.")

            elif choice == "4":
                if mony >= 200:
                    inventory["axes"] += 1
                    mony -= 200
                    print("You bought an axe.")
                else:
                    print("You don't have enough money to buy an axe.")

            elif choice == "5":
                sell_prices = {"wood": 5, "water": 5, "axes": 100, "clothing": 30}
                print("What do you want to sell?")
                print(inventory)
                print(f"Sell prices (per unit): {sell_prices}")
                item_to_sell = input("Item: ").lower()

                if item_to_sell not in inventory:
                    print("You don't have that item.")
                elif inventory[item_to_sell] <= 0:
                    print(f"You don't have any {item_to_sell} to sell.")
                else:
                    quantity = input(f"How many {item_to_sell} do you want to sell (you have {inventory[item_to_sell]})? ")
                    if not quantity.isdigit() or int(quantity) <= 0:
                        print("Invalid quantity.")
                    else:
                        quantity = int(quantity)
                        if quantity > inventory[item_to_sell]:
                            print(f"You only have {inventory[item_to_sell]} {item_to_sell}.")
                        else:
                            earnings = quantity * sell_prices[item_to_sell]
                            inventory[item_to_sell] -= quantity
                            mony += earnings
                            print(f"You sold {quantity} {item_to_sell} for ${earnings}.")

            elif choice == "6":
                print("You left the trading post.")
                break

    # -----------------------------------------------------------------
    # Player action for this turn
    # -----------------------------------------------------------------
    action = input("What would you like to do? (travel/rest/hunt/status/repair/gather/exit): ").lower()

    if action == "travel":
        if wagon_damage > 50:
            print("Your wagon is too damaged to travel. You need to repair it first.")
            goto_next_day = False
        else:
            playsound("media/sound/traveling.mp3")
            travel_distance = round(random.randint(12, 15) - (wagon_damage / 10))  # miles traveled per day
            distance_traveled += travel_distance
            food -= random.randint(5, 15)          # food consumed per day of travel
            health -= random.randint(1, 10)        # health decreases due to travel
            wagon_damage += random.randint(1, 5)   # wagon damage increases due to travel
            print(f"You traveled {travel_distance} miles.")
            goto_next_day = True

    elif action == "repair":
        if wagon_damage <= 15:
            print("the wagon is to damaged, you must by spare parts at the trading post to repair it")
            goto_next_day = False
        else:
            wagon_damage -= random.randint(5, 15)
            food -= random.randint(5, 15)
            health -= random.randint(1, 10)
            print(f"You repaired the wagon but lost some food and your health decreases.")
            goto_next_day = False

    elif action == "rest":
        food -= random.randint(5, 10)      # food consumed while resting
        health += random.randint(5, 15)    # health improves while resting
        print("You rested for the day.")
        goto_next_day = True

    elif action == "hunt":
        food_gained = random.randint(15, 25)   # food gained from hunting
        food += food_gained
        health -= random.randint(1, 10)        # health decreases due to hunting effort
        print(f"You hunted and gained {food_gained} units of food.")
        goto_next_day = False

    elif action == "status":
        info()
        goto_next_day = False

    elif action == "gather":
        item_to_gather = input("what do you want to gather? (wood)")
        if item_to_gather == "wood":
            if inventory["axes"] >= 1:
                inventory["wood"] += 10
                food -= random.randint(10, 15)
                print("you gatherd 10 wood")
            else:
                print("you nead a axe first")
        goto_next_day = True


    elif action == "exit":
        # Save every piece of game state to the save file, one variable
        # at a time, then rename the save file to whatever name the
        # player chooses before quitting.
        print("Exiting the game. Goodbye!")

        save_variable("distance_traveled", distance_traveled)
        print("saved distance traveled")
        time.sleep(0.05)

        save_variable("food", food)
        print("saved food")
        time.sleep(0.05)

        save_variable("health", health)
        print("saved health")
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

        save_variable("mony", mony)
        print("saved mony")
        time.sleep(0.05)

        save_variable("inventory", inventory)
        print("saved inventory")
        time.sleep(0.05)

        os.rename("saves/save.json", f"saves/{input('Enter the name for your savegame: ')}.json")
        print("saved save")
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
    if health <= 0:
        alive = False
        print("Your health has deteriorated too much. You have died.")

    # -----------------------------------------------------------------
    # Clamp stats to their valid ranges
    # -----------------------------------------------------------------
    if wagon_damage <= 0:
        wagon_damage = 0
    if health >= 100:
        health = 100
    if food >= 100:
        food = 100

    # -----------------------------------------------------------------
    # Advance to the next day (if the chosen action allows it)
    # -----------------------------------------------------------------
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


# ---------------------------------------------------------------------
# Game over
# ---------------------------------------------------------------------
print("auto exit in 10 seconds...")
time.sleep(10)
