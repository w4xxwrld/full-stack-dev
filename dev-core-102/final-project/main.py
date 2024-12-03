import sys
import time
import random
import json

# Globals
user_level = 1.0
inventory = []
game_is_finished = False
save_file = "fisherman_save.json"

# Utility Functions
def typewriter(text, speed=0.035):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def save_game():
    data = {
        "user_level": user_level,
        "inventory": inventory,
        "game_is_finished": game_is_finished
    }
    with open(save_file, "w") as file:
        json.dump(data, file)
    typewriter("Game saved successfully!")

def load_game():
    global user_level, inventory, game_is_finished
    try:
        with open(save_file, "r") as file:
            data = json.load(file)
            user_level = data["user_level"]
            inventory = data["inventory"]
            game_is_finished = data["game_is_finished"]
        typewriter("Game loaded successfully!")
    except FileNotFoundError:
        typewriter("No save file found. Starting a new game.")

# Inventory System
def remove_from_inventory(item):
    if item in inventory:
        inventory.remove(item)
        typewriter(f"{item} removed from your inventory.")
    else:
        typewriter(f"{item} is not in your inventory.")

def add_to_inventory(item):
    if len(inventory) < 10:
        inventory.append(item)
        typewriter(f"{item} added to inventory.")
    else:
        typewriter("Inventory full! Remove something first.")
        typewriter(f"Your inventory: {', '.join(inventory)}")
        item_to_delete = input("Choose item to remove: ").capitalize()
        remove_from_inventory(item_to_delete)

# Fishing Mechanic
def fish():
    outcomes = [
        "Caught a small fish!",
        "Caught a big fish!",
        "Lost your bait.",
        "Nothing bit today."
    ]
    result = random.choice(outcomes)
    typewriter(f"You cast your line... {result}")
    if "small" in result:
        add_to_inventory("small fish")
    elif "big" in result:
        add_to_inventory("big fish")
    elif "bait" in result:
        remove_from_inventory("Bait")

# Discover City
def discover_city():
    typewriter("You explore the city.")
    typewriter("Choose an activity:\n1. Visit Shop\n2. Walk Around")
    choice = input("Enter your choice (1-2): ")
    if choice == "1":
        shop()
    elif choice == "2":
        random_city_event()

def shop():
    items = ["Bait", "Fishing Rod", "Net"]
    typewriter(f"Items available: {', '.join(items)}")
    while True:
        item = input("What would you like to buy? ").capitalize()
        if item in items:
            add_to_inventory(item)
            break
        else:
            typewriter("Invalid item. Please enter a valid item from the list.")

def random_city_event():
    events = [
        "You meet an old sailor who shares fishing tips.",
        "A pickpocket steals an item from your inventory!",
        "You find a rare fishing lure on the street."
    ]
    event = random.choice(events)
    typewriter(f"City Event: {event}")
    if "steals" in event:
        if inventory:
            lost_item = random.choice(inventory)
            remove_from_inventory(lost_item)
    elif "rare fishing lure" in event:
        add_to_inventory("Rare Fishing Lure")

# Plot Paths
def ocean_exploration():
    global user_level
    typewriter("You explore the mysterious depths of the ocean.")
    if random.random() < 1:  # 10% probability to find a treasure map
        typewriter("You find a treasure map!")
        if inventory:
            typewriter("You can use this map to go on a treasure hunt, but it will cost all your items.")
        add_to_inventory("Treasure Map")
    else:
        typewriter("You find some rare and large ocean fish!")
        add_to_inventory("Large Ocean Fish")
        user_level += 0.2

def treasure_hunt():
    global game_is_finished
    if "Treasure Map" not in inventory:
        typewriter("You don't have a treasure map. Explore more to find one!")
        return

    if not inventory or (len(inventory) == 1 and "Treasure Map" in inventory):
        typewriter("You don't have enough items to embark on the treasure hunt. Go fishing and try again!")
        return

    typewriter("You decide to use the treasure map and embark on the ultimate treasure hunt!")
    typewriter("This will cost all items in your inventory. Proceed? (y/n)")
    if input().lower() != "y":
        typewriter("You decide to keep the treasure map for now.")
        return

    # Remove all items, including the treasure map
    if random.random() < 0.8:  # 80% success probability
        typewriter("After a thrilling adventure, you find the legendary treasure! You are now a legend!")
        inventory.clear()
        game_is_finished = True
    else:
        typewriter("The treasure eludes you this time. Better luck next time!")

def choose_plot_path():
    typewriter("Choose your adventure:\n1. Fishing Tournament\n2. Trading Travel\n3. Fishing in River\n4. Fishing in Lake\n5. Fishing in Sea\n6. Fishing in Ocean (Level 5 required)")
    if "Treasure Map" in inventory:
        typewriter("7. Treasure Hunt")

    choice = input("Enter your choice (1-6): ")
    if choice == "1":
        fishing_tournament()
    elif choice == "2":
        start_business()
    elif choice == "3":
        fishing_adventure("River", 2)
    elif choice == "4":
        fishing_adventure("Lake", 4)
    elif choice == "5":
        fishing_adventure("Sea", 6)
    elif choice == "6":
        if user_level >= 5:
            typewriter("Would you like to fish or explore the ocean?\n1. Fish\n2. Explore")
            ocean_choice = input("Enter your choice (1-2): ")
            if ocean_choice == "1":
                fishing_adventure("Ocean", 8)
            elif ocean_choice == "2":
                ocean_exploration()
            else:
                typewriter("Invalid choice.")
        else:
            typewriter("You need to be level 5 to explore the ocean!")
    elif choice == "7" and "Treasure Map" in inventory:
        treasure_hunt()
    else:
        typewriter("Invalid choice. Returning to the main menu.")

def fishing_adventure(location, difficulty):
    global user_level
    typewriter(f"You head to the {location}.")
    outcome = random.choices(["Success", "Failure"], weights=[10 - difficulty, difficulty])[0]
    if outcome == "Success":
        typewriter(f"You catch a lot of fish at the {location}!")
        add_to_inventory(f"{location} Fish")
        user_level += 0.1
    else:
        typewriter(f"The fishing trip to the {location} was unproductive.")

def fishing_tournament():
    global user_level
    typewriter("You enter the fishing tournament.")
    baits_left = 5
    while baits_left > 0:
        result = fish()
        baits_left -= 1
        if result == "Lost your bait.":
            typewriter(f"Baits left: {baits_left}")
    if baits_left == 0:
        typewriter("You used all your bait and won the tournament!")
        add_to_inventory("Golden Fishing Rod")
        user_level += 0.1
    else:
        typewriter("You ran out of bait and lost the tournament.")

def start_business():
    global user_level
    cities = ["Harbour City", "Fishrod City", "Saltlake City", "New Fish City"]
    typewriter(f"Choose a city to trade in:\n1. {cities[0]}\n2. {cities[1]}\n3. {cities[2]}\n4. {cities[3]}")
    choice = int(input("Enter your choice (1-4): "))
    city = cities[choice - 1]
    difficulty = choice * 2
    outcome = random.choices(["Success", "Buyer Declines"], weights=[10 - difficulty, difficulty])[0]
    if outcome == "Success":
        typewriter(f"You successfully traded in {city}.")
        add_to_inventory("Profit")
        user_level += 0.2
    else:
        typewriter(f"The buyer in {city} declined the deal.")

# Main Loop
def main():
    global user_level
    typewriter("Welcome to Fisherman's Adventure!")
    typewriter("Would you like to load a saved game? (y/n)")
    if input().lower() == "y":
        load_game()
    else:
        typewriter("Starting a new adventure!")

    while not game_is_finished:
        typewriter("\nWhat would you like to do?\n1. Go Fishing\n2. Discover City\n3. Check Inventory\n4. Choose Plot Path\n5. Save Game")
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            fish()
        elif choice == "2":
            discover_city()
        elif choice == "3":
            if len(inventory) == 0:
                typewriter(f"Your inventory is empty :(")
            else:
                typewriter(f"Your inventory: {', '.join(inventory)}")
        elif choice == "4":
            choose_plot_path()
        elif choice == "5":
            save_game()
        else:
            typewriter("Invalid choice.")

    typewriter("Congratulations! You've completed the adventure!")
    save_game()
if __name__ == "__main__":
    main()