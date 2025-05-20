import os
import random
import msvcrt
import time
import json
from cryptography.fernet import Fernet

ENCRYPTION_KEY = b'uP4u1U_RzJtX2xY6vQwA5iNl9fGk0cHj7bM8zO7dS1s='
cipher_suite = Fernet(ENCRYPTION_KEY)
SAVE_FILE_NAME = "savegame.dat"

is_hardcore_mode = False
is_defense_potion_active = False
is_strength_potion_active = False

stall_first_visit = {
    "alice": True,
    "unknown": True,
    "aaron": True
}

player_health = 100
player_max_health = 100
player_max_attack = 20
player_min_attack = 5
player_defense = 0
player_gold = 50
player_xp = 0
player_skill_points = 0
player_xp_to_level_up = 100
player_level = 0
player_crit_bonus_multiplier = 0.1
player_gold_bonus_multiplier = 0.0
player_xp_bonus_multiplier = 0.0

player_perks = {
    "shop_discount": 0,
    "menu_heal": 0
}
can_use_menu_heal = False
first_kill_jackpot_awarded = {}

POTION_HEAL_AMOUNT = 30
POTION_DEFENSE_BOOST = 5
POTION_STRENGTH_BOOST = 5

player_potions_inventory = {
    'healing': 1,
    'defense': 1,
    'strength': 1
}

total_fights_won = 0
potions_used_this_turn = 0

stall_item_stocks = {
    'alice': 5,
    'unknown': 5,
    'aaron': 5
}

ITEM_DISPLAY_NAMES = {
    "healing": "Healing Potion", "defense": "Defense Potion", "strength": "Strength Potion",
    "heavy_armor": "Heavy Armor", "medium_armor": "Medium Armor", "light_armor": "Light Armor",
    "short_sword": "Short Sword", "long_sword": "Long Sword", "great_sword": "Great Sword",
    "player_max_health": "Max Health", "player_gold_bonus_multiplier": "Gold Multiplier",
    "player_xp_bonus_multiplier": "XP Multiplier",
    "player_max_attack": "Max Damage Dealt", "player_min_attack": "Min Damage Dealt",
    "player_crit_bonus_multiplier": "Critical Hit Multiplier"
}

DIALOGS = {
    'alice': {'hello': ['Alice: Hi, do you want anything?', 'Alice: Hey! What do you want to buy?'],
              'bye': ['Alice: See you next time!', 'Alice: Bye Bye!', 'Alice: Goodbye!'],
              'thanks': ['Alice: Thanks for buying!', 'Alice: Anything else?']},
    'unknown': {'hello': ['Unknown: ...You seek something?', 'Unknown: The shadows whisper... what do you desire?',
                          'Unknown: You have summoned me. Speak.'],
                'bye': ['Unknown: Fading into the void...', 'Unknown: You leave, but the darkness remains.',
                        'Unknown: Until next time, wanderer.'],
                'thanks': ['Unknown: The pact is sealed.', 'Unknown: Gratitude is a fleeting shadow.',
                           'Unknown: It is done. Will there be more?']},
    'aaron': {'hello': ['Aaron: Yo, what’s up? Need something?', 'Aaron: Hey there! What can I get you?',
                        'Aaron: Sup! You looking for something?'],
              'bye': ['Aaron: Catch you later!', 'Aaron: See ya, man!', 'Aaron: Peace out!'],
              'thanks': ['Aaron: Thanks, buddy!', 'Aaron: Appreciate it! Need anything else?',
                         'Aaron: Cool, thanks! Let me know if you want more.']}
}

SHOP_ITEMS_DATA = {
    'alice': {'name': "Alice's Potion Stall", 'category': 'potions', 'stock_type': 'potions',
              'items': {'healing': {'id': '1', 'price': 30, 'name_key': 'healing'},
                        'defense': {'id': '2', 'price': 40, 'name_key': 'defense'},
                        'strength': {'id': '3', 'price': 50, 'name_key': 'strength'}},
              'first_visit_dialog': ["Alice: Hey! Welcome to my little stall.", "Alice: Sooo... Do you want anything?"],
              'out_of_stock_dialog': "Alice: I'm sorry... I am out of potions."},
    'aaron': {'name': "Aaron's Sword Stall", 'category': 'swords', 'stock_type': 'swords',
              'items': {'short_sword': {'id': '1', 'price': 50, 'damage_increase': (1, 3), 'name_key': 'short_sword'},
                        'long_sword': {'id': '2', 'price': 100, 'damage_increase': (2, 5), 'name_key': 'long_sword'},
                        'great_sword': {'id': '3', 'price': 150, 'damage_increase': (3, 7), 'name_key': 'great_sword'}},
              'first_visit_dialog': ["Aaron: Greetings, adventurer. Looking for a new blade?"],
              'out_of_stock_dialog': "Aaron: Sorry, I am out of swords."},
    'unknown': {'name': "The Unknown's Armor Stall", 'category': 'armor', 'stock_type': 'armor',
                'items': {'light_armor': {'id': '1', 'price': 60, 'defense_increase': 5, 'name_key': 'light_armor'},
                          'medium_armor': {'id': '2', 'price': 120, 'defense_increase': 10, 'name_key': 'medium_armor'},
                          'heavy_armor': {'id': '3', 'price': 180, 'defense_increase': 15, 'name_key': 'heavy_armor'}},
                'first_visit_dialog': ["Unknown: ... Arm yourself.", "Unknown: ... Protect yourself."],
                'out_of_stock_dialog': "Unknown: ... Out of stock."}
}

ENEMY_TEMPLATES = [
    {'name': 'Wolf', 'hp': 30, 'attack': 10, 'gold': 15, 'xp': 25},
    {'name': 'Mini-Goblin', 'hp': 50, 'attack': 15, 'gold': 30, 'xp': 40},
    {'name': 'Giant Spider', 'hp': 80, 'attack': 18, 'gold': 45, 'xp': 55},
    {'name': 'Goblin', 'hp': 70, 'attack': 20, 'gold': 60, 'xp': 70},
    {'name': 'Harpy', 'hp': 120, 'attack': 22, 'gold': 90, 'xp': 110},
    {'name': 'Orc', 'hp': 100, 'attack': 25, 'gold': 150, 'xp': 180},
    {'name': 'Troll', 'hp': 150, 'attack': 30, 'gold': 300, 'xp': 350},
    {'name': 'Skeleton Warrior', 'hp': 200, 'attack': 35, 'gold': 500, 'xp': 600},
    {'name': 'Basilisk', 'hp': 280, 'attack': 38, 'gold': 750, 'xp': 900},
    {'name': 'Dark Mage', 'hp': 250, 'attack': 40, 'gold': 1200, 'xp': 1500},
    {'name': 'Stone Golem', 'hp': 350, 'attack': 28, 'gold': 1000, 'xp': 1200},
    {'name': 'Demon Spawn', 'hp': 300, 'attack': 50, 'gold': 2200, 'xp': 2800},
    {'name': 'Nightmare Fiend', 'hp': 550, 'attack': 65, 'gold': 3500, 'xp': 4200},
    {'name': 'Fire Drake', 'hp': 400, 'attack': 60, 'gold': 5000, 'xp': 6000},
    {'name': 'Lich', 'hp': 450, 'attack': 55, 'gold': 8000, 'xp': 10000},
    {'name': 'Shadow Lord', 'hp': 500, 'attack': 75, 'gold': 12000, 'xp': 15000},
    {'name': 'Hydra Hatchling', 'hp': 600, 'attack': 70, 'gold': 18000, 'xp': 22000},
    {'name': 'Ancient Dragon', 'hp': 700, 'attack': 100, 'gold': 25000, 'xp': 30000},
    {'name': 'Frost Giant', 'hp': 800, 'attack': 90, 'gold': 40000, 'xp': 50000},
    {'name': 'Abyssal Horror', 'hp': 1200, 'attack': 180, 'gold': 70000, 'xp': 85000},
    {'name': 'Celestial Guardian', 'hp': 1800, 'attack': 220, 'gold': 150000, 'xp': 200000},
    {'name': 'Chaos Titan', 'hp': 2500, 'attack': 300, 'gold': 250000, 'xp': 300000},
]

ENEMY_SPAWN_RULES = [
    (2, slice(0, 2), [7, 3]),
    (4, slice(0, 4), [5, 3, 2, 1]),
    (7, slice(1, 6), [4, 3, 2, 1, 1]),
    (10, slice(3, 8), [3, 3, 2, 1, 1]),
    (14, slice(5, 10), [3, 2, 2, 1, 1]),
    (19, slice(7, 12), [2, 2, 2, 1, 1]),
    (24, slice(9, 14), [2, 2, 1, 1, 1]),
    (29, slice(11, 16), [2, 1, 1, 1, 1]),
    (34, slice(13, 18), [1, 1, 1, 1, 1]),
    (39, slice(15, 20), [1, 1, 1, 1, 0.5]),
    (44, slice(17, 22), [1, 1, 0.5, 0.5, 0.2]),
    (float('inf'), slice(18, None), [1, 1, 1, 1])
]

POTION_USE_CHOICES = {'1': 'healing', '2': 'defense', '3': 'strength'}
SKILL_UPGRADE_CONFIG = {
    "1": {"var_name": "player_max_health", "increment": 5, "cost": 1, "display_key": "player_max_health"},
    "2": {"var_name": "player_gold_bonus_multiplier", "increment": 0.015, "cost": 1,
          "display_key": "player_gold_bonus_multiplier"},
    "3": {"var_name": "player_max_attack", "increment": 2, "cost": 1, "display_key": "player_max_attack"},
    "4": {"var_name": "player_min_attack", "increment": 1, "cost": 1, "display_key": "player_min_attack"},
    "5": {"var_name": "player_crit_bonus_multiplier", "increment": 0.01, "cost": 1,
          "display_key": "player_crit_bonus_multiplier"},
    "6": {"var_name": "player_xp_bonus_multiplier", "increment": 0.02, "cost": 1,
          "display_key": "player_xp_bonus_multiplier"},
}

PERK_SHOP_CONFIG = {
    "shop_discount": {
        "name": "Merchant's Favor",
        "id_char": "d",
        "levels": [
            {"cost": 500, "effect_value": 0.05, "description_template": "Get a {:.0f}% discount in all shops."},
            {"cost": 2000, "effect_value": 0.10, "description_template": "Increase discount to {:.0f}% in all shops."},
            {"cost": 6000, "effect_value": 0.15, "description_template": "Increase discount to {:.0f}% in all shops."},
            {"cost": 10000, "effect_value": 0.20, "description_template": "Increase discount to {:.0f}% in all shops."}
        ]
    },
    "menu_heal": {
        "name": "Quick Mend",
        "id_char": "h",
        "levels": [
            {"cost": 100, "effect_value": 10,
             "description_template": "Heal {:.0f} HP from the menu (once after each battle)."},
            {"cost": 500, "effect_value": 25, "description_template": "Increase menu heal to {:.0f} HP."},
            {"cost": 1000, "effect_value": 45, "description_template": "Increase menu heal to {:.0f} HP."}
        ]
    }
}


def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')


def get_random_dialog(stall_owner_key, dialog_type_key): return random.choice(DIALOGS[stall_owner_key][dialog_type_key])


def reset_player_state_to_default():
    global is_hardcore_mode, stall_first_visit, player_health, player_max_health, player_max_attack
    global player_min_attack, player_defense, player_gold, player_xp, player_skill_points
    global player_xp_to_level_up, player_level, player_crit_bonus_multiplier, player_gold_bonus_multiplier
    global player_xp_bonus_multiplier, first_kill_jackpot_awarded
    global player_perks, can_use_menu_heal, player_potions_inventory, total_fights_won, stall_item_stocks
    global is_defense_potion_active, is_strength_potion_active

    is_hardcore_mode = False
    is_defense_potion_active = False
    is_strength_potion_active = False
    stall_first_visit = {"alice": True, "unknown": True, "aaron": True}
    player_health = 100
    player_max_health = 100
    player_max_attack = 20
    player_min_attack = 5
    player_defense = 0
    player_gold = 50
    player_xp = 0
    player_skill_points = 0
    player_xp_to_level_up = 100
    player_level = 0
    player_crit_bonus_multiplier = 0.1
    player_gold_bonus_multiplier = 0.0
    player_xp_bonus_multiplier = 0.0
    first_kill_jackpot_awarded = {}
    player_perks = {"shop_discount": 0, "menu_heal": 0}
    can_use_menu_heal = False
    player_potions_inventory = {'healing': 1, 'defense': 1, 'strength': 1}
    total_fights_won = 0
    stall_item_stocks = {'alice': 5, 'unknown': 5, 'aaron': 5}


def ask_for_hardcore_mode():
    global is_hardcore_mode
    clear_screen()
    print("Welcome, Adventurer!")
    while True:
        print("Do you want to enable Hardcore Mode? (y/n)\n(In Hardcore Mode, your game progress will NOT be saved.)")
        choice1 = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        if choice1 == 'y':
            clear_screen()
            print(
                "ARE YOU SURE you want to enable Hardcore Mode?\nThis means NO SAVES. If you die or quit, progress is GONE.\nConfirm (y/n):")
            choice2 = msvcrt.getch().decode('utf-8', errors='ignore').lower()
            if choice2 == 'y':
                is_hardcore_mode = True
                print("Hardcore Mode ENABLED. Good luck.")
                time.sleep(2)
                break
            else:
                is_hardcore_mode = False
                print("Hardcore Mode DISABLED.")
                time.sleep(1.5)
                break
        elif choice1 == 'n':
            is_hardcore_mode = False
            print("Hardcore Mode DISABLED. Progress will be saved.")
            time.sleep(1.5)
            break
        else:
            clear_screen()
            print("Invalid input. Please press 'y' or 'n'.")
            time.sleep(1)
    clear_screen()


def gather_game_state():
    return {
        "is_hardcore_mode": is_hardcore_mode, "stall_first_visit": stall_first_visit, "player_health": player_health,
        "player_max_health": player_max_health, "player_max_attack": player_max_attack,
        "player_min_attack": player_min_attack,
        "player_defense": player_defense, "player_gold": player_gold, "player_xp": player_xp,
        "player_skill_points": player_skill_points, "player_xp_to_level_up": player_xp_to_level_up,
        "player_level": player_level,
        "player_crit_bonus_multiplier": player_crit_bonus_multiplier,
        "player_gold_bonus_multiplier": player_gold_bonus_multiplier,
        "player_xp_bonus_multiplier": player_xp_bonus_multiplier,
        "first_kill_jackpot_awarded": first_kill_jackpot_awarded,
        "player_potions_inventory": player_potions_inventory, "total_fights_won": total_fights_won,
        "stall_item_stocks": stall_item_stocks, "player_perks": player_perks, "can_use_menu_heal": can_use_menu_heal,
    }


def apply_game_state(loaded_state):
    global is_hardcore_mode, stall_first_visit, player_health, player_max_health, player_max_attack, player_min_attack
    global player_defense, player_gold, player_xp, player_skill_points, player_xp_to_level_up, player_level
    global player_crit_bonus_multiplier, player_gold_bonus_multiplier, player_xp_bonus_multiplier
    global first_kill_jackpot_awarded
    global player_potions_inventory, total_fights_won
    global stall_item_stocks, player_perks, can_use_menu_heal

    reset_player_state_to_default()
    for key, default_val in gather_game_state().items():
        setattr(__import__(__name__), key, loaded_state.get(key, default_val))

    stall_first_visit.update(loaded_state.get("stall_first_visit", {"alice": True, "unknown": True, "aaron": True}))
    player_potions_inventory.update(
        loaded_state.get("player_potions_inventory", {'healing': 1, 'defense': 1, 'strength': 1}))
    stall_item_stocks.update(loaded_state.get("stall_item_stocks", {'alice': 5, 'unknown': 5, 'aaron': 5}))
    player_perks.update(loaded_state.get("player_perks", {"shop_discount": 0, "menu_heal": 0}))
    first_kill_jackpot_awarded.update(loaded_state.get("first_kill_jackpot_awarded", {}))


def save_game_state():
    if is_hardcore_mode: return
    try:
        encrypted_data = cipher_suite.encrypt(json.dumps(gather_game_state()).encode('utf-8'))
        with open(SAVE_FILE_NAME, "wb") as f:
            f.write(encrypted_data)
    except Exception:
        pass


def load_game_state():
    if not os.path.exists(SAVE_FILE_NAME): return False
    try:
        with open(SAVE_FILE_NAME, "rb") as f:
            encrypted_data = f.read()
        apply_game_state(json.loads(cipher_suite.decrypt(encrypted_data).decode('utf-8')))
        print("Game loaded successfully.")
        time.sleep(1)
        return True
    except Exception:
        try:
            os.rename(SAVE_FILE_NAME, SAVE_FILE_NAME + f".corrupted_{int(time.time())}")
        except OSError:
            pass
        return False


def delete_save_file():
    try:
        if os.path.exists(SAVE_FILE_NAME):
            os.remove(SAVE_FILE_NAME)
        return True
    except OSError:
        return False


def reset_game_progress():
    clear_screen()
    print("Are you sure you want to reset all progress? This cannot be undone. (y/n)")
    confirm1 = msvcrt.getch().decode('utf-8', errors='ignore').lower()
    if confirm1 == 'y':
        clear_screen()
        print("FINAL WARNING: All saved data will be DELETED. Continue? (y/n)")
        confirm2 = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        if confirm2 == 'y':
            if delete_save_file():
                print("Progress reset. Restarting game...")
            else:
                print("Could not delete save file. Please check file permissions.")
            reset_player_state_to_default()
            time.sleep(2)
            ask_for_hardcore_mode()
            print("Starting your new adventure...")
            time.sleep(1)
            start_battle()
            return True
        else:
            print("Reset cancelled.")
    else:
        print("Reset cancelled.")
    time.sleep(1.5)
    return False


def get_current_shop_discount():
    discount_level = player_perks.get("shop_discount", 0)
    if discount_level > 0 and discount_level <= len(PERK_SHOP_CONFIG["shop_discount"]["levels"]):
        return PERK_SHOP_CONFIG["shop_discount"]["levels"][discount_level - 1]["effect_value"]
    return 0


def calculate_discounted_price(original_price):
    discount = get_current_shop_discount()
    return round(original_price * (1 - discount))


def process_purchase(stall_owner_key, item_choice_id):
    global player_gold, player_potions_inventory, player_min_attack, player_max_attack, player_defense
    clear_screen()
    stall_data = SHOP_ITEMS_DATA[stall_owner_key]
    item_to_purchase = None
    item_key_purchased = None
    for key, details in stall_data['items'].items():
        if details['id'] == item_choice_id: item_to_purchase = details; item_key_purchased = key; break
    if not item_to_purchase: print("Sorry, that item doesn't exist."); return False

    actual_price = calculate_discounted_price(item_to_purchase['price'])
    if actual_price > player_gold: print("You don't have enough gold!"); return False

    player_gold -= actual_price
    item_display_name = ITEM_DISPLAY_NAMES[item_to_purchase['name_key']]
    if stall_data['category'] == 'potions':
        player_potions_inventory[item_key_purchased] += 1
    elif stall_data['category'] == 'swords':
        player_min_attack += item_to_purchase['damage_increase'][0]
        player_max_attack += \
            item_to_purchase['damage_increase'][1]
    elif stall_data['category'] == 'armor':
        player_defense += item_to_purchase['defense_increase']
    print(f"You purchased {item_display_name} for {actual_price}G!")
    return True


def visit_stall(stall_owner_key):
    global stall_first_visit, stall_item_stocks
    clear_screen()
    stall_config = SHOP_ITEMS_DATA[stall_owner_key]
    if stall_first_visit[stall_owner_key]:
        for line in stall_config['first_visit_dialog']: print(line); time.sleep(
            1 if len(stall_config['first_visit_dialog']) > 1 else 0)
        stall_first_visit[stall_owner_key] = False
    elif stall_item_stocks[stall_owner_key] > 0:
        print(get_random_dialog(stall_owner_key, 'hello'))

    while stall_item_stocks[stall_owner_key] > 0:
        print("\nWhat do you want to buy?")
        for item_data in stall_config['items'].values():
            display_name = ITEM_DISPLAY_NAMES[item_data['name_key']]
            discounted_price = calculate_discounted_price(item_data['price'])
            print(f"{item_data['id']}. {display_name} [{discounted_price}G]", end="  ")
        print("\nE. Exit the stall")
        player_choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        if player_choice == "e": print(get_random_dialog(stall_owner_key, 'bye')); break
        if process_purchase(stall_owner_key, player_choice):
            print(get_random_dialog(stall_owner_key, 'thanks'))
            stall_item_stocks[stall_owner_key] -= 1
        time.sleep(1.5)
        clear_screen()
        if stall_item_stocks[stall_owner_key] <= 0: break
    if stall_item_stocks[stall_owner_key] <= 0: print(stall_config['out_of_stock_dialog'])
    time.sleep(2)


def open_market():
    clear_screen()
    while True:
        print(
            "You are in the market!\nWho do you want to visit?\n1. Alice (Potions), 2. Unknown (Armor), 3. Aaron (Swords)\nE. Exit")
        market_choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        if market_choice == "1":
            visit_stall('alice')
        elif market_choice == "2":
            visit_stall('unknown')
        elif market_choice == "3":
            visit_stall('aaron')
        elif market_choice == "e":
            clear_screen(); break
        else:
            print("Invalid choice!")
        clear_screen()


def handle_battle_outcome(current_player_health, current_enemy_health, enemy_data):
    global player_health, player_defense, player_max_attack, is_strength_potion_active, is_defense_potion_active
    global stall_item_stocks, total_fights_won, player_gold, player_xp, can_use_menu_heal
    if current_player_health <= 0: clear_screen(); print("You have been defeated!"); time.sleep(2); exit()
    if current_enemy_health <= 0:
        clear_screen()
        print(f"You have defeated the {enemy_data['name']}!")
        awarded_gold, awarded_xp = calculate_rewards(enemy_data['gold'], enemy_data['xp'], enemy_data['name'])
        player_gold += awarded_gold
        player_xp += awarded_xp
        print(f"You received {awarded_gold:,} G and {awarded_xp:,} XP.")
        time.sleep(1)
        check_for_level_up()
        total_fights_won += 1
        if is_strength_potion_active: player_max_attack -= POTION_STRENGTH_BOOST; is_strength_potion_active = False
        if is_defense_potion_active: player_defense -= POTION_DEFENSE_BOOST; is_defense_potion_active = False
        stall_item_stocks['alice'] = min(stall_item_stocks['alice'] + 3, 5)
        menu_heal_level = player_perks.get("menu_heal", 0)
        if menu_heal_level > 0 and menu_heal_level <= len(PERK_SHOP_CONFIG["menu_heal"]["levels"]):
            can_use_menu_heal = True
        save_game_state()
        time.sleep(2)
        return True
    return False


def use_potion_in_battle(potion_choice_key):
    global player_potions_inventory, player_health, player_defense, player_max_attack, is_strength_potion_active, is_defense_potion_active, potions_used_this_turn
    potion_type = POTION_USE_CHOICES.get(potion_choice_key)
    if not potion_type: clear_screen(); print("Invalid potion choice!"); return
    if player_potions_inventory.get(potion_type, 0) <= 0: clear_screen(); print(
        f"You have no {ITEM_DISPLAY_NAMES[potion_type]}s!"); return
    clear_screen()
    if potion_type == 'healing':
        player_potions_inventory['healing'] -= 1
        player_health = min(player_health + POTION_HEAL_AMOUNT,
                            player_max_health)
        print(
            f"Healing Potion used! Healed {POTION_HEAL_AMOUNT} HP.")
    elif potion_type == 'defense':
        if is_defense_potion_active: print("Defense Potion already active!"); return
        player_potions_inventory['defense'] -= 1
        player_defense += POTION_DEFENSE_BOOST
        is_defense_potion_active = True
        print(f"Defense Potion used! Defense +{POTION_DEFENSE_BOOST}.")
    elif potion_type == 'strength':
        if is_strength_potion_active: print("Strength Potion already active!"); return
        player_potions_inventory['strength'] -= 1
        player_max_attack += POTION_STRENGTH_BOOST
        is_strength_potion_active = True
        print(f"Strength Potion used! Max Attack +{POTION_STRENGTH_BOOST}.")
    potions_used_this_turn += 1
    time.sleep(1.5)


def check_for_level_up():
    global player_xp_to_level_up, player_level, player_xp, player_skill_points
    leveled_up = False
    while player_xp >= player_xp_to_level_up:
        player_xp -= player_xp_to_level_up
        original_level = player_level
        player_level += 1
        player_skill_points += 1

        if player_level <= 20:
            player_xp_to_level_up += round(player_xp_to_level_up * 0.25)
        elif player_level <= 35:
            player_xp_to_level_up += round(player_xp_to_level_up * 0.15)
        else:
            player_xp_to_level_up += round(player_xp_to_level_up * 0.08) + 1000

        print(
            f"LEVEL UP! Lvl {original_level} -> {player_level}. +1 Skill Point. Next Lvl: {player_xp_to_level_up:,} XP.")
        leveled_up = True
    if leveled_up: time.sleep(1)


def calculate_rewards(base_gold, base_xp, enemy_name):
    global first_kill_jackpot_awarded

    actual_gold = round(base_gold + (base_gold * player_gold_bonus_multiplier))
    actual_xp = round(base_xp + (base_xp * player_xp_bonus_multiplier))

    jackpot_enemies = ["Chaos Titan", "Celestial Guardian"]
    if enemy_name in jackpot_enemies and not first_kill_jackpot_awarded.get(enemy_name, False):
        clear_screen()
        print("*" * 40)
        print(f"*** CONGRATULATIONS! FIRST KILL OF {enemy_name}! ***")
        print("*" * 40)
        time.sleep(1)

        jackpot_gold = random.randint(800000, 1200000)
        jackpot_xp_bonus = 0
        if enemy_name == "Chaos Titan":
            jackpot_xp_bonus = random.randint(700000, 1000000)
        elif enemy_name == "Celestial Guardian":
            jackpot_xp_bonus = random.randint(600000, 900000)

        print(f"You found a legendary hoard of {jackpot_gold:,} GOLD!")
        print(f"And gained an additional {jackpot_xp_bonus:,} XP from this momentous victory!")
        time.sleep(3)

        actual_gold = jackpot_gold
        actual_xp += jackpot_xp_bonus

        first_kill_jackpot_awarded[enemy_name] = True

    return actual_gold, actual_xp


def select_random_enemy():
    for max_fights, sl, w in ENEMY_SPAWN_RULES:
        if total_fights_won <= max_fights:
            enemies_in_slice = ENEMY_TEMPLATES[sl]
            if not w or len(w) != len(enemies_in_slice) or sum(w) <= 0:
                return dict(random.choice(enemies_in_slice))
            return dict(random.choices(enemies_in_slice, weights=w, k=1)[0])
    return dict(ENEMY_TEMPLATES[-1])


def perform_attack_round(current_enemy_hp, enemy_stats):
    global player_health, potions_used_this_turn
    dmg = random.randint(player_min_attack, player_max_attack)
    if random.randint(1, 4) == 4: dmg += round(player_max_attack * player_crit_bonus_multiplier); print("Critical Hit!")
    enemy_dmg = max(0, random.randint(1, enemy_stats['attack']) - player_defense)
    current_enemy_hp -= dmg
    player_health -= enemy_dmg
    print(f"You dealt {dmg:.0f} DMG. Enemy dealt {enemy_dmg:.0f} DMG.")
    potions_used_this_turn = 0
    return current_enemy_hp


def start_battle():
    global player_health, potions_used_this_turn
    clear_screen()
    enemy = select_random_enemy()
    enemy_hp = enemy['hp']
    print(f"Encounter: {enemy['name']} (HP: {enemy_hp:.0f}).")
    time.sleep(1)
    battle_over = False
    while player_health > 0 and enemy_hp > 0:
        clear_screen()
        print(f"{enemy['name']} HP: {enemy_hp:.0f} | Your HP: {player_health:.0f}\nAction: 1. Attack, 2. Potion")
        action = msvcrt.getch().decode('utf-8', errors='ignore')
        if action == "1":
            clear_screen(); enemy_hp = perform_attack_round(enemy_hp, enemy)
        elif action == "2":
            if potions_used_this_turn >= 3: clear_screen(); print("Too many potions this turn!"); time.sleep(1.5); continue
            if not any(player_potions_inventory.values()): clear_screen(); print("No potions!"); time.sleep(1.5); continue
            clear_screen()
            print("Use Potion:")
            opts, valid_choices, num = [], {}, 1
            for k, v in POTION_USE_CHOICES.items():
                if player_potions_inventory.get(v, 0) > 0:
                    opts.append(f"{num}. {ITEM_DISPLAY_NAMES[v]} ({player_potions_inventory[v]})")
                    valid_choices[str(num)] = k
                    num += 1
            if not valid_choices: print("No potions!"); time.sleep(1.5); continue
            for o in opts: print(o)
            print("E. Cancel")
            p_choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()
            if p_choice == 'e': continue
            if p_choice in valid_choices:
                use_potion_in_battle(valid_choices[p_choice])
            else:
                clear_screen(); print("Invalid selection."); time.sleep(1.5)
        else:
            clear_screen()
            print("Invalid action!")
            time.sleep(1)
        if player_health <= 0 or enemy_hp <= 0: battle_over = handle_battle_outcome(player_health, enemy_hp, enemy); break
        time.sleep(1.5)
    if battle_over: main_game_menu()


def open_skill_shop():
    global player_skill_points
    clear_screen()
    while True:
        print(f"Skill Shop (Points: {player_skill_points}). Upgrade what?\n")
        for k, conf in SKILL_UPGRADE_CONFIG.items():
            name = ITEM_DISPLAY_NAMES[conf['display_key']]
            val = globals()[conf['var_name']]
            inc = conf['increment']
            is_mult = "multiplier" in conf['display_key']
            val_str = f"{val * 100:.1f}%" if is_mult else f"{val:.0f}"
            inc_str = f"+{inc * 100:.1f}%" if is_mult else f"+{inc:.0f}"
            print(f"{k}. {name} (Now: {val_str}, {inc_str}) - Cost: {conf['cost']} SP")
        print("E. Exit")
        choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        clear_screen()
        if choice == 'e': print("Exiting skill shop."); break
        upg = SKILL_UPGRADE_CONFIG.get(choice)
        if upg:
            if player_skill_points >= upg['cost']:
                globals()[upg['var_name']] += upg['increment']
                player_skill_points -= upg['cost']
                new_val_str = f"{globals()[upg['var_name']] * 100:.1f}%" if "multiplier" in upg[
                    'display_key'] else f"{globals()[upg['var_name']]:.0f}"
                print(
                    f"Upgraded {ITEM_DISPLAY_NAMES[upg['display_key']]}! New: {new_val_str}. Points left: {player_skill_points}.")
            else:
                print("Not enough skill points.")
        else:
            print("Invalid choice.")
        time.sleep(2)
        clear_screen()


def open_perk_shop():
    global player_gold, player_perks
    clear_screen()
    while True:
        print(f"Perk Shop (Gold: {player_gold:,}). Permanent Upgrades:\n")
        perk_choices = {}
        for perk_key, config in PERK_SHOP_CONFIG.items():
            current_level = player_perks.get(perk_key, 0)
            print(f"{config['id_char'].upper()}. {config['name']}")
            perk_choices[config['id_char']] = perk_key

            if current_level > 0 and current_level <= len(config['levels']):
                current_effect = config['levels'][current_level - 1]['effect_value']
                desc_val = current_effect * 100 if "discount" in perk_key else current_effect
                print(
                    f"   Current Lvl {current_level}: {config['levels'][current_level - 1]['description_template'].format(desc_val)}")
            else:
                print("   Not yet acquired.")

            if current_level < len(config['levels']):
                next_level_data = config['levels'][current_level]
                next_desc_val = next_level_data['effect_value'] * 100 if "discount" in perk_key else next_level_data[
                    'effect_value']
                print(
                    f"   Next Lvl {current_level + 1}: {next_level_data['description_template'].format(next_desc_val)} - Cost: {next_level_data['cost']:,}G")
            else:
                print("   Max Level Reached.")
            print("-" * 20)
        print("E. Exit Shop")

        choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        clear_screen()
        if choice == 'e': print("Exiting Perk Shop."); break

        chosen_perk_key = perk_choices.get(choice)
        if chosen_perk_key:
            config = PERK_SHOP_CONFIG[chosen_perk_key]
            current_level = player_perks.get(chosen_perk_key, 0)
            if current_level < len(config['levels']):
                next_level_data = config['levels'][current_level]
                if player_gold >= next_level_data['cost']:
                    player_gold -= next_level_data['cost']
                    player_perks[chosen_perk_key] = current_level + 1
                    print(f"Purchased Level {current_level + 1} of {config['name']}!")
                    save_game_state()
                else:
                    print("Not enough gold for this perk.")
            else:
                print(f"{config['name']} is already at max level.")
        else:
            print("Invalid choice.")
        time.sleep(2)
        clear_screen()


def main_game_menu():
    global player_health, can_use_menu_heal
    clear_screen()
    while True:
        print("Main Menu")
        print(
            f"HP: {player_health:.0f}/{player_max_health:.0f} | Gold: {player_gold:,} | Lvl: {player_level} ({player_xp:,.0f}/{player_xp_to_level_up:,.0f} XP) | SP: {player_skill_points}")
        if is_hardcore_mode: print("HARDCORE MODE ACTIVE (NO SAVES)")

        menu_options = "1. Battle, 2. Market, 3. Skill Shop, 4. Perk Shop"
        menu_heal_level = player_perks.get("menu_heal", 0)
        heal_option_key = None
        reset_option_key = "r"

        if menu_heal_level > 0 and can_use_menu_heal and menu_heal_level <= len(
                PERK_SHOP_CONFIG["menu_heal"]["levels"]):
            heal_perk_config = PERK_SHOP_CONFIG["menu_heal"]["levels"][menu_heal_level - 1]
            heal_amount = heal_perk_config["effect_value"]
            heal_option_key = "h"
            menu_options += f", {heal_option_key.upper()}. Quick Mend ({heal_amount:.0f} HP)"

        menu_options += f", {reset_option_key.upper()}. Reset Progress, Q. Quit"
        print(menu_options)

        choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()

        if choice == "1":
            start_battle()
            break
        elif choice == "2":
            open_market()
            clear_screen()
        elif choice == "3":
            open_skill_shop()
            clear_screen()
        elif choice == "4":
            open_perk_shop()
            clear_screen()
        elif choice == heal_option_key and menu_heal_level > 0 and can_use_menu_heal:
            if menu_heal_level <= len(PERK_SHOP_CONFIG["menu_heal"]["levels"]):
                heal_amount = PERK_SHOP_CONFIG["menu_heal"]["levels"][menu_heal_level - 1]["effect_value"]
                actual_heal = min(heal_amount, player_max_health - player_health)
                player_health += actual_heal
                can_use_menu_heal = False
                clear_screen()
                print(f"Used Quick Mend, healed {actual_heal:.0f} HP.")
                time.sleep(1.5)
                clear_screen()
        elif choice == reset_option_key:
            if reset_game_progress():
                return
        elif choice == "q":
            print("Exiting game. Goodbye!")
            exit()
        else:
            clear_screen()
            print("Invalid choice.")
            time.sleep(1)
            clear_screen()


if __name__ == "__main__":
    if not load_game_state():
        reset_player_state_to_default()
        ask_for_hardcore_mode()
        print("Starting your adventure...")
        time.sleep(1)
        start_battle()
    else:
        print("Continuing your adventure...")
        time.sleep(1)
        main_game_menu()
