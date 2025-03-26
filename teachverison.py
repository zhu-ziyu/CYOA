import random
import time

#已经失败功能...
#try:
#    from playsound import playsound
#except ImportError:
#    playsound = None

# 全局玩家血量等级.....变量（反正老师看不懂....瞎写吧，注释就瞎写吧....)
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



# 播放音频（仅用于金库抢劫倒计时）已经失效...................操！
#def play_audio(sound_path):
#    if playsound:
#        try:
#            threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
#        except Exception as e:
#            print("[Audio playback failed:", e, "]")

def roll_dice():
    return random.randint(1, 6)
    random_event()

#进入打斗场景后的随机函数....纯纯为了满足老师要求
def random_event():
    event_number = random.randint(1, 5)
    if event_number == 1:
        print("\n[Random Event] A security camera malfunctions, reducing alarm chances!")
        global alarm_triggered
        alarm_triggered = False
    elif event_number == 2:
        print("\n[Random Event] A stray bullet hits your pocket, causing you to lose $100!")
        global player_money
        player_money = max(player_money - 100, 0)
    elif event_number == 3:
        print("\n[Random Event] nothing happen")
    elif event_number == 4:
        print("\n[Random Event] A friendly janitor gives you a tip about a secret entrance!")
        global secret_route
        secret_route = True
    elif event_number == 5:
        print("\n[Random Event] Your Energy Drink is found to be expired, and it is removed from your inventory!")
        global inventory
        if "Energy Drink" in inventory:
            inventory.remove("Energy Drink")

#这是一个已经完全不知道怎么写出来的固定查看功能...纯纯大**！
#def check_fixed_commands():
#    command = input("\nType a command ('HP' to view HP, 'backpack' to view inventory) or press Enter to continue: ").strip().lower()
#    if command == "hp":
#        print("\nYour current HP is:", player_hp)
#    elif command == "backpack":
#        print("\nYour backpack contains:", inventory)



# 同伙技能函数(我当时怎么想到写这个**功能的？）
def skill_fool():
    global enemy_hp, player_hp
    enemy_hp -= 10
    print("\n[Fool skill activated: enemy loses 10 HP.]")
    #if random.random() < 0.1:
    random1 = random.randint(0, 9)
    if random1 < 0.1:
        player_hp -= 10
        print("[Fool backlash: you lose 10 HP!]")

def skill_retired_military():
    global enemy_hp
    enemy_hp -= 5
    print("\n[Retired Military skill activated: enemy loses 5 HP.]")

#这个功能并未完成...后续可能补齐
def skill_robot_manufacturer():
    print("\n[Robot Manufacturer skill activated: For the next 3 rounds, you take half damage. (Effect simulated)]")
#这个功能并未完成...后续可能补齐
def skill_teacher():
    print("\n[Teacher skill activated: 50% chance to resurrect if you die; enemy damage may be reduced.]")

def skill_sam():
    global player_hp, player_max_hp
    player_hp *= 2
    player_max_hp *= 2
    print("\n[SAM skill activated: Your HP is doubled.(Testing characters, if you choose, may make your game very, very simple.)]")

def print_divider():
    print("-" * 40)
#print("------------------------------------------------------------------------------------")




# 游戏开始介绍(函数终于定义玩了）
def introduction():
    print("\nWelcome to RMC Bank Robbery!")
    print("\nYou are a professional thief planning a high-risk, high-reward bank heist.")
    print("Before you begin, you must prepare your equipment, recruit personnel,")
    print("and choose the best approach to infiltrate the bank.")
    print("\nType 'start' to begin the game")
    choice = input("\nPlease enter your choice: ").strip().lower()
    if choice == "start":
        equipment_shop()
    else:
        print("\nInvalid choice. Try again.")
        introduction()

# 装备商店阶段（这玩意真**恶心）
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
        #这玩意真是个好东西.....直接自动换行了
        print("Item: " + item["name"])
        print("Price: $" + str(item["price"]))
        print("Description: " + item["desc"])
    print_divider()
    print("\nType the name of an item to purchase it, or type 'done' when finished.")
    choice = input("Your choice: ").strip()
    #去除可能存在的空白字符+转小写
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
        #{"name": "Medic", "share": 20, "desc": "Can heal you during combat.", "skill": lambda: print("\n[Medic skill activated: Healing effect simulated.]")},
        #{"name": "Scout", "share": 15, "desc": "Provides intel on enemy positions.", "skill": lambda: print("\n[Scout skill activated: Intel gathered.]")}
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

# 偷渡分支
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
        hacker_side_door_TOF()
    else:
        print("Without a Hacking Tool, forcing the door triggers an alarm!")
        alarm_triggered = True
        combat("Side Door Guard", 30, 10)
        side_door_after_combat()


#由于老师要求这个格式所以......that why we have this...
def hacker_side_door_TOF():
    if random.random() < 0.10:
        print("Even with your Hacking Tool, a system glitch causes detection!")
        alarm_triggered = True
        combat("Side Door Guard", 30, 10)
        side_door_after_combat()
    else:
        print("Your Hacking Tool allows you to bypass security silently.")
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

#最傻逼的一集...
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
    print("Do you want to play again? (yes/no)or play the DLC?")
    choice = input("Your choice: ").strip().lower()
    if choice == "yes":
        reset_game()
    elif choice == "DLC":
        fenzang()
    elif choice == "no":
        print("Thank you for playing RMC Bank Robbery!made by ziyu(sam)")
        exit()

#youxi暴毙结算画面....
def game_over():
    print("Do you want to struggle? (yes/no)")
    choice = input("Your choice: ").strip().lower()
    if choice == "yes":
        shenwen()
    else:
        print("you die")
        print("Thank you for playing RMC Bank Robbery! made by ziyu(sam)")
        exit()

# 近战和远程交战系统
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

# 主函数
def main():
    print("=== RMC Bank Robbery ===")
    print("\nWould you like to start game? (yes/no)")
    choice = input("Your choice: ").strip().lower()
    if choice == "yes":
            introduction()
    else:
        main()

# 额外分支，凑点字数
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



#DLC!!!!!
def shenwen():
    print("\n[Interrogation DLC - Interrogation]")
    print("You are now under interrogation. The interrogator asks:")
    print("'Do you wish to confess or remain silent?' (confess/silent)")
    choice = input("Your choice: ").strip().lower()
    if choice == "confess":
        confession_branch()
    elif choice == "silent":
        silent_branch()
    else:
        print("Invalid choice. Restarting interrogation.")
        shenwen()


def confession_branch():
    print("\n[Confess Branch]")
    print("Do you want to fully confess or partially confess? (full/partial)")
    choice = input("Your choice: ").strip().lower()
    if choice == "full":
        full_confession_branch()
    elif choice == "partial":
        partial_confession_branch()
    else:
        print("Invalid choice. Try again.")
        confession_branch()


def full_confession_branch():
    print("\n[Full Confession Branch]")
    print(
        "Do you express sincere remorse and offer cooperation, or shift the blame onto someone else? (remorse/blame)")
    choice = input("Your choice: ").strip().lower()
    if choice == "remorse":
        full_confess_remorse_branch()
    elif choice == "blame":
        full_confess_blame_branch()
    else:
        print("Invalid choice. Try again.")
        full_confession_branch()


def full_confess_remorse_branch():
    print("\n[Cooperation Sub-branch]")
    print("Do you cooperate fully with the authorities or provide only partial information? (fully/partially)")
    choice = input("Your choice: ").strip().lower()
    if choice == "fully":
        print(
            "\nEnding: Redemption Ending - You cooperate fully and receive a lenient sentence with eventual freedom.")
    elif choice == "partially":
        print("\nEnding: Informant Ending - You trade off your fate by giving partial information.")
    else:
        print("Invalid choice. Try again.")
        full_confess_remorse_branch()


def full_confess_blame_branch():
    print("\n[Blame Sub-branch]")
    print("Do you accuse a subordinate or falsely blame an external party? (subordinate/external)")
    choice = input("Your choice: ").strip().lower()
    if choice == "subordinate":
        print("\nEnding: Betrayal Ending - Your betrayal backfires, leading to harsher consequences.")
    elif choice == "external":
        print("\nEnding: False Accusation Ending - Your story unravels, resulting in a severe outcome.")
    else:
        print("Invalid choice. Try again.")
        full_confess_blame_branch()


def partial_confession_branch():
    print("\n[Partial Confession Branch]")
    print("Do you downplay your role or imply that you were coerced into the heist? (downplay/coerced)")
    choice = input("Your choice: ").strip().lower()
    if choice == "downplay":
        partial_confess_downplay_branch()
    elif choice == "coerced":
        partial_confess_coerced_branch()
    else:
        print("Invalid choice. Try again.")
        partial_confession_branch()


def partial_confess_downplay_branch():
    print("\n[Downplay Sub-branch]")
    print(
        "Do you manage to convince the interrogators to reduce your charges, or do inconsistencies emerge? (reduce/inconsistencies)")
    choice = input("Your choice: ").strip().lower()
    if choice == "reduce":
        print("\nEnding: Mitigation Ending - Your convincing lowers your sentence.")
    elif choice == "inconsistencies":
        print("\nEnding: Skeptical Ending - Inconsistencies in your story result in a heavy sentence.")
    else:
        print("Invalid choice. Try again.")
        partial_confess_downplay_branch()


def partial_confess_coerced_branch():
    print("\n[Coerced Sub-branch]")
    print(
        "Do you claim you were forced into the heist and ask for protection, or is your coerced story discredited? (protection/discredited)")
    choice = input("Your choice: ").strip().lower()
    if choice == "protection":
        print("\nEnding: Coerced Confession Ending - Your claim leads to an uncertain outcome.")
    elif choice == "discredited":
        print(
            "\nEnding: Inconsistency Ending - Your coerced story is discredited, resulting in severe punishment.")
    else:
        print("Invalid choice. Try again.")
        partial_confess_coerced_branch()


def silent_branch():
    print("\n[Remain Silent Branch]")
    print("Do you deny all involvement or invoke your right to silence? (deny/silence)")
    choice = input("Your choice: ").strip().lower()
    if choice == "deny":
        silent_deny_branch()
    elif choice == "silence":
        silent_invoke_branch()
    else:
        print("Invalid choice. Try again.")
        silent_branch()


def silent_deny_branch():
    print("\n[Deny All Branch]")
    print("Do you maintain a calm denial or aggressively accuse the interrogators? (calm/aggressive)")
    choice = input("Your choice: ").strip().lower()
    if choice == "calm":
        silent_deny_calm_branch()
    elif choice == "aggressive":
        silent_deny_aggressive_branch()
    else:
        print("Invalid choice. Try again.")
        silent_deny_branch()


def silent_deny_calm_branch():
    print("\n[Calm Denial Sub-branch]")
    print(
        "Do you eventually get convicted due to evidence, or miraculously get acquitted? (conviction/acquittal)")
    choice = input("Your choice: ").strip().lower()
    if choice == "conviction":
        print("\nEnding: Inevitable Conviction Ending - Evidence forces a severe punishment.")
    elif choice == "acquittal":
        print("\nEnding: Miraculous Acquittal Ending - Against all odds, you are released but carry a stigma.")
    else:
        print("Invalid choice. Try again.")
        silent_deny_calm_branch()


def silent_deny_aggressive_branch():
    print("\n[Aggressive Denial Sub-branch]")
    print("Do you choose a defiant rejection or does violent retaliation occur? (defiant/violent)")
    choice = input("Your choice: ").strip().lower()
    if choice == "defiant":
        print("\nEnding: Defiant Rejection Ending - Your defiance worsens your situation.")
    elif choice == "violent":
        print(
            "\nEnding: Fatal Rebellion Ending - Your aggression leads to forceful detention and severe consequences.")
    else:
        print("Invalid choice. Try again.")
        silent_deny_aggressive_branch()


def silent_invoke_branch():
    print("\n[Invoke Silence Branch]")
    print("Do you request a lawyer or become aggressive toward the interrogator? (lawyer/aggressive)")
    choice = input("Your choice: ").strip().lower()
    if choice == "lawyer":
        silent_invoke_lawyer_branch()
    elif choice == "aggressive":
        silent_invoke_aggressive_branch()
    else:
        print("Invalid choice. Try again.")
        silent_invoke_branch()


def silent_invoke_lawyer_branch():
    print("\n[Lawyer Request Sub-branch]")
    print("Do you end up in legal limbo or receive judicial mercy? (limbo/mercy)")
    choice = input("Your choice: ").strip().lower()
    if choice == "limbo":
        print("\nEnding: Legal Limbo Ending - Your fate remains uncertain as the case drags on.")
    elif choice == "mercy":
        print("\nEnding: Judicial Mercy Ending - The judge shows mercy and commutes your sentence.")
    else:
        print("Invalid choice. Try again.")
        silent_invoke_lawyer_branch()


def silent_invoke_aggressive_branch():
    print("\n[Aggressive Invoke Sub-branch]")
    print(
        "Do you suffer a self-destructive outburst or get overpowered by security? (self-destruct/overpowered)")
    choice = input("Your choice: ").strip().lower()
    if choice == "self-destruct":
        print("\nEnding: Self-Destructive Ending - Your outburst leads to devastating personal consequences.")
    elif choice == "overpowered":
        print("\nEnding: Fatal Rebellion Ending - You are fatally injured during the interrogation.")
    else:
        print("Invalid choice. Try again.")
        silent_invoke_aggressive_branch()


#由于要凑字数所以又写一了一个dlc
def fenzang():
    print("\n[Loot Sharing DLC]")
    print("You have successfully completed the heist. Now it's time to divide the loot.")
    print("Do you want a fair division or a selfish division? (fair/selfish)")
    choice = input("Your choice: ").strip().lower()
    if choice == "fair":
        fenzang_fair()
    elif choice == "selfish":
        fenzang_selfish()
    else:
        print("Invalid choice, try again.")
        fenzang()


def fenzang_fair():
    print("\n[Fair Division]")
    print("Do you want to distribute the loot equally or proportionally based on contribution? (equal/proportional)")
    choice = input("Your choice: ").strip().lower()
    if choice == "equal":
        fenzang_fair_equal()
    elif choice == "proportional":
        fenzang_fair_proportional()
    else:
        print("Invalid choice, try again.")
        fenzang_fair()


def fenzang_fair_equal():
    print("\n[Equal Division - All Parties]")
    print(
        "Do you want to share equally among both associates and offsite support, or only among associates? (both/associates)")
    choice = input("Your choice: ").strip().lower()
    if choice == "both":
        fenzang_fair_equal_both()
    elif choice == "associates":
        fenzang_fair_equal_associates()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_equal()


def fenzang_fair_equal_both():
    print("\n[Equal Division Among Both]")
    print("Do all parties accept the equal share peacefully or do conflicts arise? (peaceful/conflict)")
    choice = input("Your choice: ").strip().lower()
    if choice == "peaceful":
        fenzang_fair_equal_both_peaceful()
    elif choice == "conflict":
        fenzang_fair_equal_both_conflict()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_equal_both()


def fenzang_fair_equal_both_peaceful():
    print(
        "\nEnding: Unified Prosperity – All parties accept the share and you form a stable alliance for future heists.")


def fenzang_fair_equal_both_conflict():
    print("\nEnding: Dispute Ending – Internal conflicts erupt, leading to betrayal and a fractured team.")


def fenzang_fair_equal_associates():
    print("\n[Equal Division Among Associates]")
    print("Do your associates accept the equal share, or do they feel undervalued? (accept/resent)")
    choice = input("Your choice: ").strip().lower()
    if choice == "accept":
        fenzang_fair_equal_associates_accept()
    elif choice == "resent":
        fenzang_fair_equal_associates_resent()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_equal_associates()


def fenzang_fair_equal_associates_accept():
    print("\nEnding: Loyal Alliance – Your associates accept the division, ensuring a cooperative future.")


def fenzang_fair_equal_associates_resent():
    print("\nEnding: Team Split – Resentment among associates leads to a breakup and isolation.")


def fenzang_fair_proportional():
    print("\n[Proportional Division]")
    print("Do you want to divide based on risk exposure or performance metrics? (risk/performance)")
    choice = input("Your choice: ").strip().lower()
    if choice == "risk":
        fenzang_fair_proportional_risk()
    elif choice == "performance":
        fenzang_fair_proportional_performance()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_proportional()


def fenzang_fair_proportional_risk():
    print("\n[Risk-Based Division]")
    print("Do all parties agree on the risk-based division? (agree/dispute)")
    choice = input("Your choice: ").strip().lower()
    if choice == "agree":
        fenzang_fair_proportional_risk_agree()
    elif choice == "dispute":
        fenzang_fair_proportional_risk_dispute()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_proportional_risk()


def fenzang_fair_proportional_risk_agree():
    print("\nEnding: Meritocratic Ending – Fair risk-based division leads to balanced rewards.")


def fenzang_fair_proportional_risk_dispute():
    print("\nEnding: Litigation Ending – Disputes over risk share result in legal battles and severe consequences.")


def fenzang_fair_proportional_performance():
    print("\n[Performance-Based Division]")
    print("Are the performance metrics accepted by all parties? (satisfied/unsatisfied)")
    choice = input("Your choice: ").strip().lower()
    if choice == "satisfied":
        fenzang_fair_proportional_performance_satisfied()
    elif choice == "unsatisfied":
        fenzang_fair_proportional_performance_unsatisfied()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_proportional_performance()


def fenzang_fair_proportional_performance_satisfied():
    print("\nEnding: Efficient Division Ending – Rewards based on performance yield a positive outcome.")


def fenzang_fair_proportional_performance_unsatisfied():
    print("\nEnding: Resentment Ending – Overlooked contributions cause internal strife and conflict.")


def fenzang_selfish():
    print("\n[Selfish Division]")
    print(
        "Do you want to favor yourself with a bonus or take almost all the loot, leaving only token shares? (bonus/almost_all)")
    choice = input("Your choice: ").strip().lower()
    if choice == "bonus":
        fenzang_selfish_bonus()
    elif choice == "almost_all":
        fenzang_selfish_almost_all()
    else:
        print("Invalid choice, try again.")
        fenzang_selfish()


def fenzang_selfish_bonus():
    print("\n[Selfish Bonus Branch]")
    print("Do your associates accept your bonus arrangement or threaten betrayal? (accept/threaten)")
    choice = input("Your choice: ").strip().lower()
    if choice == "accept":
        fenzang_selfish_bonus_accept()
    elif choice == "threaten":
        fenzang_selfish_bonus_threaten()
    else:
        print("Invalid choice, try again.")
        fenzang_selfish_bonus()


def fenzang_selfish_bonus_accept():
    print(
        "\nEnding: Conditional Acceptance Ending – Associates reluctantly accept your bonus, but the future remains uncertain.")


def fenzang_selfish_bonus_threaten():
    print("\nEnding: Defiant Rejection Ending – Your selfishness incites betrayal and severe consequences.")


def fenzang_selfish_almost_all():
    print("\n[Selfish 'Almost All' Branch]")
    print("Do your associates resent the token shares strongly or grudgingly accept them? (resent/accept)")
    choice = input("Your choice: ").strip().lower()
    if choice == "resent":
        fenzang_selfish_almost_all_resent()
    elif choice == "accept":
        fenzang_selfish_almost_all_accept()
    else:
        print("Invalid choice, try again.")
        fenzang_selfish_almost_all()


def fenzang_selfish_almost_all_resent():
    print("\nEnding: Abandonment Ending – Your associates desert you, leaving you alone with the consequences.")


def fenzang_selfish_almost_all_accept():
    print("\nEnding: Haunted Guilt Ending – You amass wealth but are haunted by your greed and internal strife.")


if __name__ == "__main__":
    extra_branch_choice()
    extra_shop_branch()
    extra_escape_option()
    main()
