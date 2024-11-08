import random
import msvcrt

_player_health = 100
_player_health_max = 100
_player_attack_damage_max = 20
_player_attack_damage_min = 5
_player_healing_potion = 30
_player_defense_potion_in_use = False
_player_defense_potion = 5
_player_strength_potion_in_use = False
_player_strength_potion = 5
_player_gold = 100
_player_xp = 0
_player_defense = 0
_player_xp_till_level_up = 100
_player_level = 0
_player_critical_hit_mutiplier = 0.1
_player_gold_mutiplier = 0.0

_player_potions = {
    'healing': 2,
    'defense': 0,
    'strength': 0
}

_dictionary = {
    "healing": "Healing Potion",
    "defense": "Defense Potion",
    "strength": "Strength Potion"
}


def dev_debug():
    print("Stats:")
    print(f"""
_player_health = {_player_health}
_player_health_max = {_player_health_max}
_player_attack_damage_max = {_player_attack_damage_max}
_player_attack_damage_min = {_player_attack_damage_min}
_player_healing_potion = {_player_healing_potion}
_player_defense_potion_in_use = {_player_defense_potion_in_use}
_player_defense_potion = {_player_defense_potion}
_player_strength_potion_in_use = {_player_strength_potion_in_use}
_player_strength_potion = {_player_strength_potion}
_player_gold = {_player_gold}
_player_xp = {_player_xp}
_player_defense = {_player_defense}
_player_xp_till_level_up = {_player_xp_till_level_up}
_player_level = {_player_level}
_player_critical_hit_mutiplier = {_player_critical_hit_mutiplier}
_player_gold_mutiplier = {_player_gold_mutiplier}
_player_potions = {_player_potions}
_dictionary = {_dictionary}
""")

def reset_after_battle():
    global _player_defense, _player_attack_damage_max, _player_strength_potion_in_use, _player_defense_potion_in_use

    if _player_strength_potion_in_use:
        _player_strength_potion_in_use = False

        _player_attack_damage_max -= _player_strength_potion

    if _player_defense_potion_in_use:
        _player_defense_potion_in_use = False

        _player_defense -= _player_defense_potion


def potion(_use):
    global _player_potions, _player_health, _player_defense, _player_attack_damage_max, _player_strength_potion_in_use, _player_defense_potion_in_use

    if _use == "1":
        if _player_potions['healing'] > 0:
            print("Healing potion used!")
            _player_potions['healing'] -= 1

            _player_health += _player_healing_potion

            if _player_health > _player_health_max:
                _player_health = _player_health_max

        else:
            print("You have no Healing potions!")

    elif _use == "2":
        if _player_defense_potion_in_use:
            print("You already have a defense potion in use!")

        else:
            if _player_potions['defense'] > 0:
                print("Defense potion used!")
                print(f"Defense increased by {_player_defense_potion}!")
                _player_potions['defense'] -= 1

                _player_defense += _player_defense_potion

                _player_defense_potion_in_use = True

            else:
                print("You have no Defense potions!")

    elif _use == "3":
        if _player_strength_potion_in_use:
            print("You already have a strength potion in use!")

        else:
            if _player_potions['strength'] > 0:
                print("Strength potion used!")
                print(f"Strength increased by {_player_strength_potion}!")
                _player_potions['strength'] -= 1

                _player_attack_damage_max += _player_strength_potion

                _player_strength_potion_in_use = True

            else:
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
    global _player_health, _player_gold, _player_xp

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
            _player_damage, _enemy_damage = attack(_current_enemy_health, _player_health, _enemy)

            _current_enemy_health -= _player_damage
            _player_health -= _enemy_damage

            print(f"You dealt {_player_damage:.0f} DMG to the {_current_enemy_name}.")
            print(f"The {_current_enemy_name} dealt {_enemy_damage} DMG to you")

        elif _player_action_battle == "2":
            if _player_potions:

                _potion_choices = {}

                for _i, (_potion_type, _count) in enumerate(_player_potions.items(), start=1):
                    potion_name = _dictionary.get(_potion_type, _potion_type.capitalize())

                    print(f"{_i}. {potion_name}: {_count}")

                    _potion_choices[str(_i)] = _potion_type

                print("Which potion do you want to use?")
                _player_action_potion = msvcrt.getch().decode()

            else:
                print("You have no potions!")

    else:
        if _current_enemy_health <= 0:
            print("You have defeated the enemy!")

            _given_gold, _given_xp = award_gold_and_xp(_enemy['gold'], _enemy['xp'])

            _player_gold += _given_gold
            _player_xp += _given_xp

            level_check()
            reset_after_battle()
            main_menu()

        elif _player_health <= 0:
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
    check_health(_player_health)
    while True:
        print("You are in the main menu.")
        print("What do you want to do?")
        print("1. Battle. 2. Debug")

        _player_action_menu = msvcrt.getch().decode()

        if _player_action_menu == "1":
            battle()
        elif _player_action_menu == "2":
            dev_debug()


def main():
    battle()


if __name__ == "__main__":
    main()