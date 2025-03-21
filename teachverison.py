import json
import random
import time
import os
import threading

try:
    from playsound import playsound
except ImportError:
    playsound = None

# 全局变量
player_hp = 100
player_max_hp = 100
player_armor = 100
player_max_armor = 100
player_money = 3000
inventory = []
offsite_team = []
associates = {}
alarm_triggered = False
have_vault_key = False

getaway_vehicle = True
getaway_fly = True
enemy_hp = 0
enemy_damage = 0

# 保存和加载游戏状态
def save_game(state):
    try:
        with open("savegame.json", "w") as f:
            json.dump(state, f)
        print("\n[Game saved successfully.]\n")
    except Exception as e:
        print("\n[Save failed:", e, "]\n")

def load_game():
    try:
        with open("savegame.json", "r") as f:
            state = json.load(f)
        print("\n[Game loaded successfully.]\n")
        return state
    except Exception as e:
        print("\n[Load failed:", e, "]\n")
        return None

# 播放音频（仅用于金库抢劫倒计时）
def play_audio(sound_path):
    if playsound:
        try:
            threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
        except Exception as e:
            print("[Audio playback failed:", e, "]")

def roll_dice():
    return random.randint(1, 6)

# 同伙技能函数
def skill_fool():
    global enemy_hp, player_hp
    enemy_hp -= 10
    print("\n[Fool skill activated: enemy loses 10 HP.]")
    if random.random() < 0.1:
        player_hp -= 10
        print("[Fool backlash: you lose 10 HP!]")

def skill_retired_military():
    global enemy_hp
    enemy_hp -= 5
    print("\n[Retired Military skill activated: enemy loses 5 HP.]")

def skill_robot_manufacturer():
    print("\n[Robot Manufacturer skill activated: For the next 3 rounds, you take half damage. (Effect simulated)]")

def skill_teacher():
    print("\n[Teacher skill activated: 50% chance to resurrect if you die; enemy damage may be reduced.]")

def skill_sam():
    global player_hp, player_max_hp
    player_hp *= 2
    player_max_hp *= 2
    print("\n[SAM skill activated: Your HP is doubled.]")

def print_divider():
    print("-" * 40)

# 游戏开始介绍
def introduction():
    print("\nWelcome to RMC Bank Robbery!")
    print("\nYou are a professional thief planning a high-risk, high-reward bank heist.")
    print("Before you begin, you must prepare your equipment, recruit personnel,")
    print("and choose the best approach to infiltrate the bank.")
    print("\nType 'start' to begin the game or 'load' to load a saved game.")
    choice = input("\nPlease enter your choice: ").strip().lower()
    if choice == "start":
        equipment_shop()
    elif choice == "load":
        state = load_game()
        if state:
            restore_state(state)
        else:
            introduction()
    else:
        print("\nInvalid choice. Try again.")
        introduction()

# 装备商店阶段
def equipment_shop():
    global player_money, inventory
    print("\n[Equipment Shop]")
    print("\nYou have $" + str(player_money) + " to spend on equipment.")
    shop_items = [
        {"name": "Camouflage Suit", "price": 500, "desc": "Improves stealth."},
        {"name": "Hacking Tool", "price": 500, "desc": "Helps breach side doors silently."},
        {"name": "Thermite", "price": 1000, "desc": "Used to blast open the vault door."},
        {"name": "Security Uniform", "price": 800, "desc": "Enables bribery of security."},
        {"name": "Kevlar Vest", "price": 300, "desc": "Increases your armor."},
        {"name": "Decoy Crew", "price": 600, "desc": "Distracts enemies during escape."},
        {"name": "Getaway Vehicle", "price": 1200, "desc": "Essential for a fast land escape."},
        {"name": "Tarkov Backpack", "price": 400, "desc": "Increases capacity and reduces money loss."},
        {"name": "Heavy Firepower", "price": 1500, "desc": "Boosts combat damage."},
        {"name": "Lucky Charm", "price": 200, "desc": "May increase your chance to avoid damage."}
    ]
    for item in shop_items:
        print_divider()
        print("Item: " + item["name"])
        print("Price: $" + str(item["price"]))
        print("Description: " + item["desc"])
    print_divider()
    print("\nType the name of an item to purchase it, or type 'done' when finished.")
    choice = input("Your choice: ").strip()
    if choice.lower() == "done":
        personnel_recruitment()
    else:
        found = False
        for item in shop_items:
            if choice.lower() == item["name"].lower():
                found = True
                if item["name"] in inventory:
                    print("\nYou have already purchased " + item["name"] + ".")
                else:
                    if player_money >= item["price"]:
                        player_money -= item["price"]
                        inventory.append(item["name"])
                        print("\nYou purchased " + item["name"] + ".")
                        if item["name"] == "Kevlar Vest":
                            global player_max_armor, player_armor
                            player_max_armor = 150
                            player_armor = 150
                    else:
                        print("\nInsufficient funds to purchase " + item["name"] + ".")
                break
        if not found:
            print("\nThat item is not available. Please try again.")
        print("\nCurrent Money: $" + str(player_money))
        equipment_shop()

# 人员招聘阶段
def personnel_recruitment():
    print("\n[Personnel Recruitment]")
    print("You can recruit support in two ways:")
    print("1. Offsite Assistance (hire professionals with money).")
    print("2. Associates (recruit accomplices for a share of the loot with special skills).")
    print("Type 'offsite' or 'associates' to choose.")
    choice = input("\nYour choice: ").strip().lower()
    if choice == "offsite":
        recruitment_offsite()
    elif choice == "associates":
        recruitment_associates()
    else:
        print("\nInvalid choice. Try again.")
        personnel_recruitment()

def recruitment_offsite():
    global player_money, offsite_team
    print("\n[Offsite Assistance]")
    offsite_options = [
        {"name": "Hacker", "price": 500},
        {"name": "Security Personnel", "price": 800},
        {"name": "Guard Equipment Manufacturer", "price": 1000},
        {"name": "IT Specialist", "price": 600},
        {"name": "Logistics Manager", "price": 700}
    ]
    for option in offsite_options:
        print_divider()
        print("Option: " + option["name"] + " - $" + str(option["price"]))
    print_divider()
    print("\nEnter the name of the person to hire, or type 'done' when finished:")
    choice = input("Your choice: ").strip()
    if choice.lower() == "done":
        recruitment_associates()
    else:
        found = False
        for option in offsite_options:
            if choice.lower() == option["name"].lower():
                found = True
                if option["name"] in offsite_team:
                    print("\nYou have already hired " + option["name"] + ".")
                else:
                    if player_money >= option["price"]:
                        player_money -= option["price"]
                        offsite_team.append(option["name"])
                        print("\nYou hired " + option["name"] + ".")
                    else:
                        print("\nNot enough funds to hire " + option["name"] + ".")
                break
        if not found:
            print("\nThat option is not available.")
        print("\nCurrent Money: $" + str(player_money))
        recruitment_offsite()

def recruitment_associates():
    global associates
    print("\n[Associates Recruitment]")
    associates_options = [
        {"name": "Fool", "share": 10, "desc": "Deals 10 damage to all enemies (10% backlash).", "skill": skill_fool},
        {"name": "Retired Military", "share": 30, "desc": "Deals 5 damage to several enemies.", "skill": skill_retired_military},
        {"name": "Robot Manufacturer", "share": 70, "desc": "Boosts damage and halves damage taken.", "skill": skill_robot_manufacturer},
        {"name": "Teacher", "share": 50, "desc": "50% chance to resurrect and may reduce enemy damage.", "skill": skill_teacher},
        {"name": "SAM", "share": 0, "desc": "Test mode: doubles your HP and damage.", "skill": skill_sam},
        {"name": "Medic", "share": 20, "desc": "Can heal you during combat.", "skill": lambda: print("\n[Medic skill activated: Healing effect simulated.]")},
        {"name": "Scout", "share": 15, "desc": "Provides intel on enemy positions.", "skill": lambda: print("\n[Scout skill activated: Intel gathered.]")}
    ]
    for option in associates_options:
        print_divider()
        print("Associate: " + option["name"])
        print("Share: " + str(option["share"]) + "%")
        print("Description: " + option["desc"])
    print_divider()
    print("\nEnter the name of an associate to recruit, or type 'done' when finished:")
    choice = input("Your choice: ").strip()
    if choice.lower() == "done":
        approach_selection()
    else:
        found = False
        for option in associates_options:
            if choice.lower() == option["name"].lower():
                found = True
                if option["name"] in associates:
                    print("\nYou have already recruited " + option["name"] + ".")
                else:
                    associates[option["name"]] = {"share": option["share"], "desc": option["desc"], "used": False, "skill": option["skill"]}
                    print("\nYou recruited " + option["name"] + ".")
                break
        if not found:
            print("\nThat option is not available.")
        recruitment_associates()

# 选择接近银行方式
def approach_selection():
    print("\n[Approach Selection]")
    print("How do you want to approach the bank?")
    print_divider()
    print("'walk'    - Approach on foot")
    print("'vehicle' - Use a land vehicle")
    print("'fly'     - Use a flying vehicle")
    print("'sneak'   - Use a stealth route")
    print_divider()
    choice = input("Please enter your choice: ").strip().lower()
    if choice == "walk":
        walk_route()
    elif choice == "vehicle":
        land_vehicle_route()
    elif choice == "fly":
        flying_vehicle_route()
    elif choice == "sneak":
        stealth_route()
    else:
        print("\nInvalid choice. Try again.")
        approach_selection()

# 徒步接近分支
def walk_route():
    print("\n[On Foot Approach]")
    print("You chose to approach on foot.")
    print("Options:")
    print_divider()
    print("'main'    - Enter through the main entrance (requires Camouflage Suit)")
    print("'side'    - Enter through the side door (requires Hacking Tool)")
    print("'detour'  - Take a detour to avoid confrontation")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "main":
        main_entrance_route()
    elif choice == "side":
        side_door_route()
    elif choice == "detour":
        detour_route()
    else:
        print("\nInvalid choice. Try again.")
        walk_route()

def detour_route():
    print("\n[Detour Route]")
    if random.random() < 0.5:
        print("Your detour is successful; you slip in through a back window!")
        global have_vault_key
        have_vault_key = False
        vault_phase()
    else:
        print("Your detour fails and an alarm is triggered!")
        global alarm_triggered
        alarm_triggered = True
        combat("Detour Guard", 35, 12)
        print("After the failed detour, choose an alternate approach.")
        approach_selection()

# 陆地载具分支
def land_vehicle_route():
    print("\n[Land Vehicle Approach]")
    if "Getaway Vehicle" in inventory:
        print("You have a Getaway Vehicle.")
        print("Options:")
        print_divider()
        print("'crash'   - Crash through the bank door (high risk, triggers alarm)")
        print("'circle'  - Circle around for a stealthier entry")
        print_divider()
        choice = input("Enter your choice: ").strip().lower()
        if choice == "crash":
            alarm_triggered_route()
        elif choice == "circle":
            print("You circle around and find a less guarded side entrance.")
            side_door_route()
        else:
            print("Invalid choice. Try again.")
            land_vehicle_route()
    else:
        print("You did not purchase a Getaway Vehicle. This route is unavailable.")
        approach_selection()

def alarm_triggered_route():
    global alarm_triggered
    print("\nAs you crash into the bank, alarms blare!")
    alarm_triggered = True
    combat("Front Door Guards", 35, 12)
    land_entry_after_combat()

def land_entry_after_combat():
    print("\nAfter the crash, you learn that a guard with the vault key is in the lobby.")
    print("Options:")
    print_divider()
    print("'assassinate' - Silent kill (requires Knife)")
    print("'fight'       - Engage in a firefight")
    print("'bribe'       - Bribe the guard (requires Security Uniform)")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "assassinate":
        if "Knife" in inventory:
            print("You silently kill the guard and obtain the key.")
            global have_vault_key
            have_vault_key = True
            after_key_obtained()
        else:
            print("You don't have a Knife! Your attempt fails and triggers the alarm.")
            global alarm_triggered
            alarm_triggered = True
            combat("Key Guard", 40, 15)
            after_key_obtained()
    elif choice == "fight":
        print("You choose to engage in a firefight!")
        alarm_triggered = True
        combat("Key Guard", 40, 15)
        after_key_obtained()
    elif choice == "bribe":
        if "Security Uniform" in inventory:
            print("You successfully bribe the guard to hand over the key.")
            have_vault_key = True
            after_key_obtained()
        else:
            print("You don't have a Security Uniform! Bribe fails.")
            combat("Key Guard", 40, 15)
            after_key_obtained()
    else:
        print("Invalid choice. Try again.")
        land_entry_after_combat()

# 飞行载具分支
def flying_vehicle_route():
    print("\n[Flying Vehicle Approach]")
    if getaway_fly:
        print("You are brought to the bank rooftop by helicopter.")
        print("Options on the roof:")
        print_divider()
        print("'search' - Search for the guard with the vault key")
        print("'blast'  - Use Thermite to blast the vault door directly")
        print("'wait'   - Wait to observe security patterns")
        print_divider()
        choice = input("Enter your choice: ").strip().lower()
        if choice == "search":
            roof_search_route()
        elif choice == "blast":
            roof_direct_blast()
        elif choice == "wait":
            print("You wait and notice that security seems less intense.")
            global alarm_triggered
            alarm_triggered = False
            roof_search_route()
        else:
            print("Invalid choice. Try again.")
            flying_vehicle_route()
    else:
        print("You did not purchase the necessary equipment for a flying approach.")
        approach_selection()

# 额外的偷渡分支
def stealth_route():
    print("\n[Stealth Route]")
    print("You choose a stealthy approach, avoiding main entrances.")
    print("Options:")
    print_divider()
    print("'tunnel' - Infiltrate via maintenance tunnel")
    print("'window' - Sneak in through a side window")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "tunnel":
        print("You slip into the bank through the tunnel undetected.")
        global have_vault_key
        have_vault_key = False
        vault_phase()
    elif choice == "window":
        if random.random() < 0.5:
            print("You successfully sneak in and spot a guard with the key!")
            main_entrance_after_combat()
        else:
            print("You fail to find a guard with the key; you'll have to blast the vault.")
            have_vault_key = False
            vault_phase()
    else:
        print("Invalid choice. Try again.")
        stealth_route()

# 正门分支
def main_entrance_route():
    global alarm_triggered, have_vault_key
    print("\n[Main Entrance Route]")
    print("You attempt to enter through the main entrance.")
    if "Camouflage Suit" in inventory:
        if random.random() < 0.15:
            print("Even with your Camouflage Suit, a guard spots you!")
            alarm_triggered = True
            combat("Main Entrance Guard", 30, 10)
            main_entrance_after_combat()
        else:
            print("Your suit helps you blend in; you enter undetected.")
            main_entrance_after_combat()
    else:
        print("Without a Camouflage Suit, you are immediately spotted!")
        alarm_triggered = True
        combat("Main Entrance Guard", 30, 10)
        main_entrance_after_combat()

def main_entrance_after_combat():
    print("\nAfter the main entrance confrontation, you learn that a guard holding the vault key is nearby.")
    print("Options:")
    print_divider()
    print("'assassinate' - Attempt a silent assassination (requires Knife)")
    print("'fight'       - Engage in a firefight")
    print("'sneak'       - Try to sneak past and steal the key")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "assassinate":
        if "Knife" in inventory:
            print("You silently kill the guard and secure the key.")
            global have_vault_key
            have_vault_key = True
            after_key_obtained()
        else:
            print("You don't have a Knife! Your attempt fails and the alarm triggers.")
            global alarm_triggered
            alarm_triggered = True
            combat("Key Guard", 40, 15)
            after_key_obtained()
    elif choice == "fight":
        print("You engage the guard in a firefight!")
        alarm_triggered = True
        combat("Key Guard", 40, 15)
        after_key_obtained()
    elif choice == "sneak":
        if random.random() < 0.5:
            print("You successfully sneak past and steal the key.")
            have_vault_key = True
            after_key_obtained()
        else:
            print("Your sneaking fails; the guard notices you!")
            alarm_triggered = True
            combat("Key Guard", 40, 15)
            after_key_obtained()
    else:
        print("Invalid choice. Try again.")
        main_entrance_after_combat()

# 侧门分支
def side_door_route():
    global alarm_triggered, have_vault_key
    print("\n[Side Door Route]")
    print("You choose to enter through the side door.")
    if "Hacking Tool" in inventory:
        if random.random() < 0.10:
            print("Even with your Hacking Tool, a system glitch causes detection!")
            alarm_triggered = True
            combat("Side Door Guard", 30, 10)
            side_door_after_combat()
        else:
            print("Your Hacking Tool allows you to bypass security silently.")
            side_door_after_combat()
    else:
        print("Without a Hacking Tool, forcing the door triggers an alarm!")
        alarm_triggered = True
        combat("Side Door Guard", 30, 10)
        side_door_after_combat()

def side_door_after_combat():
    print("\nAfter the side door encounter, you see a guard with the vault key.")
    print("Options:")
    print_divider()
    print("'assassinate' - Try a silent kill (requires Knife)")
    print("'fight'       - Engage in combat")
    print("'distract'    - Create a distraction to steal the key (requires Decoy Crew)")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "assassinate":
        if "Knife" in inventory:
            print("You silently eliminate the guard and secure the key.")
            global have_vault_key
            have_vault_key = True
            after_key_obtained()
        else:
            print("You lack a Knife! Your attempt fails and triggers an alarm.")
            alarm_triggered = True
            combat("Key Guard", 40, 15)
            after_key_obtained()
    elif choice == "fight":
        print("You engage the guard in combat!")
        alarm_triggered = True
        combat("Key Guard", 40, 15)
        after_key_obtained()
    elif choice == "distract":
        if "Decoy Crew" in inventory:
            print("You deploy your Decoy Crew to distract the guard and steal the key.")
            have_vault_key = True
            after_key_obtained()
        else:
            print("You do not have Decoy Crew; distraction fails.")
            combat("Key Guard", 40, 15)
            after_key_obtained()
    else:
        print("Invalid choice. Try again.")
        side_door_after_combat()

# 屋顶分支
def roof_search_route():
    print("\n[Roof Search Route]")
    print("You stealthily descend from the rooftop and locate a guard holding the vault key.")
    print("Options:")
    print_divider()
    print("'assassinate' - Attempt a silent kill (requires Knife)")
    print("'fight'       - Engage in combat")
    print("'sneak'       - Try to sneak by and steal the key")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "assassinate":
        if "Knife" in inventory:
            print("You silently take down the guard and secure the key.")
            global have_vault_key
            have_vault_key = True
            after_key_obtained()
        else:
            print("You don't have a Knife! Your attempt fails and triggers the alarm.")
            global alarm_triggered
            alarm_triggered = True
            combat("Key Guard", 40, 15)
            after_key_obtained()
    elif choice == "fight":
        print("You engage the guard in a firefight!")
        alarm_triggered = True
        combat("Key Guard", 40, 15)
        after_key_obtained()
    elif choice == "sneak":
        if random.random() < 0.5:
            print("Your sneaking is successful and you steal the key!")
            have_vault_key = True
            after_key_obtained()
        else:
            print("Your sneaking fails; the guard notices!")
            alarm_triggered = True
            combat("Key Guard", 40, 15)
            after_key_obtained()
    else:
        print("Invalid choice. Try again.")
        roof_search_route()

def roof_direct_blast():
    print("\n[Roof Direct Blast]")
    global alarm_triggered, have_vault_key
    alarm_triggered = True
    have_vault_key = False
    print("You bypass any guard and set up Thermite to blast the vault door. The explosion opens the vault!")
    vault_phase()

# 获得钥匙后分支
def after_key_obtained():
    print("\nYou now have the vault key!")
    print("Before heading to the vault, choose an option:")
    print_divider()
    print("'wait'  - Wait a moment to observe bank security (reduces alarm intensity)")
    print("'rush'  - Rush immediately to the vault")
    print("'bribe' - Bribe a nearby guard to lower security (requires Security Uniform)")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "wait":
        print("You wait and observe; the alarm intensity decreases.")
        global alarm_triggered
        alarm_triggered = False
        vault_phase()
    elif choice == "rush":
        vault_phase()
    elif choice == "bribe":
        if "Security Uniform" in inventory:
            print("You successfully bribe a guard; security is reduced.")
            alarm_triggered = False
            vault_phase()
        else:
            print("You don't have a Security Uniform. Proceeding with rush.")
            vault_phase()
    else:
        print("Invalid option. Try again.")
        after_key_obtained()

# 金库抢劫阶段
def vault_phase():
    print("\n[Vault Phase]")
    if have_vault_key:
        print("You use the key to unlock the vault door. It creaks open, revealing stacks of cash.")
        if alarm_triggered:
            print("But the alarms are still blaring!")
    else:
        print("Without a key, you use Thermite to blast open the vault door!")
        print("An explosion rocks the bank as the vault door bursts open!")
    print("\nBegin looting the vault!")
    vault_looting_game()

def vault_looting_game():
    global player_money
    print("\n[Vault Looting]")
    loot_time = 30 if alarm_triggered else 60
    print("You have " + str(loot_time) + " seconds to grab as much money as possible.")
    print("Type the number of 'clicks' you achieve (each click earns $1000, maximum $100000).")
    try:
        clicks = int(input("Enter number of clicks: "))
    except:
        print("Invalid input, assuming 0 clicks.")
        clicks = 0
    money_gained = clicks * 1000
    if money_gained > 100000:
        money_gained = 100000
    print("You grabbed $" + str(money_gained) + " from the vault!")
    player_money += money_gained
    after_loot_phase(money_gained)

# 逃脱阶段
def after_loot_phase(loot):
    print("\n[Escape Phase]")
    print("Now you must escape the bank!")
    print("Options:")
    print_divider()
    print("'backdoor' - Escape via the back door (may face pursuing enemies)")
    print("'sewer'    - Escape through the sewers (stealthy but long)")
    print("'direct'   - Run straight out of the lobby (high risk)")
    print("'window'   - Escape through a side window (if available)")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "backdoor":
        escape_backdoor()
    elif choice == "sewer":
        escape_sewer()
    elif choice == "direct":
        escape_direct()
    elif choice == "window":
        escape_window()
    else:
        print("Invalid choice. Try again.")
        after_loot_phase(loot)

def escape_backdoor():
    print("\n[Backdoor Escape]")
    print("You exit through the back door. Enemies are pursuing you!")
    print("Options:")
    print_divider()
    print("'fight'  - Engage in combat with pursuers")
    print("'assist' - Activate an associate's skill for help")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "fight":
        combat("Pursuing Enemies", 40, 15)
        escape_success()
    elif choice == "assist":
        if associates:
            activate_associate_skill()
            escape_success()
        else:
            print("No associates available. You must fight!")
            combat("Pursuing Enemies", 40, 15)
            escape_success()
    else:
        print("Invalid option. Try again.")
        escape_backdoor()

def escape_sewer():
    print("\n[Sewer Escape]")
    print("You choose to escape through the sewers.")
    print("Options:")
    print_divider()
    print("'run'     - Run quickly (risk of hostile encounters)")
    print("'stealth' - Proceed slowly and carefully")
    print_divider()
    choice = input("Enter your choice: ").strip().lower()
    if choice == "run":
        if random.random() < 0.3:
            print("While running, you encounter hostile figures!")
            combat("Sewer Hostiles", 30, 10)
            escape_success()
        else:
            escape_success()
    elif choice == "stealth":
        print("Your careful movement helps you avoid danger.")
        escape_success()
    else:
        print("Invalid choice. Try again.")
        escape_sewer()

def escape_direct():
    print("\n[Direct Escape]")
    print("You decide to run straight out of the lobby!")
    combat("Lobby Security", 50, 20)
    if "Decoy Crew" in inventory:
        print("Do you want to deploy your Decoy Crew to distract security? (yes/no)")
        choice = input("Your choice: ").strip().lower()
        if choice == "yes":
            print("You deploy your Decoy Crew and security is momentarily distracted!")
    escape_success()

def escape_window():
    print("\n[Window Escape]")
    print("You choose to escape through a side window.")
    if random.random() < 0.5:
        print("The window escape is smooth; you evade security easily!")
        escape_success()
    else:
        print("The window is guarded! You must fight.")
        combat("Window Guards", 35, 12)
        escape_success()

def escape_success():
    print("\n[Escape Successful]")
    print("After a tense escape, you finally get away!")
    print("Your final loot plus your starting money brings your total money to $" + str(player_money) + ".")
    print("\nCongratulations, you have completed the heist!")
    print("Do you want to play again? (yes/no)")
    choice = input("Your choice: ").strip().lower()
    if choice == "yes":
        reset_game()
    else:
        print("Thank you for playing RMC Bank Robbery!")
        exit()

# 近战和远程交战系统
def game_over():
    pass


def combat(enemy_name, enemy_initial_hp, enemy_damage):
    global player_hp, player_armor, enemy_hp
    enemy_hp = enemy_initial_hp
    print("\n[Combat with " + enemy_name + "]")
    round_number = 1
    while enemy_hp > 0 and player_hp > 0:
        print_divider()
        print("Round " + str(round_number))
        input("Press Enter to roll the dice...")
        player_roll = roll_dice()
        enemy_roll = roll_dice()
        print("You rolled: " + str(player_roll))
        print(enemy_name + " rolled: " + str(enemy_roll))
        if player_roll == enemy_roll:
            print("It's a tie. No damage dealt.")
        elif player_roll > enemy_roll:
            damage = 15
            if "Heavy Firepower" in inventory:
                damage = 30
            elif "Getaway Vehicle" in inventory:
                damage = 25
            enemy_hp -= damage
            print("You hit " + enemy_name + " for " + str(damage) + " damage!")
        else:
            damage = enemy_damage
            if player_armor > 0:
                if player_armor >= damage:
                    player_armor -= damage
                    damage = 0
                    print(enemy_name + " attacks, but your armor absorbs the damage!")
                else:
                    damage -= player_armor
                    player_armor = 0
                    print(enemy_name + " attacks and breaks your armor, dealing " + str(damage) + " damage!")
            else:
                player_hp -= damage
                print(enemy_name + " attacks you for " + str(damage) + " damage!")
        print("Your HP: " + str(player_hp) + " | Armor: " + str(player_armor))
        print(enemy_name + " HP: " + str(enemy_hp))
        round_number += 1
        if player_hp <= 0:
            break
    if player_hp <= 0:
        game_over()
    else:
        print("\nYou defeated " + enemy_name + "!")
        time.sleep(1)

# 激活同伙技能
def activate_associate_skill():
    global associates
    available = [name for name, data in associates.items() if not data.get("used", False)]
    if available:
        assoc_name = available[0]
        print("\nActivating " + assoc_name + "'s skill...")
        skill_func = associates[assoc_name]["skill"]
        skill_func()
        associates[assoc_name]["used"] = True
    else:
        print("\nNo associate skills available.")
    time.sleep(1)

# 重置游戏状态
def reset_game():
    global player_hp, player_max_hp, player_armor, player_max_armor, player_money
    global inventory, offsite_team, associates, alarm_triggered, have_vault_key
    player_hp = 100
    player_max_hp = 100
    player_armor = 100
    player_max_armor = 100
    player_money = 3000
    inventory.clear()
    offsite_team.clear()
    associates.clear()
    alarm_triggered = False
    have_vault_key = False
    print("\n[Game reset.]\n")
    introduction()

# 从存档恢复状态
def restore_state(state):
    global player_hp, player_max_hp, player_armor, player_max_armor, player_money
    global inventory, offsite_team, associates, alarm_triggered, have_vault_key
    player_hp = state.get("player_hp", 100)
    player_max_hp = state.get("player_max_hp", 100)
    player_armor = state.get("player_armor", 100)
    player_max_armor = state.get("player_max_armor", 100)
    player_money = state.get("player_money", 3000)
    inventory[:] = state.get("inventory", [])
    offsite_team[:] = state.get("offsite_team", [])
    associates.clear()
    for name in state.get("associates", []):
        associates[name] = {"share": 0, "desc": "", "used": False}
    alarm_triggered = state.get("alarm_triggered", False)
    have_vault_key = state.get("have_vault_key", False)
    print("\n[State restored successfully.]\n")
    approach_selection()

# 主函数
def main():
    print("=== RMC Bank Robbery ===")
    print("\nWould you like to load a saved game? (yes/no)")
    choice = input("Your choice: ").strip().lower()
    if choice == "yes":
        state = load_game()
        if state:
            restore_state(state)
        else:
            introduction()
    else:
        introduction()

# 额外分支增强游戏选择
def extra_branch_choice():
    print("\n[Extra Branch]")
    print("You find a mysterious note on the floor. Do you want to read it? (yes/no)")
    choice = input("Your choice: ").strip().lower()
    if choice == "yes":
        print("The note reads: 'Every choice matters. Choose wisely.'")
    else:
        print("You ignore the note and move on.")
    time.sleep(1)

def extra_shop_branch():
    print("\n[Extra Shop Option]")
    print("A rare item 'Energy Drink' is available for $150.")
    print("It restores 20 HP.")
    choice = input("Do you want to buy it? (yes/no): ").strip().lower()
    global player_money, inventory, player_hp, player_max_hp
    if choice == "yes":
        if player_money >= 150:
            player_money -= 150
            inventory.append("Energy Drink")
            player_hp = min(player_hp + 20, player_max_hp)
            print("You bought an Energy Drink and restored 20 HP!")
        else:
            print("Not enough money.")
    else:
        print("You decided not to buy the Energy Drink.")
    time.sleep(1)

def extra_escape_option():
    print("\n[Extra Escape Option]")
    print("On your escape, you notice an abandoned motorcycle.")
    print("Do you want to use it for a faster exit? (yes/no)")
    choice = input("Your choice: ").strip().lower()
    if choice == "yes":
        print("You hop on the motorcycle and speed away, evading enemies easily!")
    else:
        print("You stick to your chosen escape route.")
    time.sleep(1)

if __name__ == "__main__":
    extra_branch_choice()
    extra_shop_branch()
    extra_escape_option()
    main()
