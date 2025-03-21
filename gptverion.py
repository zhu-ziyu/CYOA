import tkinter as tk
from tkinter import messagebox
import json
import os

# 游戏资源要求:
# 图片文件(保存在 images/ 文件夹):
#  - images/pistol.png (手枪图片)
#  - images/rifle.png (步枪图片)
#  - images/kevlar.png (防弹衣图片)
#  - images/medkit.png (急救包图片)
#  - images/lockpick.png (开锁工具图片)
#  - images/smoke.png (烟雾弹图片)
#  - images/hacker.png (队友"黑客"头像)
#  - images/brute.png (队友"壮汉"头像)
#  - images/driver.png (队友"司机"头像)
#  - images/inside.png (队友"内应"头像)
#  - images/vault.png (金库图片)
# 音频文件(保存在 sound/ 文件夹):
#  - sound/click.mp3 (按钮点击音效)
#  - sound/jinku.mp3 (金库倒计时音效)
#  - sound/gunshot.mp3 (战斗枪声音效)
# 注意: 需要提前安装 playsound 模块用于播放 mp3 音效 (pip install playsound)

try:
    from playsound import playsound
except ImportError:
    def playsound(file, block=True):
        print(f"[Sound file '{file}' would play here]")
    print("警告: 未安装playsound模块，游戏将无声运行。请使用 'pip install playsound' 安装。")

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RMC Bank Robbery 游戏")
        self.root.geometry("800x600")
        self.player_max_hp = 30
        self.items_data = [
            {"id": "pistol", "name": "手枪", "type": "weapon", "attack": 2, "cost": 500, "image": "images/pistol.png", "desc": "基础武器，攻击+2"},
            {"id": "rifle", "name": "步枪", "type": "weapon", "attack": 4, "cost": 1000, "image": "images/rifle.png", "desc": "强力武器，攻击+4"},
            {"id": "kevlar", "name": "防弹衣", "type": "armor", "defense": 1, "cost": 700, "image": "images/kevlar.png", "desc": "防弹衣，减少1点所受伤害"},
            {"id": "medkit", "name": "急救包", "type": "consumable", "heal": 5, "cost": 300, "image": "images/medkit.png", "desc": "医疗包，使用后恢复5点生命"},
            {"id": "lockpick", "name": "开锁工具", "type": "tool", "effect": "vault", "cost": 400, "image": "images/lockpick.png", "desc": "开锁工具，可以加快打开金库"},
            {"id": "smoke", "name": "烟雾弹", "type": "consumable", "effect": "escape", "cost": 500, "image": "images/smoke.png", "desc": "烟雾弹，可在撤退时干扰敌人"}
        ]
        self.team_data = [
            {"id": "hacker", "name": "黑客", "cost": 2000, "image": "images/hacker.png", "desc": "技术高手，能够延长金库可抢时间"},
            {"id": "brute", "name": "壮汉", "cost": 1500, "image": "images/brute.png", "desc": "身强力壮，提升你在战斗中的攻击能力"},
            {"id": "driver", "name": "司机", "cost": 1500, "image": "images/driver.png", "desc": "驾驶高手，熟悉各种逃跑路线"},
            {"id": "inside", "name": "内应", "cost": 2000, "image": "images/inside.png", "desc": "银行内应，可以帮助避开初始的保安"}
        ]
        self.images = {}
        for item in self.items_data:
            img_path = item["image"]
            key = item["id"]
            try:
                self.images[key] = tk.PhotoImage(file=img_path)
            except Exception as e:
                self.images[key] = None
                print(f"警告: 无法加载图片 {img_path}")
        for member in self.team_data:
            img_path = member["image"]
            key = member["id"]
            try:
                self.images[key] = tk.PhotoImage(file=img_path)
            except Exception as e:
                self.images[key] = None
                print(f"警告: 无法加载图片 {img_path}")
        try:
            self.images["vault"] = tk.PhotoImage(file="images/vault.png")
        except Exception as e:
            self.images["vault"] = None
            print("警告: 无法加载图片 images/vault.png")
        self.player_hp = self.player_max_hp
        self.player_money = 0
        self.player_weapon = None
        self.player_armor = None
        self.inventory = {"medkit": 0, "smoke": 0, "lockpick": 0}
        self.recruited = []
        self.loot = 0
        self.vault_time = 30
        self.current_route = None
        self.smoke_used = False
        self.show_main_menu()

    def reset_player(self):
        self.player_hp = self.player_max_hp
        self.player_money = 5000
        self.player_weapon = None
        self.player_armor = None
        self.inventory = {"medkit": 0, "smoke": 0, "lockpick": 0}
        self.recruited = []
        self.loot = 0
        self.vault_time = 30
        self.current_route = None
        self.smoke_used = False

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        title_label = tk.Label(self.root, text="RMC 银行抢劫 - 文本冒险游戏", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        newgame_btn = tk.Button(self.root, text="新的抢劫计划", font=("Arial", 14), width=20,
                                command=self.start_new_game)
        newgame_btn.pack(pady=10)
        load_btn = tk.Button(self.root, text="读取存档", font=("Arial", 14), width=20,
                              command=self.load_game)
        load_btn.pack(pady=10)
        quit_btn = tk.Button(self.root, text="退出游戏", font=("Arial", 14), width=20,
                              command=self.root.destroy)
        quit_btn.pack(pady=10)

    def start_new_game(self):
        self.reset_player()
        playsound("sound/click.mp3", block=False)
        self.show_shop()

    def show_shop(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        title = tk.Label(self.root, text=f"装备购买 - 当前资金: ${self.player_money}", font=("Arial", 14, "bold"))
        title.pack(pady=5)
        items_frame = tk.Frame(self.root)
        items_frame.pack(pady=5)
        for item in self.items_data:
            item_id = item["id"]
            name = item["name"]
            desc = item.get("desc", "")
            cost = item["cost"]
            item_type = item["type"]
            owned = False
            if item_type == "weapon":
                if self.player_weapon is not None:
                    owned = True
            elif item_type == "armor":
                if self.player_armor is not None:
                    owned = True
            elif item_type == "tool":
                if self.inventory.get(item_id, 0) > 0:
                    owned = True
            row = tk.Frame(items_frame)
            row.pack(anchor='w', padx=10, pady=2)
            if self.images.get(item_id):
                icon = tk.Label(row, image=self.images[item_id])
            else:
                icon = tk.Label(row, text="[无图片]")
            icon.pack(side='left', padx=5)
            text = f"{name} - {desc} - 价格: ${cost}"
            if item_type == "consumable":
                count = self.inventory.get(item_id, 0)
                if count > 0:
                    text += f" (已持有: {count})"
            elif item_type == "tool":
                if self.inventory.get(item_id, 0) > 0:
                    text += " (已购买)"
            info = tk.Label(row, text=text, font=("Arial", 12))
            info.pack(side='left', padx=5)
            def buy_item_action(i=item):
                self.buy_item(i)
            buy_btn = tk.Button(row, text="购买", font=("Arial", 12), command=buy_item_action)
            if owned:
                buy_btn.config(state='disabled')
            buy_btn.pack(side='left', padx=5)
        finish_btn = tk.Button(self.root, text="完成购买", font=("Arial", 14), command=self.finish_shopping)
        finish_btn.pack(pady=10)

    def buy_item(self, item):
        item_id = item["id"]
        cost = item["cost"]
        item_type = item["type"]
        if self.player_money < cost:
            playsound("sound/click.mp3", block=False)
            messagebox.showwarning("资金不足", "您没有足够的资金购买该物品！")
            return
        if item_type == "weapon" and self.player_weapon is not None:
            playsound("sound/click.mp3", block=False)
            messagebox.showwarning("装备限制", "您已经拥有武器，不能购买更多武器！")
            return
        if item_type == "armor" and self.player_armor is not None:
            playsound("sound/click.mp3", block=False)
            messagebox.showwarning("装备限制", "您已经拥有防具，不能购买更多防具！")
            return
        if item_type == "tool" and self.inventory.get(item_id, 0) > 0:
            playsound("sound/click.mp3", block=False)
            messagebox.showwarning("装备限制", f"您已经拥有{item['name']}！")
            return
        self.player_money -= cost
        if item_type == "weapon":
            self.player_weapon = item
        elif item_type == "armor":
            self.player_armor = item
        elif item_type == "consumable":
            self.inventory[item_id] = self.inventory.get(item_id, 0) + 1
        elif item_type == "tool":
            self.inventory[item_id] = 1
        playsound("sound/click.mp3", block=False)
        self.show_shop()

    def finish_shopping(self):
        playsound("sound/click.mp3", block=False)
        self.show_recruit()

    def show_recruit(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        title = tk.Label(self.root, text=f"队友招募 - 当前资金: ${self.player_money}", font=("Arial", 14, "bold"))
        title.pack(pady=5)
        team_frame = tk.Frame(self.root)
        team_frame.pack(pady=5)
        for member in self.team_data:
            mid = member["id"]
            name = member["name"]
            desc = member["desc"]
            cost = member["cost"]
            row = tk.Frame(team_frame)
            row.pack(anchor='w', padx=10, pady=2)
            if self.images.get(mid):
                icon = tk.Label(row, image=self.images[mid])
            else:
                icon = tk.Label(row, text="[无图片]")
            icon.pack(side='left', padx=5)
            text = f"{name} - {desc} - 招募费用: ${cost}"
            info = tk.Label(row, text=text, font=("Arial", 12))
            info.pack(side='left', padx=5)
            def recruit_action(m=member):
                self.recruit_member(m)
            recruit_btn = tk.Button(row, text="招募", font=("Arial", 12), command=recruit_action)
            if mid in self.recruited:
                recruit_btn.config(state='disabled', text="已招募")
            elif self.player_money < cost:
                recruit_btn.config(state='disabled')
            recruit_btn.pack(side='left', padx=5)
        finish_btn = tk.Button(self.root, text="完成招募", font=("Arial", 14), command=self.finish_recruitment)
        finish_btn.pack(pady=10)

    def recruit_member(self, member):
        mid = member["id"]
        cost = member["cost"]
        if self.player_money < cost:
            playsound("sound/click.mp3", block=False)
            messagebox.showwarning("资金不足", "您没有足够的资金招募该队友！")
            return
        if mid in self.recruited:
            playsound("sound/click.mp3", block=False)
            messagebox.showinfo("提示", f"{member['name']} 已在您的队伍中。")
            return
        self.player_money -= cost
        self.recruited.append(mid)
        playsound("sound/click.mp3", block=False)
        self.show_recruit()

    def finish_recruitment(self):
        playsound("sound/click.mp3", block=False)
        self.start_heist()

    def start_heist(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if "inside" in self.recruited:
            text = "在内应的帮助下，你顺利混入银行，避开了大厅的保安。"
            info_label = tk.Label(self.root, text=text, font=("Arial", 14))
            info_label.pack(pady=20)
            continue_btn = tk.Button(self.root, text="继续", font=("Arial", 14),
                                     command=self.enter_vault)
            continue_btn.pack(pady=5)
        else:
            text = "你走进银行大厅，一名保安发现了你！看来不得不硬拼。"
            info_label = tk.Label(self.root, text=text, font=("Arial", 14))
            info_label.pack(pady=20)
            fight_btn = tk.Button(self.root, text="进入战斗", font=("Arial", 14),
                                   command=self.fight_guard)
            fight_btn.pack(pady=5)
        save_btn = tk.Button(self.root, text="保存游戏", font=("Arial", 12), command=self.save_game)
        save_btn.pack(pady=10)

    def fight_guard(self):
        guard = {"name": "保安", "hp": 15, "power": 1}
        self.current_route = None
        self.run_combat(enemy=guard, final=False)

    def enter_vault(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if "hacker" in self.recruited or self.inventory.get("lockpick", 0) > 0:
            self.vault_time = 60
        else:
            self.vault_time = 30
        instr = f"开始抢劫金库！你有{self.vault_time}秒时间搜刮现金。"
        instr_label = tk.Label(self.root, text=instr, font=("Arial", 14))
        instr_label.pack(pady=10)
        if self.images.get("vault"):
            vault_img_label = tk.Label(self.root, image=self.images["vault"])
            vault_img_label.pack(pady=5)
        self.time_left = self.vault_time
        self.money_collected = 0
        timer_text = tk.StringVar()
        timer_text.set(f"剩余时间: {self.time_left} 秒")
        self.timer_label = tk.Label(self.root, textvariable=timer_text, font=("Arial", 14))
        self.timer_label.pack(pady=5)
        money_text = tk.StringVar()
        money_text.set(f"已获取金钱: ${self.money_collected}")
        self.money_label = tk.Label(self.root, textvariable=money_text, font=("Arial", 14))
        self.money_label.pack(pady=5)
        grab_btn = tk.Button(self.root, text="拿钱!", font=("Arial", 14),
                              command=lambda: self.grab_money(money_text))
        grab_btn.pack(pady=10)
        self.grab_button = grab_btn
        self.update_timer(timer_text)

    def update_timer(self, timer_text):
        timer_text.set(f"剩余时间: {self.time_left} 秒")
        if self.time_left == 15:
            playsound("sound/jinku.mp3", block=False)
        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, lambda: self.update_timer(timer_text))
        else:
            if hasattr(self, "grab_button"):
                self.grab_button.config(state='disabled')
            self.loot = self.money_collected
            self.player_money += self.loot
            self.root.after(500, self.choose_escape_route)

    def grab_money(self, money_text_var):
        if self.time_left <= 0:
            return
        if self.money_collected < 100000:
            self.money_collected += 1000
            if self.money_collected > 100000:
                self.money_collected = 100000
            money_text_var.set(f"已获取金钱: ${self.money_collected}")
            playsound("sound/click.mp3", block=False)
            if self.money_collected >= 100000:
                if hasattr(self, "grab_button"):
                    self.grab_button.config(state='disabled', text="已装满")
        else:
            if hasattr(self, "grab_button"):
                self.grab_button.config(state='disabled')

    def choose_escape_route(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        info_label = tk.Label(self.root, text=f"你从金库抢到了 ${self.loot}！", font=("Arial", 14))
        info_label.pack(pady=10)
        instr_label = tk.Label(self.root, text="选择撤退路线：", font=("Arial", 14))
        instr_label.pack(pady=5)
        front_btn = tk.Button(self.root, text="正面突围", font=("Arial", 14),
                              command=lambda: self.escape_route("front"))
        front_btn.pack(pady=5)
        alley_btn = tk.Button(self.root, text="后巷撤离", font=("Arial", 14),
                              command=lambda: self.escape_route("alley"))
        alley_btn.pack(pady=5)
        car_btn = tk.Button(self.root, text="驾车逃逸", font=("Arial", 14),
                              command=lambda: self.escape_route("car"))
        car_btn.pack(pady=5)
        save_btn = tk.Button(self.root, text="保存游戏", font=("Arial", 12), command=self.save_game)
        save_btn.pack(pady=10)

    def escape_route(self, route):
        playsound("sound/click.mp3", block=False)
        if route == "front":
            if self.inventory.get("smoke", 0) > 0:
                for widget in self.root.winfo_children():
                    widget.destroy()
                text = "正门出口有大量警察等待。您有烟雾弹，可以掩护撤退。"
                label = tk.Label(self.root, text=text, font=("Arial", 14))
                label.pack(pady=20)
                use_smoke_btn = tk.Button(self.root, text="使用烟雾弹逃脱", font=("Arial", 14),
                                           command=lambda: self.use_smoke_then_success("front"))
                fight_btn = tk.Button(self.root, text="硬闯突围", font=("Arial", 14),
                                       command=lambda: self.fight_escape("front"))
                use_smoke_btn.pack(pady=5)
                fight_btn.pack(pady=5)
            else:
                self.fight_escape("front")
        elif route == "alley":
            if self.inventory.get("smoke", 0) > 0:
                self.smoke_used = True
                self.inventory["smoke"] -= 1
                outcome_text = "你从后巷撤离，并使用了烟雾弹掩护，全身而退，所有金钱毫发无损！"
            else:
                lost_amount = int(self.loot * 0.2)
                if lost_amount < 0:
                    lost_amount = 0
                self.player_money -= lost_amount
                self.loot -= lost_amount
                outcome_text = f"你从后巷迅速撤离。为了加快速度，不得不丢下了一部分现金（损失${lost_amount}）。"
            self.show_success(outcome_text)
        elif route == "car":
            if "driver" in self.recruited:
                outcome_text = "您的司机早已在外接应。你跳上车，在司机高超的车技下成功甩开了警察！"
                self.show_success(outcome_text)
            else:
                if self.inventory.get("smoke", 0) > 0:
                    for widget in self.root.winfo_children():
                        widget.destroy()
                    text = "警察正在追赶您的车辆！您有烟雾弹，可以用来甩开他们。"
                    label = tk.Label(self.root, text=text, font=("Arial", 14))
                    label.pack(pady=20)
                    use_smoke_btn = tk.Button(self.root, text="使用烟雾弹摆脱警察", font=("Arial", 14),
                                               command=lambda: self.use_smoke_then_success("car"))
                    fight_btn = tk.Button(self.root, text="与警车交火", font=("Arial", 14),
                                           command=lambda: self.fight_escape("car"))
                    use_smoke_btn.pack(pady=5)
                    fight_btn.pack(pady=5)
                else:
                    self.fight_escape("car")

    def use_smoke_then_success(self, route):
        if self.inventory.get("smoke", 0) > 0:
            self.inventory["smoke"] -= 1
            self.smoke_used = True
        if route == "front":
            outcome_text = "你投掷了一枚烟雾弹，趁着浓烟掩护，你成功冲出重围！"
        elif route == "car":
            outcome_text = "你向后抛出一枚烟雾弹，警车被烟雾干扰，你趁机摆脱了追兵！"
        else:
            outcome_text = ""
        self.show_success(outcome_text)

    def fight_escape(self, route):
        if route == "front":
            enemy = {"name": "特警", "hp": 30, "power": 3}
            narrative = "你选择正面突围！大量武装警察堵在门口，枪战爆发！"
        elif route == "car":
            enemy = {"name": "警察", "hp": 20, "power": 2}
            narrative = "你开车冲出停车场，警察在后紧追不舍，试图逼停你！"
        else:
            return
        for widget in self.root.winfo_children():
            widget.destroy()
        label = tk.Label(self.root, text=narrative, font=("Arial", 14))
        label.pack(pady=20)
        fight_btn = tk.Button(self.root, text="战斗", font=("Arial", 14),
                               command=lambda: self.start_escape_combat(enemy, route))
        fight_btn.pack(pady=10)

    def start_escape_combat(self, enemy, route):
        self.current_route = route
        self.run_combat(enemy=enemy, final=True)

    def run_combat(self, enemy, final):
        for widget in self.root.winfo_children():
            widget.destroy()
        enemy_name = enemy["name"]
        enemy_hp = enemy["hp"]
        enemy_power = enemy["power"]
        self.current_enemy_hp = enemy_hp
        self.current_enemy = enemy
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)
        status_label = tk.Label(top_frame, text=f"敌人: {enemy_name} HP: {self.current_enemy_hp}    玩家HP: {self.player_hp}", font=("Arial", 12))
        status_label.pack()
        log = tk.Text(self.root, height=10, width=60, font=("Arial", 12))
        log.pack(pady=5)
        log.config(state=tk.NORMAL)
        if enemy_name == "保安":
            log.insert(tk.END, "战斗开始！对抗银行保安。\n")
        else:
            if self.current_route == "front":
                log.insert(tk.END, "战斗开始！你与特警展开激烈枪战！\n")
            elif self.current_route == "car":
                log.insert(tk.END, "战斗开始！你与警车上的警察交火！\n")
            else:
                log.insert(tk.END, "战斗开始！\n")
        log.config(state=tk.DISABLED)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        def attack_action():
            self.combat_round(status_label, log, final)
        attack_btn = tk.Button(btn_frame, text="攻击", font=("Arial", 12), command=attack_action)
        attack_btn.grid(row=0, column=0, padx=10)
        medkit_btn = None
        if self.inventory.get("medkit", 0) > 0:
            def heal_action():
                self.use_medkit(status_label, log, final)
            medkit_btn = tk.Button(btn_frame, text=f"急救包 x{self.inventory['medkit']}", font=("Arial", 12), command=heal_action)
            medkit_btn.grid(row=0, column=1, padx=10)
        self.attack_button = attack_btn
        self.medkit_button = medkit_btn

    def combat_round(self, status_label, log_widget, final):
        log_widget.config(state=tk.NORMAL)
        player_roll = __import__('random').randint(1, 6)
        dmg = player_roll
        if self.player_weapon:
            dmg += self.player_weapon.get("attack", 0)
        if "brute" in self.recruited:
            dmg += 2
        self.current_enemy_hp -= dmg
        log_widget.insert(tk.END, f"你掷出了{player_roll}点，造成了{dmg}点伤害！\n")
        playsound("sound/gunshot.mp3", block=False)
        if self.current_enemy_hp <= 0:
            self.current_enemy_hp = 0
            log_widget.insert(tk.END, f"敌人{self.current_enemy['name']}被击倒了！\n")
            status_label.config(text=f"敌人: {self.current_enemy['name']} HP: {self.current_enemy_hp}    玩家HP: {self.player_hp}")
            self.attack_button.config(state='disabled')
            if self.medkit_button:
                self.medkit_button.config(state='disabled')
            log_widget.insert(tk.END, "战斗胜利！\n")
            log_widget.config(state=tk.DISABLED)
            btn = tk.Button(self.root, text="继续", font=("Arial", 14))
            if final:
                btn.config(text="完成抢劫", command=self.end_success)
            else:
                btn.config(text="进入金库", command=self.enter_vault)
            btn.pack(pady=10)
            return
        status_label.config(text=f"敌人: {self.current_enemy['name']} HP: {self.current_enemy_hp}    玩家HP: {self.player_hp}")
        enemy_roll = __import__('random').randint(1, 6)
        enemy_dmg = enemy_roll + self.current_enemy.get("power", 0)
        if self.player_armor:
            enemy_dmg -= self.player_armor.get("defense", 0)
            if enemy_dmg < 0:
                enemy_dmg = 0
        if enemy_dmg < 0:
            enemy_dmg = 0
        self.player_hp -= enemy_dmg
        log_widget.insert(tk.END, f"敌人攻击造成了{enemy_dmg}点伤害！\n")
        playsound("sound/gunshot.mp3", block=False)
        if self.player_hp < 0:
            self.player_hp = 0
        status_label.config(text=f"敌人: {self.current_enemy['name']} HP: {self.current_enemy_hp}    玩家HP: {self.player_hp}")
        if self.player_hp <= 0:
            log_widget.insert(tk.END, "你受到了致命伤害！\n")
            log_widget.config(state=tk.DISABLED)
            self.attack_button.config(state='disabled')
            if self.medkit_button:
                self.medkit_button.config(state='disabled')
            messagebox.showerror("游戏结束", "你已经倒下，抢劫计划失败了！")
            self.show_game_over()
            return
        log_widget.config(state=tk.DISABLED)

    def use_medkit(self, status_label, log_widget, final):
        log_widget.config(state=tk.NORMAL)
        if self.inventory.get("medkit", 0) > 0 and self.player_hp > 0:
            heal_amount = 5
            if self.player_hp + heal_amount > self.player_max_hp:
                heal_amount = self.player_max_hp - self.player_hp
            self.player_hp += heal_amount
            self.inventory["medkit"] -= 1
            log_widget.insert(tk.END, f"你使用急救包，恢复了{heal_amount}点生命值。\n")
            playsound("sound/click.mp3", block=False)
            if self.medkit_button:
                if self.inventory["medkit"] > 0:
                    self.medkit_button.config(text=f"急救包 x{self.inventory['medkit']}")
                else:
                    self.medkit_button.config(state='disabled', text="急救包 x0")
            enemy_roll = __import__('random').randint(1, 6)
            enemy_dmg = enemy_roll + self.current_enemy.get("power", 0)
            if self.player_armor:
                enemy_dmg -= self.player_armor.get("defense", 0)
                if enemy_dmg < 0:
                    enemy_dmg = 0
            self.player_hp -= enemy_dmg
            log_widget.insert(tk.END, f"敌人趁机攻击，造成了{enemy_dmg}点伤害！\n")
            playsound("sound/gunshot.mp3", block=False)
            if self.player_hp < 0:
                self.player_hp = 0
            status_label.config(text=f"敌人: {self.current_enemy['name']} HP: {self.current_enemy_hp}    玩家HP: {self.player_hp}")
            if self.player_hp <= 0:
                log_widget.insert(tk.END, "你受到了致命伤害！\n")
                log_widget.config(state=tk.DISABLED)
                self.attack_button.config(state='disabled')
                if self.medkit_button:
                    self.medkit_button.config(state='disabled')
                messagebox.showerror("游戏结束", "你已经倒下，抢劫计划失败了！")
                self.show_game_over()
                return
        log_widget.config(state=tk.DISABLED)

    def end_success(self):
        outcome_text = ""
        if self.current_route == "front":
            outcome_text = "你成功击退了所有警察，从正门杀出一条血路！"
        elif self.current_route == "car":
            outcome_text = "你击退了追击的警察，成功驾车逃脱！"
        self.show_success(outcome_text)

    def show_success(self, narrative=""):
        for widget in self.root.winfo_children():
            widget.destroy()
        if narrative:
            narrative_label = tk.Label(self.root, text=narrative, font=("Arial", 14))
            narrative_label.pack(pady=10)
        result_text = f"抢劫成功！共计获得现金 ${self.loot}。"
        result_label = tk.Label(self.root, text=result_text, font=("Arial", 16, "bold"))
        result_label.pack(pady=20)
        menu_btn = tk.Button(self.root, text="返回主菜单", font=("Arial", 14), command=self.show_main_menu)
        menu_btn.pack(pady=5)
        quit_btn = tk.Button(self.root, text="退出游戏", font=("Arial", 14), command=self.root.destroy)
        quit_btn.pack(pady=5)

    def show_game_over(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        over_label = tk.Label(self.root, text="抢劫失败！", font=("Arial", 16, "bold"), fg="red")
        over_label.pack(pady=20)
        menu_btn = tk.Button(self.root, text="返回主菜单", font=("Arial", 14), command=self.show_main_menu)
        menu_btn.pack(pady=5)
        quit_btn = tk.Button(self.root, text="退出游戏", font=("Arial", 14), command=self.root.destroy)
        quit_btn.pack(pady=5)

    def save_game(self):
        state = {
            "player_hp": self.player_hp,
            "player_money": self.player_money,
            "player_max_hp": self.player_max_hp,
            "loot": self.loot,
            "inventory": self.inventory,
            "weapon": self.player_weapon["id"] if self.player_weapon else None,
            "armor": self.player_armor["id"] if self.player_armor else None,
            "recruited": self.recruited,
            "stage": None
        }
        if self.loot > 0 and (not state["stage"]):
            state["stage"] = "escape"
        if state["stage"] is None:
            state["stage"] = "heist_start"
        try:
            with open("savegame.json", "w") as f:
                json.dump(state, f)
            messagebox.showinfo("保存成功", "游戏进度已保存!")
        except Exception as e:
            messagebox.showerror("保存失败", f"无法保存游戏: {e}")

    def load_game(self):
        try:
            with open("savegame.json", "r") as f:
                state = json.load(f)
        except FileNotFoundError:
            messagebox.showwarning("无存档", "未找到存档文件。")
            return
        except Exception as e:
            messagebox.showerror("读取错误", f"存档文件读取失败: {e}")
            return
        self.player_hp = state.get("player_hp", self.player_max_hp)
        self.player_money = state.get("player_money", 0)
        self.loot = state.get("loot", 0)
        inv = state.get("inventory", {})
        for key in ["medkit", "smoke", "lockpick"]:
            self.inventory[key] = inv.get(key, 0)
        weapon_id = state.get("weapon")
        armor_id = state.get("armor")
        self.player_weapon = None
        self.player_armor = None
        if weapon_id:
            for it in self.items_data:
                if it["id"] == weapon_id:
                    self.player_weapon = it
                    break
        if armor_id:
            for it in self.items_data:
                if it["id"] == armor_id:
                    self.player_armor = it
                    break
        self.recruited = state.get("recruited", [])
        stage = state.get("stage", "heist_start")
        if stage == "heist_start":
            self.start_heist()
        elif stage == "escape":
            self.choose_escape_route()
        else:
            self.start_heist()

if __name__ == "__main__":
    game = Game()
    game.root.mainloop()
