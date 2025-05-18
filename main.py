import os
import random
import msvcrt
import time
import json
from cryptography.fernet import Fernet

ENCRYPTION_KEY = b'uP4u1U_RzJtX2xY6vQwA5iNl9fGk0cHj7bM8zO7dS1s=' # pls dont cheat ;-;
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
    "healing": "Healing Potion",
    "defense": "Defense Potion",
    "strength": "Strength Potion",
    "heavy_armor": "Heavy Armor",
    "medium_armor": "Medium Armor",
    "light_armor": "Light Armor",
    "short_sword": "Short Sword",
    "long_sword": "Long Sword",
    "great_sword": "Great Sword",
    "player_max_health": "Max Health",
    "player_gold_bonus_multiplier": "Gold Multiplier",
    "player_max_attack": "Max Damage Dealt",
    "player_min_attack": "Min Damage Dealt",
    "player_crit_bonus_multiplier": "Critical Hit Multiplier"
}

DIALOGS = {
    'alice': {
        'hello': ['Alice: Hi, do you want anything?', 'Alice: Hey! What do you want to buy?'],
        'bye': ['Alice: See you next time!', 'Alice: Bye Bye!', 'Alice: Goodbye!'],
        'thanks': ['Alice: Thanks for buying!', 'Alice: Anything else?']
    },
    'unknown': {
        'hello': ['Unknown: ...You seek something?', 'Unknown: The shadows whisper... what do you desire?',
                  'Unknown: You have summoned me. Speak.'],
        'bye': ['Unknown: Fading into the void...', 'Unknown: You leave, but the darkness remains.',
                'Unknown: Until next time, wanderer.'],
        'thanks': ['Unknown: The pact is sealed.', 'Unknown: Gratitude is a fleeting shadow.',
                   'Unknown: It is done. Will there be more?']
    },
    'aaron': {
        'hello': ['Aaron: Yo, what’s up? Need something?', 'Aaron: Hey there! What can I get you?',
                  'Aaron: Sup! You looking for something?'],
        'bye': ['Aaron: Catch you later!', 'Aaron: See ya, man!', 'Aaron: Peace out!'],
        'thanks': ['Aaron: Thanks, buddy!', 'Aaron: Appreciate it! Need anything else?',
                   'Aaron: Cool, thanks! Let me know if you want more.']
    }
}

SHOP_ITEMS_DATA = {
    'alice': {
        'name': "Alice's Potion Stall",
        'category': 'potions',
        'stock_type': 'potions',
        'items': {
            'healing': {'id': '1', 'price': 30, 'name_key': 'healing'},
            'defense': {'id': '2', 'price': 40, 'name_key': 'defense'},
            'strength': {'id': '3', 'price': 50, 'name_key': 'strength'}
        },
        'first_visit_dialog': ["Alice: Hey! Welcome to my little stall.", "Alice: Sooo... Do you want anything?"],
        'out_of_stock_dialog': "Alice: I'm sorry... I am out of potions."
    },
    'aaron': {
        'name': "Aaron's Sword Stall",
        'category': 'swords',
        'stock_type': 'swords',
        'items': {
            'short_sword': {'id': '1', 'price': 50, 'damage_increase': (1, 3), 'name_key': 'short_sword'},
            'long_sword': {'id': '2', 'price': 100, 'damage_increase': (2, 5), 'name_key': 'long_sword'},
            'great_sword': {'id': '3', 'price': 150, 'damage_increase': (3, 7), 'name_key': 'great_sword'}
        },
        'first_visit_dialog': ["Aaron: Greetings, adventurer. Looking for a new blade?"],
        'out_of_stock_dialog': "Aaron: Sorry, I am out of swords."
    },
    'unknown': {
        'name': "The Unknown's Armor Stall",
        'category': 'armor',
        'stock_type': 'armor',
        'items': {
            'light_armor': {'id': '1', 'price': 60, 'defense_increase': 5, 'name_key': 'light_armor'},
            'medium_armor': {'id': '2', 'price': 120, 'defense_increase': 10, 'name_key': 'medium_armor'},
            'heavy_armor': {'id': '3', 'price': 180, 'defense_increase': 15, 'name_key': 'heavy_armor'}
        },
        'first_visit_dialog': ["Unknown: ... Arm yourself.", "Unknown: ... Protect yourself."],
        'out_of_stock_dialog': "Unknown: ... Out of stock."
    }
}

ENEMY_TEMPLATES = [
    {'name': 'Wolf', 'hp': 30, 'attack': 10, 'gold': 10, 'xp': 20},
    {'name': 'Mini-Goblin', 'hp': 50, 'attack': 15, 'gold': 20, 'xp': 30},
    {'name': 'Goblin', 'hp': 70, 'attack': 20, 'gold': 30, 'xp': 40},
    {'name': 'Orc', 'hp': 100, 'attack': 25, 'gold': 50, 'xp': 60},
    {'name': 'Troll', 'hp': 150, 'attack': 30, 'gold': 70, 'xp': 80},
    {'name': 'Skeleton Warrior', 'hp': 200, 'attack': 35, 'gold': 100, 'xp': 100},
    {'name': 'Dark Mage', 'hp': 250, 'attack': 40, 'gold': 150, 'xp': 150},
    {'name': 'Demon Spawn', 'hp': 300, 'attack': 50, 'gold': 200, 'xp': 200},
    {'name': 'Fire Drake', 'hp': 400, 'attack': 60, 'gold': 300, 'xp': 300},
    {'name': 'Shadow Lord', 'hp': 500, 'attack': 75, 'gold': 400, 'xp': 400},
    {'name': 'Ancient Dragon', 'hp': 700, 'attack': 100, 'gold': 500, 'xp': 500},
    {'name': 'Chaos Titan', 'hp': 1000, 'attack': 150, 'gold': 700, 'xp': 700}
]

ENEMY_SPAWN_RULES = [
    (4, slice(0, 2), [8, 2]), (9, slice(0, 3), [6, 3, 1]), (14, slice(0, 4), [5, 3, 2, 1]),
    (19, slice(0, 5), [4, 3, 2, 1, 1]), (24, slice(0, 6), [3, 2, 2, 2, 1, 1]),
    (29, slice(0, 7), [2, 2, 2, 2, 1, 1, 1]), (34, slice(0, 8), [2, 2, 1, 1, 1, 1, 2, 2]),
    (39, slice(0, 9), [1, 1, 1, 1, 2, 2, 3, 3, 4]), (44, slice(0, 10), [1, 1, 1, 2, 2, 2, 3, 3, 4, 5]),
    (49, slice(0, 11), [1, 1, 1, 1, 1, 2, 3, 3, 4, 5, 6]),
    (float('inf'), slice(0, None), [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 8])
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
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_random_dialog(stall_owner_key, dialog_type_key):
    return random.choice(DIALOGS[stall_owner_key][dialog_type_key])


def ask_for_hardcore_mode():
    global is_hardcore_mode
    clear_screen()
    print("Welcome, Adventurer!")
    while True:
        print("Do you want to enable Hardcore Mode? (y/n)")
        print("(In Hardcore Mode, your game progress will NOT be saved.)")
        choice1 = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        if choice1 == 'y':
            clear_screen()
            print("ARE YOU SURE you want to enable Hardcore Mode?")
            print("This means NO SAVES. If you die or quit, progress is GONE.")
            print("Confirm (y/n):")
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
            print("Hardcore Mode DISABLED. Your progress will be saved after battles.")
            time.sleep(1.5)
            break
        else:
            clear_screen()
            print("Invalid input. Please press 'y' or 'n'.")
            time.sleep(1)
    clear_screen()


def gather_game_state():
    return {
        "is_hardcore_mode": is_hardcore_mode,
        "stall_first_visit": stall_first_visit,
        "player_health": player_health,
        "player_max_health": player_max_health,
        "player_max_attack": player_max_attack,
        "player_min_attack": player_min_attack,
        "player_defense": player_defense,
        "player_gold": player_gold,
        "player_xp": player_xp,
        "player_skill_points": player_skill_points,
        "player_xp_to_level_up": player_xp_to_level_up,
        "player_level": player_level,
        "player_crit_bonus_multiplier": player_crit_bonus_multiplier,
        "player_gold_bonus_multiplier": player_gold_bonus_multiplier,
        "player_potions_inventory": player_potions_inventory,
        "total_fights_won": total_fights_won,
        "stall_item_stocks": stall_item_stocks,
    }


def apply_game_state(loaded_state):
    global is_hardcore_mode, stall_first_visit, player_health, player_max_health
    global player_max_attack, player_min_attack, player_defense, player_gold, player_xp
    global player_skill_points, player_xp_to_level_up, player_level
    global player_crit_bonus_multiplier, player_gold_bonus_multiplier
    global player_potions_inventory, total_fights_won, stall_item_stocks

    is_hardcore_mode = loaded_state.get("is_hardcore_mode", False)
    stall_first_visit.update(loaded_state.get("stall_first_visit", stall_first_visit))
    player_health = loaded_state.get("player_health", player_health)
    player_max_health = loaded_state.get("player_max_health", player_max_health)
    player_max_attack = loaded_state.get("player_max_attack", player_max_attack)
    player_min_attack = loaded_state.get("player_min_attack", player_min_attack)
    player_defense = loaded_state.get("player_defense", player_defense)
    player_gold = loaded_state.get("player_gold", player_gold)
    player_xp = loaded_state.get("player_xp", player_xp)
    player_skill_points = loaded_state.get("player_skill_points", player_skill_points)
    player_xp_to_level_up = loaded_state.get("player_xp_to_level_up", player_xp_to_level_up)
    player_level = loaded_state.get("player_level", player_level)
    player_crit_bonus_multiplier = loaded_state.get("player_crit_bonus_multiplier", player_crit_bonus_multiplier)
    player_gold_bonus_multiplier = loaded_state.get("player_gold_bonus_multiplier", player_gold_bonus_multiplier)
    player_potions_inventory.update(loaded_state.get("player_potions_inventory", player_potions_inventory))
    total_fights_won = loaded_state.get("total_fights_won", total_fights_won)
    stall_item_stocks.update(loaded_state.get("stall_item_stocks", stall_item_stocks))


def save_game_state():
    if is_hardcore_mode:
        return
    state = gather_game_state()
    try:
        json_data = json.dumps(state).encode('utf-8')
        encrypted_data = cipher_suite.encrypt(json_data)
        with open(SAVE_FILE_NAME, "wb") as f:
            f.write(encrypted_data)
    except Exception:
        pass


def load_game_state():
    if not os.path.exists(SAVE_FILE_NAME):
        return False
    try:
        with open(SAVE_FILE_NAME, "rb") as f:
            encrypted_data = f.read()
        decrypted_data_bytes = cipher_suite.decrypt(encrypted_data)
        loaded_state = json.loads(decrypted_data_bytes.decode('utf-8'))
        apply_game_state(loaded_state)
        print("Game loaded successfully.")
        time.sleep(1)
        return True
    except Exception:
        try:
            os.rename(SAVE_FILE_NAME, SAVE_FILE_NAME + ".corrupted")
        except OSError:
            pass
        return False


def process_purchase(stall_owner_key, item_choice_id):
    global player_gold, player_potions_inventory, player_min_attack, player_max_attack, player_defense
    clear_screen()
    stall_data = SHOP_ITEMS_DATA[stall_owner_key]
    item_to_purchase = None
    item_key_purchased = None

    for key, details in stall_data['items'].items():
        if details['id'] == item_choice_id:
            item_to_purchase = details
            item_key_purchased = key
            break
    if not item_to_purchase:
        print("Sorry, that item doesn't exist.")
        return False
    if item_to_purchase['price'] > player_gold:
        print("You don't have enough gold!")
        return False

    player_gold -= item_to_purchase['price']
    item_display_name = ITEM_DISPLAY_NAMES[item_to_purchase['name_key']]

    if stall_data['category'] == 'potions':
        player_potions_inventory[item_key_purchased] += 1
        print(f"You purchased a {item_display_name}!")
    elif stall_data['category'] == 'swords':
        player_min_attack += item_to_purchase['damage_increase'][0]
        player_max_attack += item_to_purchase['damage_increase'][1]
        print(f"You purchased a {item_display_name}!")
    elif stall_data['category'] == 'armor':
        player_defense += item_to_purchase['defense_increase']
        print(f"You purchased {item_display_name}!")
    return True


def visit_stall(stall_owner_key):
    global stall_first_visit, stall_item_stocks
    clear_screen()
    stall_config = SHOP_ITEMS_DATA[stall_owner_key]

    if stall_first_visit[stall_owner_key]:
        for line in stall_config['first_visit_dialog']:
            print(line)
            if len(stall_config['first_visit_dialog']) > 1: time.sleep(1.5)
        stall_first_visit[stall_owner_key] = False
    elif stall_item_stocks[stall_owner_key] > 0:
        print(get_random_dialog(stall_owner_key, 'hello'))

    while stall_item_stocks[stall_owner_key] > 0:
        print("\nWhat do you want to buy?")
        for item_data in stall_config['items'].values():
            display_name = ITEM_DISPLAY_NAMES[item_data['name_key']]
            print(f"{item_data['id']}. {display_name} [{item_data['price']}G]", end="  ")
        print("\nE. Exit the stall")

        player_choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        if player_choice == "e":
            print(get_random_dialog(stall_owner_key, 'bye'))
            break
        purchase_successful = process_purchase(stall_owner_key, player_choice)
        if purchase_successful:
            print(get_random_dialog(stall_owner_key, 'thanks'))
            stall_item_stocks[stall_owner_key] -= 1
        time.sleep(1.5)
        clear_screen()
        if stall_item_stocks[stall_owner_key] <= 0: break
    if stall_item_stocks[stall_owner_key] <= 0:
        print(stall_config['out_of_stock_dialog'])
    time.sleep(2)


def open_market():
    clear_screen()
    while True:
        print("You are in the market!")
        print("Who do you want to visit?")
        print("1. Alice (Potions), 2. Unknown (Armor), 3. Aaron (Swords)")
        print("E. Exit the market")
        market_choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        if market_choice == "1":
            visit_stall('alice')
        elif market_choice == "2":
            visit_stall('unknown')
        elif market_choice == "3":
            visit_stall('aaron')
        elif market_choice == "e":
            clear_screen();
            break
        else:
            print("Invalid choice!")
        clear_screen()


def handle_battle_outcome(current_player_health, current_enemy_health, enemy_data):
    global player_health, player_defense, player_max_attack, is_strength_potion_active, is_defense_potion_active
    global stall_item_stocks, total_fights_won, player_gold, player_xp

    if current_player_health <= 0:
        clear_screen();
        print("You have been defeated!");
        time.sleep(2);
        exit()

    if current_enemy_health <= 0:
        clear_screen();
        print(f"You have defeated the {enemy_data['name']}!")
        awarded_gold, awarded_xp = calculate_rewards(enemy_data['gold'], enemy_data['xp'])
        player_gold += awarded_gold;
        player_xp += awarded_xp
        print(f"You received {awarded_gold:.0f} G and {awarded_xp} XP.");
        time.sleep(1)
        check_for_level_up();
        total_fights_won += 1

        if is_strength_potion_active: player_max_attack -= POTION_STRENGTH_BOOST; is_strength_potion_active = False
        if is_defense_potion_active: player_defense -= POTION_DEFENSE_BOOST; is_defense_potion_active = False

        stall_item_stocks['alice'] = min(stall_item_stocks['alice'] + 3, 5)
        save_game_state()
        time.sleep(2);
        return True
    return False


def use_potion_in_battle(potion_choice_key):
    global player_potions_inventory, player_health, player_defense, player_max_attack
    global is_strength_potion_active, is_defense_potion_active, potions_used_this_turn

    potion_type = POTION_USE_CHOICES.get(potion_choice_key)
    if not potion_type: clear_screen(); print("Invalid potion choice!"); return

    if player_potions_inventory.get(potion_type, 0) <= 0:
        clear_screen();
        print(f"You have no {ITEM_DISPLAY_NAMES[potion_type]}s!");
        return

    clear_screen()
    if potion_type == 'healing':
        player_potions_inventory['healing'] -= 1
        player_health = min(player_health + POTION_HEAL_AMOUNT, player_max_health)
        print(f"{ITEM_DISPLAY_NAMES['healing']} used! Healed for {POTION_HEAL_AMOUNT} HP.")
    elif potion_type == 'defense':
        if is_defense_potion_active: print("A defense potion is already active!"); return
        player_potions_inventory['defense'] -= 1;
        player_defense += POTION_DEFENSE_BOOST;
        is_defense_potion_active = True
        print(f"{ITEM_DISPLAY_NAMES['defense']} used! Defense increased by {POTION_DEFENSE_BOOST}.")
    elif potion_type == 'strength':
        if is_strength_potion_active: print("A strength potion is already active!"); return
        player_potions_inventory['strength'] -= 1;
        player_max_attack += POTION_STRENGTH_BOOST;
        is_strength_potion_active = True
        print(f"{ITEM_DISPLAY_NAMES['strength']} used! Max attack increased by {POTION_STRENGTH_BOOST}.")
    potions_used_this_turn += 1;
    time.sleep(1.5)


def check_for_level_up():
    global player_xp_to_level_up, player_level, player_xp, player_skill_points
    leveled_up = False
    while player_xp >= player_xp_to_level_up:
        player_xp -= player_xp_to_level_up;
        original_level = player_level;
        player_level += 1;
        player_skill_points += 1
        player_xp_to_level_up += round(player_xp_to_level_up / 4)
        print(f"LEVEL UP! Level {original_level} ----> {player_level}")
        print(f"You gained 1 skill point. Next level at {player_xp_to_level_up} XP.");
        leveled_up = True
    if leveled_up: time.sleep(1)


def calculate_rewards(base_gold, base_xp):
    gold_reward = base_gold + (base_gold * player_gold_bonus_multiplier)
    return round(gold_reward), base_xp


def select_random_enemy():
    for max_fights, enemy_slice, weights in ENEMY_SPAWN_RULES:
        if total_fights_won <= max_fights:
            return dict(random.choices(ENEMY_TEMPLATES[enemy_slice], weights=weights, k=1)[0])
    return dict(ENEMY_TEMPLATES[0])


def perform_attack_round(current_enemy_hp, enemy_stats):
    global player_health, potions_used_this_turn
    rolled_player_damage = random.randint(player_min_attack, player_max_attack)
    if random.randint(1, 4) == 4:
        rolled_player_damage += round(player_max_attack * player_crit_bonus_multiplier);
        print("Critical Hit!")
    player_damage_taken = max(0, random.randint(1, enemy_stats['attack']) - player_defense)
    current_enemy_hp -= rolled_player_damage;
    player_health -= player_damage_taken
    print(f"You dealt {rolled_player_damage:.0f} damage to the {enemy_stats['name']}.")
    print(f"The {enemy_stats['name']} dealt {player_damage_taken:.0f} damage to you.")
    potions_used_this_turn = 0
    return current_enemy_hp


def start_battle():
    global player_health, potions_used_this_turn
    clear_screen()
    current_enemy = select_random_enemy();
    current_enemy_health = current_enemy['hp']
    print(f"You encounter a wild {current_enemy['name']} (HP: {current_enemy_health:.0f}).");
    time.sleep(1)

    battle_over = False
    while player_health > 0 and current_enemy_health > 0:
        clear_screen()
        print(f"{current_enemy['name']} HP: {current_enemy_health:.0f} | Your HP: {player_health:.0f}")
        print("Choose action: 1. Attack, 2. Use Potion")
        battle_action = msvcrt.getch().decode('utf-8', errors='ignore')

        if battle_action == "1":
            clear_screen();
            current_enemy_health = perform_attack_round(current_enemy_health, current_enemy)
        elif battle_action == "2":
            if potions_used_this_turn >= 3:
                clear_screen();
                print("You've used too many potions this turn! Attack first.");
                time.sleep(1.5);
                continue
            if not any(player_potions_inventory.values()):
                clear_screen();
                print("You have no potions!");
                time.sleep(1.5);
                continue
            clear_screen();
            print("Which potion to use?")
            potion_options_display, valid_potion_choices, choice_num = [], {}, 1
            for p_type_key, p_name in POTION_USE_CHOICES.items():
                if player_potions_inventory.get(p_name, 0) > 0:
                    potion_options_display.append(
                        f"{choice_num}. {ITEM_DISPLAY_NAMES[p_name]} ({player_potions_inventory[p_name]})")
                    valid_potion_choices[str(choice_num)] = p_type_key;
                    choice_num += 1
            if not valid_potion_choices: print("You have no potions available!"); time.sleep(1.5); continue
            for option_str in potion_options_display: print(option_str)
            print("E. Cancel")
            potion_input_choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()
            if potion_input_choice == 'e': continue
            if potion_input_choice in valid_potion_choices:
                use_potion_in_battle(valid_potion_choices[potion_input_choice])
            else:
                clear_screen(); print("Invalid potion selection."); time.sleep(1.5)
        else:
            clear_screen(); print("Invalid action!"); time.sleep(1)

        if player_health <= 0 or current_enemy_health <= 0:
            battle_over = handle_battle_outcome(player_health, current_enemy_health, current_enemy)
            break
        time.sleep(1.5)
    if battle_over: main_game_menu()


def open_skill_shop():
    global player_skill_points
    clear_screen()
    while True:
        print(f"Welcome to the Skill Shop. You have {player_skill_points} skill points.")
        print("What would you like to upgrade?")
        for choice_key, config in SKILL_UPGRADE_CONFIG.items():
            stat_name = ITEM_DISPLAY_NAMES[config['display_key']]
            current_val = globals()[config['var_name']]
            inc = config['increment']
            cost = config['cost']
   
            if "multiplier" in config['display_key']:
                print(
                    f"{choice_key}. {stat_name} (Current: {current_val * 100:.1f}%, +{inc * 100:.1f}%) - Cost: {cost} SP")
            else:
                print(f"{choice_key}. {stat_name} (Current: {current_val:.0f}, +{inc:.0f}) - Cost: {cost} SP")

        print("E. Exit Shop")
        skill_choice = msvcrt.getch().decode('utf-8', errors='ignore').lower();
        clear_screen()

        if skill_choice == 'e': print("Exiting skill shop."); break
        selected_upgrade = SKILL_UPGRADE_CONFIG.get(skill_choice)
        if selected_upgrade:
            if player_skill_points >= selected_upgrade['cost']:
                globals()[selected_upgrade['var_name']] += selected_upgrade['increment']
                player_skill_points -= selected_upgrade['cost']
                new_val_display = globals()[selected_upgrade['var_name']]
                if "multiplier" in selected_upgrade['display_key']: new_val_display *= 100
                print(
                    f"Upgraded {ITEM_DISPLAY_NAMES[selected_upgrade['display_key']]}! New value: {new_val_display:.1f}{'%' if 'multiplier' in selected_upgrade['display_key'] else ''}.")
                print(f"You have {player_skill_points} skill points remaining.")
            else:
                print("Not enough skill points.")
        else:
            print("Invalid choice.")
        time.sleep(2);
        clear_screen()


def main_game_menu():
    clear_screen()
    while True:
        print("Main Menu")
        print(
            f"HP: {player_health:.0f}/{player_max_health:.0f} | Gold: {player_gold} | Lvl: {player_level} ({player_xp:.0f}/{player_xp_to_level_up:.0f} XP) | SP: {player_skill_points}")
        if is_hardcore_mode: print("HARDCORE MODE ACTIVE (NO SAVES)")
        print("1. Battle, 2. Market, 3. Skill Shop, Q. Quit")
        menu_choice = msvcrt.getch().decode('utf-8', errors='ignore').lower()

        if menu_choice == "1":
            start_battle(); break
        elif menu_choice == "2":
            open_market(); clear_screen()
        elif menu_choice == "3":
            open_skill_shop(); clear_screen()
        elif menu_choice == "q":
            print("Exiting game. Goodbye!"); exit()
        else:
            clear_screen(); print("Invalid choice."); time.sleep(1); clear_screen()


if __name__ == "__main__":
    game_loaded_successfully = load_game_state()
    if not game_loaded_successfully:
        ask_for_hardcore_mode()
        print("Starting your adventure...");
        time.sleep(1)
        start_battle()
    else:
        print("Continuing your adventure...");
        time.sleep(1)
        main_game_menu()
