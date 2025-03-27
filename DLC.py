
#very big DLC!!!

def hostage_control():
    print("\n[Hostage Control DLC - Entering Hostage Situation]")
    print("You have secured several hostages in the bank lobby. Police are surrounding the building...")
    print("Options:")
    print_divider()
    print("'negotiate' - Begin negotiations with the police.")
    print("'threaten'  - Threaten harm to hostages to demand bigger ransom.")
    print("'escape'    - Abandon hostages and attempt a risky escape (stronger enemies).")
    print_divider()

    choice = input("Enter your choice: ").strip().lower()
    if choice == "negotiate":
        hostage_negotiation_layer1()
    elif choice == "threaten":
        hostage_threaten_layer1()
    else:
        # 无论玩家输入escape或者其他指令，都跳到这儿统一处理当作要逃跑。。。因为想偷懒呢
        print("You decide to abandon the hostages and make a run for it!")
        hostage_escape_stronger_enemies()

#进入谈判
def hostage_negotiation_layer1():
    print("\n[Hostage Negotiation - Phase 1]")
    print("Police negotiators want you to release some hostages as a gesture. They also offer partial ransom.")
    random_event_during_hostage_DLC()

    print("\nOptions:")
    print_divider()
    print("'partial_release' - Release a few hostages for partial ransom.")
    print("'refuse_release'  - Refuse to release anyone.")
    print("'ally_gold_run'   - Send one ally to retrieve gold from the vault while you keep negotiating.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "partial_release":
        hostage_negotiation_partialrelease_layer2()
    elif choice == "refuse_release":
        hostage_negotiation_refuserelease_layer2()
    else:
        ally_vault_run_layer2()

def hostage_threaten_layer1():
    print("\n[Hostage Threaten - Phase 1]")
    print("You broadcast a threatening message: 'If demands not met, hostages will be harmed.'")
    random_event_during_hostage_DLC()

    print("\nOptions:")
    print_divider()
    print("'big_demand' - Demand a huge sum of money immediately.")
    print("'stall'      - Stall them while you figure out your next move.")
    print("'split_team' - Send half your team to handle the vault or side tasks, while you keep threatening.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "big_demand":
        hostage_threaten_bigdemand_layer2()
    elif choice == "stall":
        hostage_threaten_stall_layer2()
    else:
        hostage_threaten_splitteam_layer2()

def hostage_negotiation_partialrelease_layer2():
    print("\n[Negotiation - Partial Release - Phase 2]")
    money_gained = random.randint(100, 500) * 10  # 随机得到一些仅一些..........就很合理
    print(f"You release a few hostages. The police deliver a partial ransom of ${money_gained}.")
    add_money_to_player(money_gained)

    print("\nOptions:")
    print_divider()
    print("'cooperate_more' - Try to show more cooperation for a bigger final payoff.")
    print("'threaten_turn'  - Suddenly switch tactics and threaten to escalate.")
    print("'escape_now'     - Take the partial ransom and attempt to escape immediately.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "cooperate_more":
        hostage_negotiation_partial_cooperate_layer3()
    elif choice == "threaten_turn":
        hostage_negotiation_partial_threaten_layer3()
    else:
        print("You try to escape with only partial ransom. The police are somewhat alerted but less so than full threat.")
        hostage_escape_stronger_enemies()

def hostage_negotiation_refuserelease_layer2():
    print("\n[Negotiation - Refuse Release - Phase 2]")
    print("Police are angered. They threaten to storm in if you don't show some good faith.")
    random_event_during_hostage_DLC()

    print("\nOptions:")
    print_divider()
    print("'double_down'    - Double down on refusal and demand more money.")
    print("'fake_surrender' - Pretend to surrender to lure them in.")
    print("'hostage_fear'   - Terrorize hostages so they cry out, pressuring the police.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "double_down":
        hostage_negotiation_refuse_doubledown_layer3()
    elif choice == "fake_surrender":
        hostage_negotiation_refuse_fakesurrender_layer3()
    else:
        hostage_negotiation_refuse_hostagefear_layer3()

#尚未完成...
def ally_vault_run_focusneg_layer3():
    pass

#尚未完成...
def ally_vault_run_radiocheck_layer3():
    pass


def ally_vault_run_layer2():
    print("\n[Negotiation - Ally Vault Run - Phase 2]")
    print("You send a trusted ally to the vault while you keep negotiating. They might grab loot, or might betray you.")
    random_ally_betrayal_scenario()

    print("\nOptions:")
    print_divider()
    print("'focus_negotiation' - Focus on negotiating a better ransom for yourself, ignoring the ally's status.")
    print("'radio_check'       - Try to radio your ally for updates.")
    print("'abort_and_escape'  - Abandon negotiations and attempt an immediate breakout.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "focus_negotiation":
        #还在制作（still make)
        ally_vault_run_focusneg_layer3()
    elif choice == "radio_check":
        #还在制作（still make)
        ally_vault_run_radiocheck_layer3()
    else:
        print("You abandon negotiations. The police realize the ruse!")
        hostage_escape_stronger_enemies()

#第三层...
def hostage_threaten_bigdemand_layer2():
    print("\n[Hostage Threaten - Big Demand - Phase 2]")
    money_demanded = random.randint(300, 1000) * 10
    print(f"You demand a huge ransom of ${money_demanded} or you'll harm the hostages immediately.")
    random_event_during_hostage_DLC()

    print("\nOptions:")
    print_divider()
    print("'await_response' - Wait to see if the police comply with the big demand.")
    print("'take_action'    - Harm a hostage to prove your seriousness (increases alarm!).")
    print("'send_decoy'     - Attempt to send a decoy outside to draw police attention while you do something else.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "await_response":
        hostage_threaten_bigdemand_await_layer3()
    elif choice == "take_action":
        hostage_threaten_bigdemand_action_layer3()
    else:
        hostage_threaten_bigdemand_decoy_layer3()


#layer2号
def hostage_threaten_stall_layer2():
    print("\n[Hostage Threaten - Stall - Phase 2]")
    print("You stall for time, telling police your demands are still being prepared.")
    random_event_during_hostage_DLC()

    print("\nOptions:")
    print_divider()
    print("'fortify' - Use the time to fortify your position or place traps.")
    print("'intel'   - Try to gather intel from hostages (maybe bank manager?).")
    print("'split_2' - Split your crew again: Some watch hostages, some check perimeter.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "fortify":
        hostage_threaten_stall_fortify_layer3()
    elif choice == "intel":
        hostage_threaten_stall_intel_layer3()
    else:
        hostage_threaten_stall_split2_layer3()

def hostage_threaten_splitteam_layer2():
    print("\n[Hostage Threaten - Split Team - Phase 2]")
    print("You decide to split your team: half keep threatening hostages, half do side tasks (vault? side door?).")
    random_event_during_hostage_DLC()

    print("\nOptions:")
    print_divider()
    print("'vault_focus'   - Send half the team to get more money from the vault.")
    print("'side_sabotage' - Send half the team to sabotage any police infiltration from side doors.")
    print("'betrayal_risk' - Worry about your team turning on you, try to keep them in check.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "vault_focus":
        hostage_threaten_split_vault_layer3()
    elif choice == "side_sabotage":
        hostage_threaten_split_side_layer3()
    else:
        hostage_threaten_split_betrayal_layer3()

#bug补齐函数修复.....（fix all.....)
def hostage_negotiation_refuse_doubledown_layer3():
    print("\n[Negotiation - Refuse Release -> Double Down - Phase 3]")
    random_event_during_hostage_DLC()
    print("You refuse to show any goodwill and demand even more ransom. The police appear agitated.")

    print("\nOptions:")
    print_divider()
    print("'push_demands' - Push your demands to the limit, risking an assault.")
    print("'fake_cooperate' - Pretend to reconsider releasing hostages (a ruse).")
    print("'secret_escape' - Attempt to slip away using a side passage, ignoring negotiations.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "push_demands":
        if random.random() < 0.4:
            print("Police lose patience and assault the bank!")
            combat("SWAT Assault", 100, 30)
            escape_success()
        else:
            big_money = random.randint(300, 800)
            add_money_to_player(big_money)
            print(f"You somehow pressure them to send another ${big_money} before they pause negotiations!")
            hostage_cooperate_endgame_layer4()  # 随机结局
    elif choice == "fake_cooperate":
        print("You pretend to soften up, but it's a trick. The police remain uncertain.")
        hostage_stall_tactics_layer4()  # 复用(懒得写新的了）
    else:
        print("You decide the negotiations won't go well and try to escape quietly.")
        hostage_escape_stronger_enemies()

def hostage_negotiation_refuse_fakesurrender_layer3():
    print("\n[Negotiation - Refuse Release -> Fake Surrender - Phase 3]")
    random_event_during_hostage_DLC()
    print("You pretend to surrender, inviting the police to move in close. Could lead to a final shootout or a cunning advantage.")

    print("\nOptions:")
    print_divider()
    print("'ambush'   - Ambush the police as they approach.")
    print("'trick_run' - Slip away from a side exit while they approach the front.")
    print("'last_stand' - Actually consider surrendering if conditions are right.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "ambush":
        print("As soon as the police get close, you open fire!")
        combat("Police Team (Close Range)", 70, 20)
        # 直接逃或继续   :)
        escape_success()
    elif choice == "trick_run":
        print("While they come in from the main entrance, you flee through a hidden path!")
        if random.random() < 0.5:
            print("You slip away successfully!")
            escape_success()
        else:
            print("Your path was blocked by an unexpected SWAT unit!")
            combat("SWAT Blocking Team", 80, 25)
            escape_success()
    else:
        print("You actually consider turning yourself in. The police remain wary.")
        if random.random() < 0.3:
            print("They accept your surrender. You face jail time!")
            game_over()  # 或者另行处理结局
        else:
            print("They suspect a trick and open fire. A chaotic firefight ensues!")
            combat("Suspicious Police", 80, 25)
            escape_success()

def hostage_negotiation_refuse_hostagefear_layer3():
    print("\n[Negotiation - Refuse Release -> Hostage Fear - Phase 3]")
    random_event_during_hostage_DLC()
    print("You terrorize the hostages, making them scream for mercy. The police are under more pressure but also more hostile.")

    print("\nOptions:")
    print_divider()
    print("'demand_fast' - Demand immediate payment or you'll harm more hostages.")
    print("'use_snipers' - Force hostages to the windows as human shields against potential sniper shots.")
    print("'underground' - Move hostages to a lower floor or basement to avoid police eyes.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "demand_fast":
        quick_money = random.randint(100, 500)
        print(f"Police hastily wire ${quick_money}, but they're preparing a breach!")
        add_money_to_player(quick_money)
        if random.random() < 0.4:
            print("SWAT storms in right after the partial payment!")
            combat("SWAT Storm Team", 100, 35)
        escape_success()
    elif choice == "use_snipers":
        print("You line the windows with frightened hostages. SWAT snipers hold fire, but tension soars!")
        if random.random() < 0.5:
            print("Snipers eventually find an opening and shoot your weapon out of your hand!")
            # 可能导致小伤害
            combat("SWAT Sniper Follow-up", 50, 15)
        hostage_stall_tactics_layer4()
    else:
        print("You move deeper into the building with the hostages, limiting line of sight.")
        if random.random() < 0.3:
            print("Police use tear gas in the basement! You must fight your way out!")
            combat("Tear Gas SWAT Team", 90, 25)
        escape_success()


#第三层~~~~~~~

def hostage_threaten_bigdemand_await_layer3():
    print("\n[Hostage Threaten - Big Demand -> Await Response - Phase 3]")
    random_event_during_hostage_DLC()
    print("You wait, uncertain if the police will comply or assault. Time passes...")

    print("\nOptions:")
    print_divider()
    print("'stay_firm'  - Remain firm in your big demand.")
    print("'reduce_demand' - Show a slight compromise for partial money.")
    print("'fake_attack'   - Fire some warning shots or injure a hostage to speed them up.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "stay_firm":
        if random.random() < 0.4:
            print("Police attempt a quick rescue operation!")
            combat("Quick SWAT Raid", 70, 20)
        else:
            big_ransom = random.randint(400, 900)
            add_money_to_player(big_ransom)
            print(f"They reluctantly send ${big_ransom} to keep you from harming anyone... for now.")
        hostage_cooperate_endgame_layer4()
    elif choice == "reduce_demand":
        print("You reduce demands slightly, hoping for guaranteed money.")
        partial = random.randint(200, 400)
        add_money_to_player(partial)
        print(f"You receive a partial ransom of ${partial}.")
        hostage_stall_tactics_layer4()
    else:
        print("You injure a hostage or fire shots into the air. Police panic!")
        if random.random() < 0.3:
            print("Negotiators freeze. SWAT moves in for a forced rescue!")
            combat("SWAT Force", 80, 25)
        else:
            print("They pay something quickly to buy more time.")
            add_money_to_player(random.randint(100,300))
        escape_success()

def hostage_threaten_bigdemand_action_layer3():
    print("\n[Hostage Threaten - Big Demand -> Take Action - Phase 3]")
    random_event_during_hostage_DLC()
    print("You decide to harm a hostage or do something drastic to prove your seriousness. Alarm intensifies!")

    print("\nOptions:")
    print_divider()
    print("'severe_injury' - Severely injure a hostage, scaring police (but they may retaliate strongly).")
    print("'broadcast_fear' - Broadcast live to media, showing your ruthlessness.")
    print("'release_one'    - Oddly, you harm one but release another, causing confusion.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "severe_injury":
        print("You severely injure a hostage on camera. The police are furious!")
        if random.random() < 0.5:
            print("SWAT decides to storm in immediately!")
            combat("Enraged SWAT Assault", 110, 35)
        else:
            print("They wire you more money out of desperation.")
            add_money_to_player(random.randint(500, 1000))
        escape_success()
    elif choice == "broadcast_fear":
        print("You broadcast a shocking video feed. The whole city is in uproar!")
        # 可能带来大笔钱或更大SWAT（交给系统判断
        if random.random() < 0.5:
            add_money_to_player(random.randint(300, 700))
            print("Police tries to appease you with partial funds, but tension is huge!")
        else:
            print("Police will not negotiate further; they prepare a final breach!")
            combat("Large SWAT Team", 120, 40)
        escape_success()
    else:
        print("You release one hostage while harming another, sowing confusion.")
        if random.random() < 0.3:
            print("Police slip up, letting you move hostages to a safer vantage point.")
            hostage_stall_tactics_layer4()
        else:
            print("The confusion isn't enough; an assault begins.")
            combat("Confused SWAT Team", 80, 25)
            escape_success()

def hostage_threaten_bigdemand_decoy_layer3():
    print("\n[Hostage Threaten - Big Demand -> Send Decoy - Phase 3]")
    random_event_during_hostage_DLC()
    print("You send a disguised person (or a bound hostage) outside, hoping to distract the police while you plot your next move.")

    print("\nOptions:")
    print_divider()
    print("'vault_run'   - Exploit the distraction to grab more loot from the vault.")
    print("'reinforce'   - Move your team to reinforce the main entrance with barricades.")
    print("'escape_backdoor' - Attempt a quiet backdoor escape while decoy draws attention.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "vault_run":
        print("Your decoy lures away key police units. You rush for the vault!")
        add_money_to_player(random.randint(200, 700))
        if random.random() < 0.4:
            print("Remaining police discover you quickly! Short firefight!")
            combat("Scramble Police", 60, 18)
        escape_success()
    elif choice == "reinforce":
        print("You fortify the entrance while the police are busy with the decoy, buying more time.")
        hostage_stall_tactics_layer4()
    else:
        print("You slip out the back. The decoy is probably captured, but you might escape!")
        if random.random() < 0.5:
            print("Escape successful with some loot!")
            escape_success()
        else:
            print("A secondary unit was guarding the back alley. You must fight them!")
            combat("Back Alley Patrol", 70, 20)
            escape_success()


def hostage_threaten_stall_fortify_layer3():
    print("\n[Hostage Threaten - Stall -> Fortify - Phase 3]")
    random_event_during_hostage_DLC()
    print("You use the stalling time to set up barricades, traps, or defensive positions.")

    print("\nOptions:")
    print_divider()
    print("'tripwire_trap' - Place tripwire grenades or improvised traps.")
    print("'block_entrance' - Block or weld the main entrance shut.")
    print("'roof_watch'     - Position a lookout on the roof to spot police movements.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "tripwire_trap":
        print("You rig some tripwire traps near the entrances.")
        if random.random() < 0.3:
            print("A trap misfires while setting up, injuring you slightly!")
            combat("Self-inflicted chaos", 30, 10)
        hostage_stall_tactics_layer4()
    elif choice == "block_entrance":
        print("You weld the main doors, hoping to slow any breach. Police might try alternate routes.")
        if random.random() < 0.5:
            print("SWAT decides to blow a hole in the wall instead!")
            combat("Wall Breach SWAT", 90, 30)
        else:
            print("They hold off, uncertain how to proceed.")
            hostage_stall_tactics_layer4()
    else:
        print("You send a lookout to the roof, hopefully preventing a surprise assault from above.")
        if random.random() < 0.4:
            print("A police helicopter spots your lookout! Small firefight ensues.")
            combat("Helicopter Support", 80, 25)
        hostage_stall_tactics_layer4()

def hostage_threaten_stall_intel_layer3():
    print("\n[Hostage Threaten - Stall -> Intel - Phase 3]")
    random_event_during_hostage_DLC()
    print("You attempt to interrogate hostages—especially the bank manager—for security codes or hidden stashes.")

    print("\nOptions:")
    print_divider()
    print("'safe_combination' - Demand the combination to a hidden safe.")
    print("'employee_info'    - Learn about any panic buttons, secret exits, or bank secrets.")
    print("'hostage_double'   - Try to see if any hostage might turn traitor and work for you.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "safe_combination":
        safe_money = random.randint(200, 800)
        print(f"The manager reluctantly gives up the code. You retrieve ${safe_money} from a small safe!")
        add_money_to_player(safe_money)
        hostage_stall_tactics_layer4()
    elif choice == "employee_info":
        print("You discover the location of a potential secret tunnel but it's partially blocked.")
        if random.random() < 0.3:
            print("Tunnel is actually collapsed. Dead end.")
            hostage_stall_tactics_layer4()
        else:
            print("You might use that tunnel to escape!")
            hostage_escape_stronger_enemies()
    else:
        print("One of the hostages might join you if you promise them a cut.")
        if random.random() < 0.4:
            print("They fake cooperation, then sabotage you from inside!")
            combat("Internal Hostage Betrayal", 50, 15)
            escape_success()
        else:
            print("They help you, giving insider tips or distracting police.")
            add_money_to_player(random.randint(100, 300))
        hostage_stall_tactics_layer4()

def hostage_threaten_stall_split2_layer3():
    print("\n[Hostage Threaten - Stall -> Split_2 - Phase 3]")
    random_event_during_hostage_DLC()
    print("You split your crew: some watch the hostages, others check the perimeter for possible infiltration.")

    print("\nOptions:")
    print_divider()
    print("'roof_defense'    - Place some members on the roof to guard from above.")
    print("'parking_lot'     - Station members near the parking lot, watching police movements.")
    print("'internal_patrol' - Have them patrol inside, in case the police break in from vents or windows.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "roof_defense":
        print("Your roof squad may see SWAT rapelling down.")
        if random.random() < 0.4:
            combat("Rooftop SWAT Rappel", 70, 20)
        hostage_stall_tactics_layer4()
    elif choice == "parking_lot":
        print("They watch the police outside. Possibly they notice a gap to escape!")
        if random.random() < 0.5:
            print("You find a momentary gap and drive away in a stolen police van!")
            escape_success()
        else:
            print("No gap big enough; you remain inside.")
            hostage_stall_tactics_layer4()
    else:
        print("They patrol the hallways. If police attempt a stealth entry, you might catch them.")
        if random.random() < 0.3:
            combat("Stealth SWAT Infiltrators", 60, 18)
        hostage_stall_tactics_layer4()


def hostage_threaten_split_vault_layer3():
    print("\n[Hostage Threaten - Split Team -> Vault Focus - Phase 3]")
    random_event_during_hostage_DLC()
    print("You send half your team to secure the vault, hoping to gather more money, while others watch the hostages.")

    print("\nOptions:")
    print_divider()
    print("'quick_loot' - Grab whatever is easily accessible in the vault and return.")
    print("'full_drill' - Attempt a deeper drilling for maximum loot, but it takes time.")
    print("'trap_vault' - Booby-trap the vault area to harm SWAT if they try to reclaim it.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "quick_loot":
        loot = random.randint(400, 1200)
        print(f"Your team grabs a quick haul of ${loot}.")
        add_money_to_player(loot)
        hostage_stall_tactics_layer4()
    elif choice == "full_drill":
        if random.random() < 0.4:
            print("SWAT intercepts mid-drill! Your team is pinned!")
            combat("Vault Hallway SWAT", 80, 25)
        else:
            big_loot = random.randint(1500, 3000)
            print(f"Full drilling success! They haul out ${big_loot} from deeper vault sections!")
            add_money_to_player(big_loot)
        escape_success()
    else:
        print("You lay traps in the vault. If SWAT tries to reclaim it, they'll get a surprise.")
        if random.random() < 0.5:
            print("SWAT triggers the trap, suffering casualties. They retreat!")
            hostage_stall_tactics_layer4()
        else:
            print("They carefully disarm your trap and proceed. Time wasted for them, though.")
            hostage_stall_tactics_layer4()

def hostage_threaten_split_side_layer3():
    print("\n[Hostage Threaten - Split Team -> Side Sabotage - Phase 3]")
    random_event_during_hostage_DLC()
    print("You send half your team to sabotage any attempt by police to breach from side doors or windows.")

    print("\nOptions:")
    print_divider()
    print("'barricade_side' - Barricade or booby-trap the side entrance.")
    print("'fake_exit'      - Make a fake exit to lure SWAT there while you hold main.")
    print("'capture_swats'  - Attempt a mini-ambush on any SWAT who tries to come in from the side.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "barricade_side":
        print("Side entrance barricaded. SWAT might choose a rooftop or front breach now.")
        hostage_stall_tactics_layer4()
    elif choice == "fake_exit":
        print("You create a fake 'escape tunnel' that leads nowhere, hoping to lure SWAT.")
        if random.random() < 0.4:
            print("SWAT investigates and wastes time. You gain precious minutes!")
            hostage_stall_tactics_layer4()
        else:
            print("They see through the ruse quickly, no real benefit for you.")
            hostage_stall_tactics_layer4()
    else:
        print("You lie in wait for unsuspecting SWAT near the side windows.")
        if random.random() < 0.5:
            combat("Ambushed SWAT", 60, 18)
        else:
            print("SWAT chooses a different route, you wait in vain.")
        escape_success()

def hostage_threaten_split_betrayal_layer3():
    print("\n[Hostage Threaten - Split Team -> Betrayal Risk - Phase 3]")
    random_event_during_hostage_DLC()
    print("You're worried your split team might betray you or cut a deal with the police.")

    print("\nOptions:")
    print_divider()
    print("'recall_team' - Recall them and keep a closer eye on them.")
    print("'send_loyalist' - Send a known loyal accomplice to watch them.")
    print("'trust_fate'   - Assume they won't betray you and continue your plan.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "recall_team":
        print("You recall your team. Now you're all back together but lose time.")
        hostage_stall_tactics_layer4()
    elif choice == "send_loyalist":
        if random.random() < 0.3:
            print("The loyalist catches them trying to surrender to the police!")
            combat("Internal Betrayers", 50, 15)
        else:
            print("They stay in line under the loyalist's watch. For now, no betrayal occurs.")
        hostage_stall_tactics_layer4()
    else:
        print("You trust them. There's a risk!")
        if random.random() < 0.4:
            print("They cut a deal with the police. You lose some money or face a pincer attack!")
            subtract_money_from_player(random.randint(200,600))
            combat("Pincer Attack", 80, 25)
        else:
            print("No betrayal yet; they follow your orders.")
        escape_success()



def hostage_negotiation_partial_threaten_layer3():
    print("\n[Negotiation - Partial Release -> Sudden Threaten - Phase 3]")
    random_event_during_hostage_DLC()
    print("You catch the police off-guard by switching from partial release to threatening hostages again.")

    print("\nOptions:")
    print_divider()
    print("'demand_final' - Demand a final large sum.")
    print("'fake_bomb'    - Claim you planted bombs in the building.")
    print("'call_ally'    - Summon your ally to bring you more gear from the getaway vehicle.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "demand_final":
        hostage_final_demand_layer4()
    elif choice == "fake_bomb":
        hostage_fake_bomb_layer4()
    else:
        hostage_call_ally_layer4()


def hostage_call_ally_layer4():
    print("\n[Hostage - Call Ally - Final Phase]")
    random_event_during_hostage_DLC()
    print("You call an ally outside to bring supplies or possibly help you break out. But there's risk they get caught or betray you.")

    print("\nOptions:")
    print_divider()
    print("'gear_arrive'   - Wait for them to arrive with heavy gear (guns, armor).")
    print("'ally_disguise' - Have them disguise as a negotiator to get inside.")
    print("'cancel_call'   - On second thought, calling them might blow their cover. Cancel it.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "gear_arrive":
        if random.random() < 0.4:
            print("Police intercept your ally's approach! Big firefight outside!")
            combat("Ally vs. Police Outside", 60, 20)
        else:
            print("Your ally arrives with better gear!")
#伤害翻倍代码还需呀完成
            print("Your next combat deals more damage!")
#玩家火力提升还要更新......
        escape_success()
    elif choice == "ally_disguise":
        if random.random() < 0.3:
            print("The disguise fails, police discover the trick quickly!")
            combat("Police Reaction Force", 80, 25)
            escape_success()
        else:
            print("They slip in, boosting your hostage control advantage!")
            add_money_to_player(random.randint(300, 700))
            hostage_stall_tactics_layer4()
    else:
        print("You cancel the ally call. You remain on your own with the hostages.")
        hostage_stall_tactics_layer4()

#随机事件（random things。）
def hostage_negotiation_partial_cooperate_layer3():
    print("\n[Negotiation - Partial Release -> Cooperate More - Phase 3]")
    random_event_during_hostage_DLC()
    print("You decide to further cooperate. Police might reduce the severity of your future charges...")

    print("\nOptions:")
    print_divider()
    print("'full_release'   - Release all but one hostage for a larger sum of money.")
    print("'stall_them'     - Pretend to cooperate but secretly stall.")
    print("'escape_surprise' - Attempt a surprise escape right now.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "full_release":
        big_ransom = random.randint(600, 1200)
        print(f"Police pay you a big sum of ${big_ransom}, but your leverage is almost gone.")
        add_money_to_player(big_ransom)
        hostage_cooperate_endgame_layer4()
    elif choice == "stall_them":
        hostage_stall_tactics_layer4()
    else:
        print("You attempt a surprise escape while police are somewhat relaxed!")
        hostage_escape_stronger_enemies()


def random_event_during_hostage_DLC():
    roll = random.randint(1, 6)
    if roll == 1:
        print("\n[Random Event] A frightened hostage tries to escape, causing momentary chaos!")
    elif roll == 2:
        print("\n[Random Event] You find a phone on a hostage, possibly used to contact outside.")
    elif roll == 3:
        print("\n[Random Event] Police drone flies near a window, taking pictures of your location!")
    elif roll == 4:
        print("\n[Random Event] One of your accomplices claims there's a hidden safe behind the manager's office.")
    elif roll == 5:
        print("\n[Random Event] A SWAT sniper bullet nearly hits you, but lodges in the wall!")
    else:
        print("\n[Random Event] Nothing unusual happens... for now.")

def random_ally_betrayal_scenario():
    chance = random.random()
    if chance < 0.2:
        print("\n[Ally Betrayal] Your ally attempts to steal some money and vanish!")
        stolen = random.randint(100, 1000)
        print(f"They manage to take ${stolen} worth of valuables from you!")
        subtract_money_from_player(stolen)
    elif chance < 0.4:
        print("\n[Ally Hesitation] Your ally is stuck, worried about the police, not collecting loot effectively.")
    else:
        print("\n[Ally Loyal] Your ally remains loyal... for now.")

def add_money_to_player(amount):
    global player_money
    player_money += amount
    print(f"[System] Player money increased by ${amount}. Total: ${player_money}.")

def subtract_money_from_player(amount):
    global player_money
    if player_money < amount:
        amount = player_money
    player_money -= amount
    print(f"[System] Player loses ${amount}. Remaining: ${player_money}.")

#ending

def hostage_cooperate_endgame_layer4():
    print("\n[Hostage - Cooperative Path - Final Phase]")
    print("You have nearly no hostages left, but you did get a big chunk of ransom. Police might let you walk away or might double-cross you.")
    if random.random() < 0.5:
        print("Police keep their word. You slip away with the money, albeit precariously.")
        escape_success()
    else:
        print("Police SWAT storms in at the last second! You must fight your way out!")
        combat("SWAT Team (Final Betrayal)", 90, 30)
        escape_success()

def hostage_stall_tactics_layer4():
    print("\n[Hostage - Stall Tactics - Final Phase]")
    print("You've stalled the police multiple times. They grow impatient.")

    print("\nOptions:")
    print_divider()
    print("'dig_in'      - Dig in for a long standoff.")
    print("'bluff_exit'  - Pretend you have an exit route, see if police let you pass.")
    print("'fake_blast'  - Use thermite or a fake bomb threat to open a new path.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "dig_in":
        print("You brace for a siege. This might lead to a final SWAT assault.")
        combat("SWAT Assault", 100, 35)
        escape_success()
    elif choice == "bluff_exit":
        if random.random() < 0.3:
            print("Police buy your bluff and back off, giving you a window to slip away!")
            escape_success()
        else:
            print("Your bluff fails. A tear gas volley hits your area!")
            combat("Tear Gas & SWAT", 90, 25)
            escape_success()
    else:
        print("You use a bomb threat or thermite to create a new exit path.")
        hostage_escape_stronger_enemies()

def hostage_final_demand_layer4():
    print("\n[Hostage - Final Demand - Phase 4]")
    money_gained = random.randint(800, 2000)
    print(f"You demand one final large sum. The police deposit ${money_gained} in a location you specify.")
    add_money_to_player(money_gained)
    print("Will you trust them enough to pick it up? Possibly a trap...")

    print("\nOptions:")
    print_divider()
    print("'pickup'   - Attempt to retrieve the dropped money.")
    print("'ignore'   - In your greed, you go for it anyway.")
    print("'escape'   - Decide it's too dangerous, cut your losses, and flee.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "pickup":
        if random.random() < 0.4:
            print("It's a police ambush! You have to fight your way out!")
            combat("Ambush Team", 90, 25)
        else:
            print("You successfully grab the money and slip away!")
        escape_success()
    elif choice == "ignore":
        print("You walk right into a potential trap, but in your greed, you push forward.")
        if random.random() < 0.6:
            print("SWAT traps you. A fierce gunfight ensues!")
            combat("SWAT Trap", 100, 30)
        else:
            print("Miraculously, the trap was poorly set, and you got away with the money!")
        escape_success()
    else:
        print("You decide it's not worth the risk. Time to run!")
        hostage_escape_stronger_enemies()

def hostage_fake_bomb_layer4():
    print("\n[Hostage - Fake Bomb - Phase 4]")
    print("You claim you have bombs placed around the hostages, demanding the police stand down.")
    random_event_during_hostage_DLC()

    print("\nOptions:")
    print_divider()
    print("'police_call_bluff' - The police might call your bluff; risk a direct assault!")
    print("'negotiator_trap'   - Lure the lead negotiator in, attempt to capture them too.")
    print("'escape_with_bomb'  - Pretend to have a bomb strapped while you walk out.")
    print_divider()

    choice = input("Your choice: ").strip().lower()
    if choice == "police_call_bluff":
        if random.random() < 0.5:
            print("They storm in! Fight or die!")
            combat("Police Assault (Fake Bomb Exposed)", 100, 30)
            escape_success()
        else:
            print("Police hesitate, giving you time to slip away with some hostages as cover.")
            escape_success()
    elif choice == "negotiator_trap":
        print("You lure the head negotiator inside. Possibly a huge advantage or a disaster.")
        if random.random() < 0.5:
            print("Success! You capture the negotiator, forcing the police to back off. You gain time to gather more loot.")
            add_money_to_player(random.randint(300, 900))
            hostage_escape_stronger_enemies()
        else:
            print("Negotiator was armed or had backup. You get ambushed!")
            combat("Negotiator's SWAT Escort", 100, 25)
            game_over()
    else:
        print("You step out, faking a bomb vest. The police are forced back, but snipers might shoot if they realize the ruse.")
        if random.random() < 0.3:
            print("A sniper bullet hits you! You're gravely wounded!")
            game_over()
        else:
            print("Somehow you cross the perimeter and vanish into the night!")
            escape_success()

#包强的....
def hostage_escape_stronger_enemies():

    print("\n[Hostage Escape - Stronger Enemies]")
    print("You abandon the hostage situation and attempt to escape. The police are on high alert!")
    combat("SWAT Reinforcements", 80, 25)
    print("You break through the police perimeter in chaos!")
    escape_success()