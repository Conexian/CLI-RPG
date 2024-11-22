import os
import random
import msvcrt
import time

_player_first_play = True
_player_defense_potion_in_use = False
_player_strength_potion_in_use = False
_player_alice_stall_first_time = True
_player_unknown_stall_first_time = True
_player_aaron_stall_first_time = True

_player_health = 100
_player_health_max = 100
_player_attack_damage_max = 20
_player_attack_damage_min = 5
_player_healing_potion = 30
_player_defense_potion = 5
_player_strength_potion = 5
_player_potion_abuse_counter = 0
_player_gold = 100
_player_xp = 0
_player_defense = 0
_player_xp_till_level_up = 100
_player_level = 0
_player_critical_hit_mutiplier = 0.1
_player_gold_mutiplier = 0.0

_alice_stock_potions = 5


def clear(): os.system('cls')

_player_potions = {
    'healing': 1,
    'defense': 1,
    'strength': 1
}

_dictionary = {
    "healing": "Healing Potion",
    "defense": "Defense Potion",
    "strength": "Strength Potion"
}


def dev_debug():
    clear()
    print("Stats:")
    print(f"""
_player_first_play = {_player_first_play}
_player_defense_potion_in_use = {_player_defense_potion_in_use}
_player_strength_potion_in_use = {_player_strength_potion_in_use}
_player_alice_stall_first_time = {_player_alice_stall_first_time}
_player_unknown_stall_first_time = {_player_unknown_stall_first_time}
_player_aaron_stall_first_time = {_player_aaron_stall_first_time}

_player_health = {_player_health}
_player_health_max = {_player_health_max}
_player_attack_damage_max = {_player_attack_damage_max}
_player_attack_damage_min = {_player_attack_damage_min}
_player_healing_potion = {_player_healing_potion}
_player_defense_potion = {_player_defense_potion}
_player_strength_potion = {_player_strength_potion}
_player_potion_abuse_counter = {_player_potion_abuse_counter}
_player_gold = {_player_gold}
_player_xp = {_player_xp}
_player_defense = {_player_defense}
_player_xp_till_level_up = {_player_xp_till_level_up}
_player_level = {_player_level}
_player_critical_hit_mutiplier = {_player_critical_hit_mutiplier}
_player_gold_mutiplier = {_player_gold_mutiplier}

_alice_stock_potions = {_alice_stock_potions}

_player_potions = {_player_potions}
_dictionary = {_dictionary}
""")

def random_dialog(_chosen_stall, _type_of_dialog):
    _dialog_data = {
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

    return random.choice(_dialog_data[_chosen_stall][_type_of_dialog])

def purchase(_stall, _item_id):
    global _player_potions, _player_gold

    clear()

    _success = False

    if _stall == 'alice':
        _alice_stall = {
            'healing': {'item_id': '1', 'price': 30},
            'defense': {'item_id': '2', 'price': 40},
            'strength': {'item_id': '3', 'price': 50}
        }

        for _key, _value in _alice_stall.items():
            if _value['item_id'] == _item_id:
                if _value['price'] <= _player_gold:
                    _player_potions[_key] += 1
                    _player_gold -= _value['price']
                    print(f"You purchased a {_key} potion!")
                    _success = True
                    break
                else:
                    print("You don't have enough gold!")
                    break
        else:
            print("Sorry, that item doesn't exist.")

    return _success



def stall(_person):
    global _player_alice_stall_first_time, _player_unknown_stall_first_time, _player_aaron_stall_first_time, _alice_stock_potions

    clear()


    if _person == 'alice':
        if _player_alice_stall_first_time:
            print("Alice: Hey! Welcome to my little stall.")
            time.sleep(2)
            print("Alice: Sooo... Do you want anything?")
            _player_alice_stall_first_time = False

        else:
            if _alice_stock_potions > 0:
                _current_stall_hello = random_dialog('alice', 'hello')
                print(_current_stall_hello)

        while _alice_stock_potions > 0:
            print("What do you want to buy?")
            print("1. Healing potion [40G], 2. Defense potion [50G], 3. Strength potion [60G].")
            print("E. Exit the stall")
            _player_alice_stall_purchase_choice = msvcrt.getch().decode()
            if _player_alice_stall_purchase_choice.lower() == "e":
                bye = random_dialog('alice', 'bye')
                print(bye)
                break

            _success = purchase('alice', _player_alice_stall_purchase_choice)

            if _success:
                _thanks = random_dialog('alice', 'thanks')
                print(_thanks)
                _alice_stock_potions -= 1
        else:
            print("Alice: I'm sorry... I am out of potions.")


def market():
    clear()

    while True:
        print("You are in the market!")
        print("What do you want to do?")
        print("1. Visit Alice's potion stall, 2. Visit the Unknown's weapon stall"
              ", 3. Visit Aaron's armor stall. ")
        print("E. Exit the market")
        _player_action_market = msvcrt.getch().decode()

        if _player_action_market == "1":
            stall('alice')
        elif _player_action_market.lower() == "e":
            break
        else:
            print("Unimplemented!")


def reset_after_battle():
    global _player_defense, _player_attack_damage_max, _player_strength_potion_in_use, _player_defense_potion_in_use, _alice_stock_potions

    if _player_strength_potion_in_use:
        _player_strength_potion_in_use = False

        _player_attack_damage_max -= _player_strength_potion

    if _player_defense_potion_in_use:
        _player_defense_potion_in_use = False

        _player_defense -= _player_defense_potion

    _alice_stock_potions += 3

    if _alice_stock_potions > 5:
        _alice_stock_potions = 5


def potion(_use):
    global _player_potions, _player_health, _player_defense, _player_attack_damage_max, _player_strength_potion_in_use, _player_defense_potion_in_use, _player_potion_abuse_counter

    if _use == "1":
        if _player_potions.get('healing', 0) > 0:
            clear()
            print("Healing potion used!")
            _player_potions['healing'] -= 1

            _player_health += _player_healing_potion
            _player_potion_abuse_counter += 1

            if _player_health > _player_health_max:
                _player_health = _player_health_max

        else:
            clear()
            print("You have no Healing potions!")

    elif _use == "2":
        if _player_defense_potion_in_use:
            clear()
            print("You already have a defense potion in use!")

        else:
            if _player_potions['defense'] > 0:
                clear()
                print("Defense potion used!")
                print(f"Defense increased by {_player_defense_potion}!")
                _player_potions['defense'] -= 1

                _player_defense += _player_defense_potion
                _player_potion_abuse_counter += 1

                _player_defense_potion_in_use = True

            else:
                clear()
                print("You have no Defense potions!")

    elif _use == "3":
        if _player_strength_potion_in_use:
            clear()
            print("You already have a strength potion in use!")

        else:
            if _player_potions['strength'] > 0:
                clear()
                print("Strength potion used!")
                print(f"Strength increased by {_player_strength_potion}!")
                _player_potions['strength'] -= 1

                _player_attack_damage_max += _player_strength_potion
                _player_potion_abuse_counter += 1

                _player_strength_potion_in_use = True

            else:
                clear()
                print("You have no Strength potions!")


def level_check():
    global _player_xp_till_level_up, _player_level, _player_xp

    if _player_level == 0:
        if _player_xp >= 100:
            _player_xp -= 100

            _additional_xp = _player_xp_till_level_up / 4
            _player_xp_till_level_up += round(_additional_xp)
            print(f"You have leveled up! {_player_level} ----> {_player_level + 1}")

            _player_level += 1

    elif _player_level != 0:
        if _player_xp >= _player_xp_till_level_up:
            _player_xp -= _player_xp_till_level_up

            _additional_xp = _player_xp_till_level_up / 4
            _player_xp_till_level_up += round(_additional_xp)
            print(f"You have leveled up! {_player_level} ----> {_player_level + 1}")

            _player_level += 1


def award_gold_and_xp(_enemy_gold, _enemy_xp):
    if _player_gold_mutiplier == 0.0:
        print(f"You were awarded {_enemy_gold} G. And {_enemy_xp} XP.")

        return _enemy_gold, _enemy_xp

    else:
        _mutiplier_increase = _enemy_gold * _player_gold_mutiplier
        _enemy_gold += _mutiplier_increase
        print(f"You were awarded {_enemy_gold:.0f} G. And {_enemy_xp} XP.")

        return _enemy_gold, _enemy_xp


def check_health(_player_health):
    if _player_health <= 0:
        print("You lost lol")
        exit()


def random_enemy():
    _enemies = [
        {'name': 'Wolf', 'hp': 30, 'attack': 10, 'gold': 10, 'xp': 20},
        {'name': 'Mini-Goblin', 'hp': 50, 'attack': 15, 'gold': 20, 'xp': 30}
    ]

    _weights = [6, 4]

    return random.choices(_enemies, weights=_weights, k=1)[0]


def battle():
    global _player_health, _player_gold, _player_xp, _player_potion_abuse_counter

    clear()

    _enemy = random_enemy()
    _current_enemy_health = _enemy['hp']
    _current_enemy_name = _enemy['name']
    print(f"You encounter a wild {_current_enemy_name}.")

    while _player_health > 0 and _current_enemy_health > 0:
        print(f"The {_current_enemy_name} has {_current_enemy_health:.0f} HP!")
        print(f"You have {_player_health} HP.")
        print("1. Attack, 2. Use potion")
        _player_action_battle = msvcrt.getch().decode()

        if _player_action_battle == "1":
            clear()

            _player_damage, _enemy_damage = attack(_current_enemy_health, _player_health, _enemy)

            _current_enemy_health -= _player_damage
            _player_health -= _enemy_damage

            print(f"You dealt {_player_damage:.0f} DMG to the {_current_enemy_name}.")
            print(f"The {_current_enemy_name} dealt {_enemy_damage} DMG to you")

            _player_potion_abuse_counter = 0

        elif _player_action_battle == "2":
            if _player_potion_abuse_counter >= 3:
                clear()
                print("You are using too many potions in a short period of time!")

            elif all(value == 0 for value in _player_potions.values()):
                clear()
                print("You have no potions")

            else:
                clear()
                _potion_choices = {}

                for _i, (_potion_type, _count) in enumerate(_player_potions.items(), start=1):
                    _potion_name = _dictionary.get(_potion_type, _potion_type.capitalize())

                    print(f"{_i}. {_potion_name}: {_count}")

                    _potion_choices[str(_i)] = _potion_type

                print("Which potion do you want to use?")
                _player_action_potion = msvcrt.getch().decode()
                potion(_player_action_potion)

        else:
            clear()
            print("Invalid action!")

    else:
        check_health(_player_health)
        if _current_enemy_health <= 0:
            clear()
            print("You have defeated the enemy!")

            _given_gold, _given_xp = award_gold_and_xp(_enemy['gold'], _enemy['xp'])

            _player_gold += _given_gold
            _player_xp += _given_xp

            level_check()
            reset_after_battle()
            main_menu()

        elif _player_health <= 0:
            clear()
            print("You died lol")
            exit()


def attack(_current_enemy_health, _current_player_health, _enemy):
    _enemy_attack_damage = random.randint(1, _enemy['attack'])
    _player_attack_damage = random.randint(_player_attack_damage_min, _player_attack_damage_max)

    if random.randint(1, 4) == 4:
        _critical_hit_damage = _player_attack_damage_max * _player_critical_hit_mutiplier
        _player_attack_damage += _critical_hit_damage

    return _player_attack_damage, _enemy_attack_damage


def main_menu():
    while True:
        print("You are in the main menu.")
        print("What do you want to do?")
        print("1. Battle, 2. Market, 3. Debug.")

        _player_action_menu = msvcrt.getch().decode()

        if _player_action_menu == "1":
            battle()
        elif _player_action_menu == "2":
            market()
        elif _player_action_menu == "3":
            dev_debug()


def main():
    battle()


if __name__ == "__main__":
    if _player_first_play:
        _player_first_play = False
        battle()
    else:
        main_menu()
