#todo:
# make wagon breakdowns


import time
import random


wagon_name = None
pioner_name = None
distance_neded = 2170
distance_traveled = 0
food =100
helth = 100
alive = True
day = 0


wagon_name = input("Wagon name: ")
pioner_name = input("Pioner name: ")
print(f"Welcome {pioner_name} to the Oregon Trail! Your wagon is named {wagon_name}. You have {food} units of food and {helth} health. Your goal is to travel {distance_neded} miles to reach your destination. Good luck!")

while alive and distance_traveled < distance_neded:
    print(f"\nDay {day}:")
    print(f"Distance traveled: {distance_traveled} miles")
    print(f"Food remaining: {food} units")
    print(f"Health: {helth}")

    if random.randint(0, 10) == 0:
        encounter = random.choice(["bandits", "storm", "sickness"])

        if encounter == "bandits":
            print("You encountered bandits! They stole some of your food.")
            if food > 21:
                food -= random.randint(10, 20)
            else:
                print("You don't have enough food to lose. The bandits hit you instead")
                helth -= random.randint(1, 20)

        elif encounter == "storm":
            print("A storm has hit! You lost some food and your health decreased.")
            food -= random.randint(5, 15)
            helth -= random.randint(5, 15)

        elif encounter == "sickness":
            print("You have fallen ill! Your health has decreased.")
            helth -= random.randint(10, 20)

        print(f"After the encounter, you have {food} units of food and {helth} health.")
        time.sleep(1)  # Simulate the passage of time
        print(".")
        time.sleep(1)  # Simulate the passage of time
        print(".")

    else:
        action = input("What would you like to do? (travel/rest/hunt/status/quit): ").lower()

        if action == "travel":
            travel_distance = random.randint(12, 15)  # miles traveled per day
            distance_traveled += travel_distance
            food -= random.randint(5, 15)  # food consumed per day of travel
            helth -= random.randint(1, 10)  # health decreases due to travel
            print(f"You traveled {travel_distance} miles.")

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

        elif action == "quit":
            alive = False
            print("You have decided to quit the journey.")

        else:
            print("Invalid action. Please choose again.")

        if food <= 0:
            alive = False
            print("You have run out of food and cannot continue. You have died.")

        if helth <= 0:
            alive = False
            print("Your health has deteriorated too much. You have died.")

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


