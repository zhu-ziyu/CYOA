import tkinter as tk
import json
import random
import threading

# Attempt to import playsound for sound effect
try:
    from playsound import playsound
except ImportError:
    playsound = None


class BankRobberyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("RMC Bank Robbery - Text Adventure")
        # Player initial stats
        self.initial_money = 3000
        self.player_hp = 100
        self.player_max_armor = 100
        self.player_armor = 100
        self.player_money = self.initial_money
        self.inventory = []
        # Game state flags
        self.alarm_triggered = False
        self.have_vault_key = False
        self.approach_method = None
        self.money_looted = 0
        # Control saving availability
        self.can_save = True
        # Load images
        self.images = {}
        image_files = {
            "vault": "image/vault.png",
            "gun": "image/gun.png",
            "character": "image/character.png",
            "item": "image/item.png"
        }
        for key, path in image_files.items():
            try:
                img = tk.PhotoImage(file=path)
                self.images[key] = img
            except Exception:
                # Try PIL if installed
                try:
                    from PIL import Image, ImageTk
                    imgpil = Image.open(path)
                    img = ImageTk.PhotoImage(imgpil)
                    self.images[key] = img
                except Exception:
                    self.images[key] = None
        # UI elements setup
        self.image_label = tk.Label(root)
        self.image_label.pack(side="top", pady=5)
        self.story_label = tk.Label(root, text="", wraplength=500, justify="left")
        self.story_label.pack(side="top", padx=10, pady=5)
        self.status_label = tk.Label(root, text="", justify="left")
        self.status_label.pack(side="bottom", fill="x", padx=5, pady=5)
        # Menu for save/load
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Game", command=self.save_game)
        file_menu.add_command(label="Load Game", command=self.load_game)
        menubar.add_cascade(label="File", menu=file_menu)
        # Start game introduction
        self.show_intro()

    def update_status(self):
        """Update status label with current HP, Armor, Money, Inventory."""
        inv_str = ", ".join(self.inventory) if self.inventory else "None"
        status_text = f"HP: {self.player_hp}    Armor: {self.player_armor}    Money: {self.player_money}\nInventory: {inv_str}"
        self.status_label.config(text=status_text)

    def clear_active_widgets(self):
        """Destroy any dynamically created widgets (buttons/frames) from the last scene."""
        if hasattr(self, "active_widgets"):
            for widget in self.active_widgets:
                try:
                    widget.destroy()
                except:
                    pass
        self.active_widgets = []

    def show_intro(self):
        """Display the game introduction and proceed to equipment prep."""
        self.clear_active_widgets()
        if self.images.get("character"):
            self.image_label.config(image=self.images["character"])
        else:
            self.image_label.config(image="")
        intro_text = ("You are a master thief planning to rob the RMC Bank. "
                      "This is a risky mission, but the payoff could be huge. "
                      "You'll need to prepare well before you begin the heist.")
        self.story_label.config(text=intro_text)
        btn = tk.Button(self.root, text="Continue", command=self.show_shop)
        btn.pack(side="top", pady=10)
        self.active_widgets.append(btn)
        self.current_stage = "intro"
        self.update_status()

    def show_shop(self):
        """Show equipment shop for player to buy gear."""
        self.clear_active_widgets()
        if self.images.get("item"):
            self.image_label.config(image=self.images["item"])
        else:
            self.image_label.config(image="")
        shop_text = (f"You have ${self.player_money} to spend on equipment for the heist.\n"
                     "Choose your gear:")
        self.story_label.config(text=shop_text)
        # Create a frame for item list
        self.shop_frame = tk.Frame(self.root)
        self.shop_frame.pack(side="top", pady=5)
        # Reset item buttons dict
        self.item_buttons = {}
        # Items for sale
        self.items_for_sale = [
            {"name": "Camouflage Suit", "price": 500, "desc": "Helps avoid detection at the main entrance."},
            {"name": "Hacking Tool", "price": 500, "desc": "Allows silent entry through the side door."},
            {"name": "Thermite", "price": 1000, "desc": "Explosive charges to blast open the vault."},
            {"name": "Security Uniform", "price": 800, "desc": "Disguise as a guard; may help bribe security."},
            {"name": "Kevlar Vest", "price": 300, "desc": "Improved armor vest (increases armor value)."},
            {"name": "Knife", "price": 100, "desc": "A knife for silent takedowns (ignores armor)."},
            {"name": "Pistol", "price": 300, "desc": "A basic handgun for self-defense."},
            {"name": "Rifle", "price": 800, "desc": "An assault rifle for serious firepower."}
        ]
        # List each item with a Buy button
        for idx, item in enumerate(self.items_for_sale):
            name = item["name"];
            price = item["price"];
            desc = item["desc"]
            lbl = tk.Label(self.shop_frame, text=f"{name} - ${price}: {desc}", justify="left")
            lbl.grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            btn = tk.Button(self.shop_frame, text="Buy", command=lambda n=name, p=price: self.buy_item(n, p))
            btn.grid(row=idx, column=1, padx=5, pady=2)
            self.item_buttons[name] = btn
            # Disable button if item already in inventory (for load mid-shop scenario)
            if name in self.inventory:
                btn.config(state="disabled", text="Purchased")
        done_btn = tk.Button(self.shop_frame, text="Done Shopping", command=self.finish_shopping)
        done_btn.grid(row=len(self.items_for_sale), column=0, columnspan=2, pady=10)
        self.active_widgets.append(self.shop_frame)
        self.current_stage = "shopping"
        self.update_status()

    def buy_item(self, item_name, price):
        """Handle purchasing an item from the shop."""
        if item_name in self.inventory:
            return  # already purchased
        if self.player_money >= price:
            self.player_money -= price
            self.inventory.append(item_name)
            # Apply immediate effects for certain items
            if item_name == "Kevlar Vest":
                self.player_max_armor = 150
                self.player_armor = 150
            # Disable the purchased item's button
            if item_name in self.item_buttons:
                self.item_buttons[item_name].config(state="disabled", text="Purchased")
            self.update_status()
        else:
            # Not enough money
            old_text = self.story_label.cget("text")
            self.story_label.config(text="Not enough money to purchase this item.")
            # Restore shop text after a short delay
            self.root.after(1500, lambda: self.story_label.config(text=old_text))

    def finish_shopping(self):
        """Complete shopping and move to approach selection."""
        self.clear_active_widgets()
        self.story_label.config(text="You have finished equipping yourself for the heist.")
        self.choose_approach()

    def choose_approach(self):
        """Ask the player how they want to approach the bank."""
        if self.images.get("character"):
            self.image_label.config(image=self.images["character"])
        else:
            self.image_label.config(image="")
        approach_text = ("How will you approach the bank?\n"
                         "Choose your method of entry:")
        self.story_label.config(text=approach_text)
        btn1 = tk.Button(self.root, text="On foot", command=self.approach_on_foot)
        btn2 = tk.Button(self.root, text="By car (ram the entrance)", command=self.approach_by_land)
        btn3 = tk.Button(self.root, text="By helicopter (land on roof)", command=self.approach_from_roof)
        btn1.pack(side="top", pady=5);
        btn2.pack(side="top", pady=5);
        btn3.pack(side="top", pady=5)
        self.active_widgets = [btn1, btn2, btn3]
        self.current_stage = "choose_approach"
        self.update_status()

    def approach_on_foot(self):
        """Chosen to approach on foot - decide entry point."""
        self.clear_active_widgets()
        self.approach_method = "foot"
        text = ("You approach the bank on foot under the cover of darkness. "
                "Now at the bank's perimeter, you need to decide how to enter.")
        self.story_label.config(text=text)
        btn1 = tk.Button(self.root, text="Enter through the main entrance", command=self.main_entrance)
        btn2 = tk.Button(self.root, text="Sneak in through the side door", command=self.side_door)
        btn1.pack(side="top", pady=5);
        btn2.pack(side="top", pady=5)
        self.active_widgets = [btn1, btn2]
        self.current_stage = "approach_on_foot"
        self.update_status()

    def approach_by_land(self):
        """Chosen to approach by land vehicle (loud entry)."""
        self.clear_active_widgets()
        self.approach_method = "land"
        text = ("You load your gear into a van and drive towards the bank. "
                "Your plan is to crash the van through the entrance for a speedy entry.")
        self.story_label.config(text=text)
        btn = tk.Button(self.root, text="Crash into the bank lobby", command=self.land_entry)
        btn.pack(side="top", pady=5)
        self.active_widgets = [btn]
        self.current_stage = "approach_by_land"
        self.update_status()

    def approach_from_roof(self):
        """Chosen to approach via rooftop (helicopter)."""
        self.clear_active_widgets()
        self.approach_method = "roof"
        text = ("A helicopter lifts you to the bank's rooftop, offering a stealthy entry from above. "
                "You quietly land on the roof and prepare to move inside.")
        self.story_label.config(text=text)
        if "Thermite" in self.inventory:
            # Choice: get key or use thermite directly
            btn1 = tk.Button(self.root, text="Find the guard with the vault key", command=self.roof_find_guard)
            btn2 = tk.Button(self.root, text="Skip guard and blast the vault door", command=self.roof_direct_vault)
            btn1.pack(side="top", pady=5);
            btn2.pack(side="top", pady=5)
            self.active_widgets = [btn1, btn2]
        else:
            btn = tk.Button(self.root, text="Enter the building", command=self.roof_find_guard)
            btn.pack(side="top", pady=5)
            self.active_widgets = [btn]
        self.current_stage = "roof_decision"
        self.update_status()

    def main_entrance(self):
        """Attempt entry via main entrance (foot approach)."""
        self.clear_active_widgets()
        # Determine detection
        detected = False
        if "Camouflage Suit" in self.inventory:
            # Camouflage reduces detection significantly
            if random.random() < 0.1:  # small chance to still be caught
                detected = True
        else:
            # Without disguise, high chance to be noticed
            if random.random() < 0.7:
                detected = True
        if detected:
            self.alarm_triggered = True
            text = ("You try to walk through the main entrance. A guard stops you, eyeing you suspiciously. "
                    "Your cover is blown! The guard draws a weapon.")
            self.story_label.config(text=text)
            # Engage in combat with entrance guard
            self.start_combat(enemy_name="Guard", enemy_hp=30, enemy_damage=10, enemy_weapon="bullet",
                              on_win=self.main_first_fight_win)
        else:
            text = ("Dressed inconspicuously, you slip past the main entrance security without drawing attention. "
                    "You are now inside the bank lobby, unnoticed.")
            self.story_label.config(text=text)
            # Inside quietly - locate the guard with the vault key
            if "Knife" in self.inventory:
                # Silent kill guard
                kill_text = ("\nYou locate the guard carrying the vault key. "
                             "You creep behind him and silently eliminate him with your knife. No one hears a thing.")
                self.have_vault_key = True
                # Remain undetected
            else:
                # Take out guard with a gunshot (loud)
                shoot_text = ("\nYou find the guard with the vault key and take him out with a single shot. "
                              "The gunshot echoes loudly! The alarm is triggered!")
                self.alarm_triggered = True
                self.have_vault_key = True
            # Update story text to include guard outcome
            if "Knife" in self.inventory:
                self.story_label.config(text=text + kill_text)
            else:
                self.story_label.config(text=text + shoot_text)
            # Proceed to vault
            self.proceed_to_vault_prompt()
        # (If detected, combat flow continues via on_win callback)

    def main_first_fight_win(self):
        """After winning the fight with the entrance guard (main entrance)."""
        self.clear_active_widgets()
        text = ("The guard collapses. Alarms begin to blare! "
                "You rush deeper into the bank to find the vault key.")
        self.story_label.config(text=text)
        # Now confront the vault key guard
        btn = tk.Button(self.root, text="Confront the vault key guard", command=self.main_key_guard_fight)
        btn.pack(side="top", pady=5)
        self.active_widgets = [btn]
        self.current_stage = "main_first_fight_done"
        self.update_status()

    def main_key_guard_fight(self):
        """Start fight with the guard carrying the vault key (main entrance path)."""
        self.clear_active_widgets()
        text = "You corner the guard carrying the vault key. He won't surrender without a fight."
        self.story_label.config(text=text)
        # Fight the key guard (tougher enemy)
        self.start_combat(enemy_name="Key Guard", enemy_hp=40, enemy_damage=15, enemy_weapon="bullet",
                          on_win=self.main_key_guard_defeated)

    def main_key_guard_defeated(self):
        """After defeating the vault key guard on main entrance path."""
        self.clear_active_widgets()
        self.have_vault_key = True
        text = "The guard with the key is defeated. You grab the vault key from his body."
        self.story_label.config(text=text)
        self.proceed_to_vault_prompt()

    def side_door(self):
        """Attempt entry via side door (foot approach)."""
        self.clear_active_widgets()
        # Determine if door entry triggers alarm
        if "Hacking Tool" in self.inventory:
            text = ("Using your hacking device, you bypass the side door security quietly. "
                    "You slip into the bank through a side entrance, unnoticed.")
            detected = False
        else:
            text = ("You attempt to pry open the side door. The alarm sensor trips as you force entry! "
                    "Guards are alerted to your presence.")
            detected = True
        self.story_label.config(text=text)
        if detected:
            self.alarm_triggered = True
            # Fight a guard responding to the alarm
            self.start_combat(enemy_name="Guard", enemy_hp=30, enemy_damage=10, enemy_weapon="bullet",
                              on_win=self.side_first_fight_win)
        else:
            # Undetected inside
            # Find the vault key guard
            if "Knife" in self.inventory:
                stealth_text = ("\nInside, you spot the guard with the vault key. "
                                "You silently eliminate him with your knife before he can react.")
                self.have_vault_key = True
            else:
                stealth_text = ("\nInside, you spot the guard with the vault key. "
                                "You shoot him with your pistol. He goes down, but the noise wasn't completely silent – the alarm starts blaring!")
                self.alarm_triggered = True
                self.have_vault_key = True
            self.story_label.config(text=text + stealth_text)
            self.proceed_to_vault_prompt()

    def side_first_fight_win(self):
        """After winning the fight at side door entry."""
        self.clear_active_widgets()
        text = ("The guard is neutralized. You dash into the building. "
                "You need to secure the vault key quickly!")
        self.story_label.config(text=text)
        btn = tk.Button(self.root, text="Find the guard with the key", command=self.side_key_guard_fight)
        btn.pack(side="top", pady=5)
        self.active_widgets = [btn]
        self.current_stage = "side_first_fight_done"
        self.update_status()

    def side_key_guard_fight(self):
        """Start fight with vault key guard on side door path."""
        self.clear_active_widgets()
        text = "You locate the guard carrying the vault key. He stands his ground, ready to fight."
        self.story_label.config(text=text)
        self.start_combat(enemy_name="Key Guard", enemy_hp=40, enemy_damage=15, enemy_weapon="bullet",
                          on_win=self.side_key_guard_defeated)

    def side_key_guard_defeated(self):
        """After defeating the vault key guard on side door path."""
        self.clear_active_widgets()
        self.have_vault_key = True
        text = "The vault key is now in your hands after defeating its holder."
        self.story_label.config(text=text)
        self.proceed_to_vault_prompt()

    def land_entry(self):
        """Execute the loud entry by crashing the van into the bank."""
        self.clear_active_widgets()
        self.alarm_triggered = True
        text = ("You slam the van through the bank's entrance! Glass shatters and alarms instantly blare. "
                "The guards inside are taken by surprise.")
        self.story_label.config(text=text)
        # Fight the first guard
        self.start_combat(enemy_name="Guard", enemy_hp=30, enemy_damage=10, enemy_weapon="bullet",
                          on_win=self.land_first_fight_win)

    def land_first_fight_win(self):
        """After defeating the first guard in land approach."""
        self.clear_active_widgets()
        text = ("One guard is down. But more security rushes in! "
                "The guard with the vault key appears amidst the chaos.")
        self.story_label.config(text=text)
        btn = tk.Button(self.root, text="Fight the guard with the key", command=self.land_second_fight)
        btn.pack(side="top", pady=5)
        self.active_widgets = [btn]
        self.current_stage = "land_first_fight_done"
        self.update_status()

    def land_second_fight(self):
        """Fight the guard carrying the vault key on land approach."""
        self.clear_active_widgets()
        text = "The guard carrying the vault key stands before you, weapon drawn."
        self.story_label.config(text=text)
        # Possibly tougher guard
        self.start_combat(enemy_name="Head Guard", enemy_hp=50, enemy_damage=15, enemy_weapon="bullet",
                          on_win=self.land_key_guard_defeated)

    def land_key_guard_defeated(self):
        """After defeating the vault key guard on land approach."""
        self.clear_active_widgets()
        self.have_vault_key = True
        text = ("The last guard falls, and you snatch the vault key from him. "
                "The path to the vault is clear.")
        self.story_label.config(text=text)
        self.proceed_to_vault_prompt()

    def roof_find_guard(self):
        """Infiltrate from roof: handle the guard with the vault key."""
        self.clear_active_widgets()
        text = ("You quietly make your way down into the building from the roof. "
                "Soon, you spot the security room where a guard seems to be carrying the vault key.")
        self.story_label.config(text=text)
        # If player has security uniform and enough money, offer bribe option
        if "Security Uniform" in self.inventory and self.player_money >= 1000:
            btn1 = tk.Button(self.root, text="Take out the guard silently", command=self.roof_kill_guard)
            btn2 = tk.Button(self.root, text="Try to bribe the guard", command=self.roof_bribe_guard)
            btn1.pack(side="top", pady=5);
            btn2.pack(side="top", pady=5)
            self.active_widgets = [btn1, btn2]
            self.current_stage = "roof_guard_options"
        else:
            # No choice, must neutralize guard
            self.roof_kill_guard()

    def roof_kill_guard(self):
        """Neutralize the guard with the vault key (kill or fight)."""
        self.clear_active_widgets()
        if "Knife" in self.inventory:
            # Silent kill
            self.have_vault_key = True
            text = ("With the guard's back turned, you silently dispatch him with your knife. "
                    "He collapses without a sound, and the vault key is now yours.")
            self.story_label.config(text=text)
            # No alarm triggered
            self.proceed_to_vault_prompt()
        else:
            # Engage in fight (gunfire, alarm triggers)
            self.alarm_triggered = True
            text = "You burst into the security room. The guard reaches for his gun - a fight breaks out!"
            self.story_label.config(text=text)
            self.start_combat(enemy_name="Key Guard", enemy_hp=40, enemy_damage=15, enemy_weapon="bullet",
                              on_win=self.roof_guard_defeated)

    def roof_guard_defeated(self):
        """After fighting and defeating the guard with the vault key (roof path)."""
        self.clear_active_widgets()
        self.have_vault_key = True
        text = ("The guard is down. You grab the vault key from his body as alarms begin to ring!")
        self.story_label.config(text=text)
        self.proceed_to_vault_prompt()

    def roof_bribe_guard(self):
        """Bribe the guard to get the vault key (roof path)."""
        self.clear_active_widgets()
        bribe_cost = 1000
        self.player_money -= bribe_cost
        self.have_vault_key = True
        text = ("Disguised in a security uniform, you manage to convince the guard to accept a bribe. "
                f"He quietly hands over the vault key in exchange for ${bribe_cost}, then slips away.")
        self.story_label.config(text=text)
        # No alarm triggered
        self.update_status()
        self.proceed_to_vault_prompt()

    def roof_direct_vault(self):
        """Skip guard and go straight to vault with thermite (roof path)."""
        self.clear_active_widgets()
        text = ("You decide to bypass the guard entirely and head straight to the vault. "
                "Reaching the vault door, you begin setting up the thermite charges.")
        self.story_label.config(text=text)
        btn = tk.Button(self.root, text="Detonate the thermite and breach the vault",
                        command=self.open_vault_with_blast)
        btn.pack(side="top", pady=5)
        self.active_widgets = [btn]
        self.current_stage = "vault_blast_ready"
        self.update_status()

    def open_vault_with_blast(self):
        """Use thermite to open the vault (triggers alarm)."""
        self.alarm_triggered = True
        self.have_vault_key = False
        self.open_vault()

    def proceed_to_vault_prompt(self):
        """Present a prompt to open the vault (after obtaining key or setting explosives)."""
        self.clear_active_widgets()
        if self.images.get("vault"):
            self.image_label.config(image=self.images["vault"])
        # Narrative based on context
        if self.have_vault_key:
            if self.alarm_triggered:
                text = ("With the vault key in hand, you race to the vault as alarms blare throughout the bank.")
            else:
                text = ("With the vault key in hand, you reach the vault door without anyone noticing.")
        else:
            # No key (using explosives)
            text = ("Having set the charges, you prepare to blast open the vault door.")
        self.story_label.config(text=text)
        action_text = "Open the vault" if self.have_vault_key else "Blast the vault"
        btn = tk.Button(self.root, text=action_text, command=self.open_vault)
        btn.pack(side="top", pady=5)
        self.active_widgets = [btn]
        self.current_stage = "vault_prompt"
        self.update_status()

    def open_vault(self):
        """Open the vault and initiate the looting mini-game."""
        self.clear_active_widgets()
        # Vault opening narrative
        if self.have_vault_key:
            if self.alarm_triggered:
                text = ("You unlock the vault door with the key. The door swings open as the alarms continue to ring.")
            else:
                text = ("You quietly unlock the vault door with the key. Inside, stacks of cash await you.")
        else:
            text = ("You detonate the thermite charges! The vault door is blown open with a thunderous blast.")
        # If vault blast triggers alarm (and wasn't already triggered)
        if not self.alarm_triggered and not self.have_vault_key:
            self.alarm_triggered = True
            text += " Alarms sound throughout the building!"
        self.story_label.config(text=text)
        # Set time limit: 30s if alarm triggered, 60s if still stealth
        self.time_left = 30 if self.alarm_triggered else 60
        # Display timer and money labels
        self.timer_label = tk.Label(self.root, text=f"Time remaining: {self.time_left} s")
        self.loot_label = tk.Label(self.root, text="Money grabbed: $0")
        self.timer_label.pack(side="top", pady=5)
        self.loot_label.pack(side="top", pady=5)
        grab_btn = tk.Button(self.root, text="Grab money!", command=self.grab_money)
        grab_btn.pack(side="top", pady=5)
        self.active_widgets = [self.timer_label, self.loot_label, grab_btn]
        self.loot_clicks = 0
        # Disable saving during timed sequence
        self.can_save = False
        # Start countdown
        self.countdown_timer(grab_btn)

    def grab_money(self):
        """Handle clicking the 'Grab money' button to accumulate cash."""
        # Increase click count if under max money
        if self.loot_clicks * 1000 < 100000:
            self.loot_clicks += 1
            amount = self.loot_clicks * 1000
            if amount > 100000:
                amount = 100000
            self.loot_label.config(text=f"Money grabbed: ${amount}")
            # If vault is maxed out at $100k, disable further clicking
            if amount >= 100000:
                for widget in self.active_widgets:
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Grab money!":
                        widget.config(state="disabled")
                        break

    def countdown_timer(self, grab_button):
        """Update the countdown timer each second, and finish looting when time is up."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time remaining: {self.time_left} s")
            # Play vault alarm sound at 15 seconds remaining, if available
            if self.time_left == 15 and playsound:
                try:
                    threading.Thread(target=playsound, args=("sound/jinku.mp3",), daemon=True).start()
                except Exception:
                    pass
            # Continue countdown
            self.root.after(1000, lambda: self.countdown_timer(grab_button))
        else:
            # Time is up
            if grab_button:
                grab_button.config(state="disabled")
            total_money = self.loot_clicks * 1000
            if total_money > 100000:
                total_money = 100000
            self.money_looted = total_money
            # Add loot to player's money
            self.player_money += self.money_looted
            # Clear vault UI and proceed to escape
            self.clear_active_widgets()
            self.escape_sequence()

    def escape_sequence(self):
        """Narrative for escaping after looting the vault."""
        if self.images.get("character"):
            self.image_label.config(image=self.images["character"])
        if self.approach_method == "roof":
            if self.alarm_triggered:
                text = ("You haul the bag of cash to the rooftop as police sirens wail. "
                        "Your helicopter pilot pulls you up under a hail of bullets, but you manage to escape with the money.")
            else:
                text = ("Carrying the bag of cash, you return to the rooftop. "
                        "The helicopter lifts off silently into the night. You've escaped without anyone noticing.")
        else:
            # Foot or land escape by vehicle
            if self.alarm_triggered:
                text = (
                    "You sprint out of the bank and jump into your getaway vehicle as sirens blare in the distance. "
                    "After a high-speed chase, you manage to lose the police and reach your safehouse.")
            else:
                text = ("You slip out of the bank with the money and blend into the darkness. "
                        "You drive to your safehouse without anyone realizing a heist took place.")
        text += f"\n\nHeist complete! You stole ${self.money_looted}."
        self.story_label.config(text=text)
        # Offer to play again or quit
        btn1 = tk.Button(self.root, text="Play Again", command=self.reset_game)
        btn2 = tk.Button(self.root, text="Quit", command=self.root.destroy)
        btn1.pack(side="top", pady=5);
        btn2.pack(side="top", pady=5)
        self.active_widgets = [btn1, btn2]
        self.current_stage = "heist_complete"
        self.can_save = True
        self.update_status()

    def start_combat(self, enemy_name, enemy_hp, enemy_damage, enemy_weapon, on_win):
        """Initialize combat interface and logic for a given enemy."""
        self.clear_active_widgets()
        self.can_save = False  # disable saving during combat
        # Store on_win callback for potential use (e.g., bribe continue)
        self.combat_on_win = on_win
        if self.images.get("gun"):
            self.image_label.config(image=self.images["gun"])
        fight_text = f"You engage in combat with the {enemy_name}!"
        self.story_label.config(text=fight_text)
        # Save enemy stats in object
        self.enemy_name = enemy_name
        self.enemy_hp = enemy_hp
        self.enemy_damage = enemy_damage
        self.enemy_weapon = enemy_weapon
        # Create roll dice button
        attack_btn = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        attack_btn.pack(side="top", pady=5)
        self.active_widgets = [attack_btn]
        self.update_status()

    def roll_dice(self):
        """Simulate one round of dice roll combat."""
        player_bonus = 0
        if "Rifle" in self.inventory:
            player_bonus = 1
        elif "Pistol" in self.inventory:
            player_bonus = 0
        else:
            player_bonus = 0
        enemy_bonus = 0
        # Roll until no tie
        player_roll = random.randint(1, 6) + player_bonus
        enemy_roll = random.randint(1, 6) + enemy_bonus
        if player_roll == enemy_roll:
            result_text = (f"You rolled {player_roll} vs {self.enemy_name} rolled {enemy_roll}. "
                           "It's a tie! No one is hurt.")
            self.story_label.config(text=result_text)
            return
        if player_roll > enemy_roll:
            # Player wins round -> enemy takes damage
            if "Rifle" in self.inventory:
                damage = 30
            elif "Pistol" in self.inventory:
                damage = 20
            elif "Knife" in self.inventory:
                damage = 15
            else:
                damage = 10
            self.enemy_hp -= damage
            result_text = (f"You rolled {player_roll} vs {self.enemy_name} rolled {enemy_roll}. "
                           f"You hit the {self.enemy_name} for {damage} damage.")
            if self.enemy_hp <= 0:
                result_text += f" The {self.enemy_name} is defeated."
        else:
            # Enemy wins round -> player takes damage
            damage = self.enemy_damage
            if self.enemy_weapon == "bullet" and self.player_armor > 0:
                if self.player_armor >= damage:
                    self.player_armor -= damage
                    damage_to_hp = 0
                else:
                    damage_to_hp = damage - self.player_armor
                    self.player_armor = 0
                if damage_to_hp > 0:
                    self.player_hp -= damage_to_hp
                result_text = (f"You rolled {player_roll} vs {self.enemy_name} rolled {enemy_roll}. "
                               f"The {self.enemy_name} hits you for {damage} damage.")
            else:
                # Melee attack or no armor left
                self.player_hp -= damage
                result_text = (f"You rolled {player_roll} vs {self.enemy_name} rolled {enemy_roll}. "
                               f"The {self.enemy_name} hits you for {damage} damage (ignores armor).")
            if self.player_hp <= 0:
                result_text += " You have been defeated."
        self.story_label.config(text=result_text)
        self.update_status()
        # Check combat end conditions
        if self.enemy_hp <= 0:
            # Enemy defeated
            self.clear_active_widgets()
            self.can_save = True
            if self.combat_on_win:
                self.combat_on_win()
        elif self.player_hp <= 0:
            # Player defeated
            self.clear_active_widgets()
            self.game_over()
        # If fight continues, leave roll button for next click

    def game_over(self):
        """Handle player defeat scenario with option to bribe or restart."""
        text = "You have been defeated."
        bribe_cost = 1000
        if self.player_money >= bribe_cost:
            text += f"\nYou can bribe the guards with ${bribe_cost} to continue."
        self.story_label.config(text=text)
        # Buttons for bribe (if possible), restart, quit
        if self.player_money >= bribe_cost:
            bribe_btn = tk.Button(self.root, text=f"Bribe (${bribe_cost})",
                                  command=lambda: self.bribe_continue(bribe_cost))
            bribe_btn.pack(side="top", pady=5)
            self.active_widgets = [bribe_btn]
        else:
            self.active_widgets = []
        restart_btn = tk.Button(self.root, text="Restart Heist", command=self.reset_game)
        quit_btn = tk.Button(self.root, text="Quit", command=self.root.destroy)
        restart_btn.pack(side="top", pady=5);
        quit_btn.pack(side="top", pady=5)
        self.active_widgets.extend([restart_btn, quit_btn])
        self.current_stage = "game_over"
        self.can_save = False  # disable saving at game over

    def bribe_continue(self, bribe_cost):
        """Continue game by bribing guards after defeat."""
        # Deduct money and revive player
        self.player_money -= bribe_cost
        self.player_hp = 100
        self.player_armor = self.player_max_armor
        # Clear game over UI
        self.clear_active_widgets()
        self.update_status()
        # Treat as victory in that combat
        if hasattr(self, "combat_on_win") and self.combat_on_win:
            self.combat_on_win()

    def reset_game(self):
        """Reset the game to initial state for a new playthrough."""
        # Reset stats and inventory
        self.player_hp = 100
        self.player_max_armor = 100
        self.player_armor = 100
        self.player_money = self.initial_money
        self.inventory = []
        self.alarm_triggered = False
        self.have_vault_key = False
        self.approach_method = None
        self.money_looted = 0
        self.can_save = True
        self.clear_active_widgets()
        if self.images.get("character"):
            self.image_label.config(image=self.images["character"])
        else:
            self.image_label.config(image="")
        self.show_intro()

    def save_game(self):
        """Save current game state to a JSON file."""
        if not self.can_save:
            return  # Do nothing if saving is currently disabled
        data = {
            "stage": getattr(self, "current_stage", None),
            "player_hp": self.player_hp,
            "player_armor": self.player_armor,
            "player_max_armor": self.player_max_armor,
            "player_money": self.player_money,
            "inventory": self.inventory,
            "alarm_triggered": self.alarm_triggered,
            "have_vault_key": self.have_vault_key,
            "approach_method": self.approach_method,
            "money_looted": self.money_looted
        }
        old_text = self.story_label.cget("text")
        try:
            with open("savegame.json", "w") as f:
                json.dump(data, f)
            # Show confirmation message briefly
            self.story_label.config(text=old_text + "\n\n(Game saved)")
            self.root.after(1000, lambda: self.story_label.config(text=old_text))
        except Exception as e:
            self.story_label.config(text=f"Save failed: {e}")

    def load_game(self):
        """Load game state from a JSON save file."""
        try:
            with open("savegame.json", "r") as f:
                data = json.load(f)
        except Exception as e:
            self.story_label.config(text=f"Load failed: {e}")
            return
        # Clear current UI
        self.clear_active_widgets()
        # Restore player state
        self.player_hp = data.get("player_hp", 100)
        self.player_armor = data.get("player_armor", 100)
        self.player_max_armor = data.get("player_max_armor", 100)
        self.player_money = data.get("player_money", self.initial_money)
        self.inventory = data.get("inventory", [])
        self.alarm_triggered = data.get("alarm_triggered", False)
        self.have_vault_key = data.get("have_vault_key", False)
        self.approach_method = data.get("approach_method", None)
        self.money_looted = data.get("money_looted", 0)
        stage = data.get("stage", None)
        self.update_status()
        # Jump to saved stage
        if stage == "shopping":
            self.show_shop()
        elif stage == "choose_approach":
            self.choose_approach()
        elif stage == "approach_on_foot":
            self.approach_on_foot()
        elif stage == "approach_by_land":
            self.approach_by_land()
        elif stage == "roof_decision":
            self.approach_from_roof()
        elif stage == "main_first_fight_done":
            self.main_first_fight_win()
        elif stage == "side_first_fight_done":
            self.side_first_fight_win()
        elif stage == "land_first_fight_done":
            self.land_first_fight_win()
        elif stage == "vault_prompt":
            self.proceed_to_vault_prompt()
        elif stage == "vault_blast_ready":
            self.roof_direct_vault()
        elif stage == "roof_guard_options":
            self.roof_find_guard()
        elif stage == "game_over":
            self.game_over()
        elif stage == "heist_complete":
            self.escape_sequence()
        else:
            # Unrecognized stage or None: restart game
            self.reset_game()


# If run as a script, start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = BankRobberyGame(root)
    root.mainloop()
