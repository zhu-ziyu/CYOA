import tkinter as tk
import json
import random
import threading
import time
import os

try:
    from playsound import playsound
except ImportError:
    playsound = None


# --------------------------
# 辅助函数：播放音频
# --------------------------
def play_sound(sound_path):
    if playsound:
        try:
            threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
        except Exception as e:
            print("播放音频失败：", e)


# --------------------------
# 同伙类：记录同伙数据及技能
# --------------------------
class Associate:
    def __init__(self, name, share, description, skill_func):
        self.name = name
        self.share = share
        self.description = description
        self.skill_func = skill_func
        self.used = False

    def activate_skill(self, game):
        if not self.used:
            self.skill_func(game)
            self.used = True
        else:
            game.add_log(f"{self.name} 的技能已使用。")


# --------------------------
# 游戏主类
# --------------------------
class BankRobberyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("RMC Bank Robbery - Text Adventure")
        self.root.geometry("800x600")
        self.current_stage = "intro"

        # 玩家初始属性
        self.initial_money = 3000
        self.player_hp = 100
        self.player_max_hp = 100
        self.player_armor = 100
        self.player_max_armor = 100
        self.player_money = self.initial_money
        self.inventory = []  # 装备列表
        self.offsite_team = []  # 离线支援人员
        self.associates = {}  # 同伙字典，键为名称
        self.associate_active = False

        # 战斗属性
        self.enemy_hp = 0
        self.enemy_damage = 0
        self.enemy_name = ""
        self.combat_on_win = None

        # 金库抢劫相关
        self.have_vault_key = False
        self.alarm_triggered = False
        self.loot_clicks = 0
        self.money_looted = 0
        self.loot_time = 0

        # 存档开关（战斗中禁止存档）
        self.can_save = True

        # 日志记录（显示在状态栏中）
        self.log_messages = []

        # 加载图片资源
        self.images = {}
        self.load_images()

        # 创建菜单
        self.create_menu()

        # 创建界面基本元素
        self.create_ui_elements()

        # 初始化动态控件列表
        self.active_widgets = []

        # 开始游戏流程
        self.show_intro()

    # --------------------------
    # 加载图片资源
    # --------------------------
    def load_images(self):
        image_files = {
            "character": "image/character.png",
            "vault": "image/vault.png",
            "gun": "image/gun.png",
            "item": "image/item.png",
            "vehicle": "image/vehicle.png",
            "background": "image/background.png"
        }
        for key, path in image_files.items():
            try:
                self.images[key] = tk.PhotoImage(file=path)
            except Exception as e:
                print(f"加载图片 {path} 失败: {e}")
                self.images[key] = None

    # --------------------------
    # 创建菜单
    # --------------------------
    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="保存游戏", command=self.save_game)
        file_menu.add_command(label="加载游戏", command=self.load_game)
        menubar.add_cascade(label="文件", menu=file_menu)
        self.root.config(menu=menubar)

    # --------------------------
    # 创建基本 UI 元素
    # --------------------------
    def create_ui_elements(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack(pady=5)

        self.story_label = tk.Label(self.main_frame, text="", wraplength=750, justify="left", font=("Arial", 14))
        self.story_label.pack(padx=10, pady=10)

        self.status_label = tk.Label(self.root, text="", anchor="w", font=("Courier", 12), bg="#EEE")
        self.status_label.pack(side="bottom", fill="x")

        self.update_status()

    # --------------------------
    # 清除当前动态控件
    # --------------------------
    def clear_active_widgets(self):
        if hasattr(self, "active_widgets"):
            for widget in self.active_widgets:
                try:
                    widget.destroy()
                except Exception:
                    pass
            self.active_widgets = []

    # --------------------------
    # 更新状态栏信息
    # --------------------------
    def update_status(self):
        inv = ", ".join(self.inventory) if self.inventory else "None"
        offsite = ", ".join(self.offsite_team) if self.offsite_team else "None"
        assoc = ", ".join(self.associates.keys()) if self.associates else "None"
        log_text = "\n".join(self.log_messages[-3:])  # 最近 3 条日志
        status = (
            f"HP: {self.player_hp}/{self.player_max_hp}    Armor: {self.player_armor}/{self.player_max_armor}    Money: ${self.player_money}\n"
            f"Inventory: {inv}\n"
            f"离线支援: {offsite}\n"
            f"同伙: {assoc}\n"
            f"日志: {log_text}")
        self.status_label.config(text=status)

    # --------------------------
    # 添加日志信息
    # --------------------------
    def add_log(self, message):
        self.log_messages.append(message)
        self.update_status()

    # --------------------------
    # 游戏流程 – 介绍阶段
    # --------------------------
    def show_intro(self):
        self.clear_active_widgets()
        self.current_stage = "intro"
        if self.images.get("background"):
            self.image_label.config(image=self.images["background"])
        else:
            self.image_label.config(image="")
        intro_text = (
            "欢迎来到 RMC Bank Robbery！\n\n"
            "你是一名技艺高超的职业盗贼，准备抢劫 RMC 银行。"
            "在这场高风险高回报的行动中，你需要精心准备装备、招聘人员，并选择最佳作案路线。\n\n"
            "点击‘开始游戏’开启你的冒险！"
        )
        self.story_label.config(text=intro_text)
        start_btn = tk.Button(self.main_frame, text="开始游戏", font=("Arial", 14), command=self.show_equipment_shop)
        start_btn.pack(pady=10)
        self.active_widgets.append(start_btn)
        self.add_log("进入介绍阶段。")

    # --------------------------
    # 装备购买阶段
    # --------------------------
    def show_equipment_shop(self):
        self.clear_active_widgets()
        self.current_stage = "equipment_shop"
        if self.images.get("item"):
            self.image_label.config(image=self.images["item"])
        shop_text = (
            "装备商店：\n\n"
            "使用初始资金购买装备，每件装备都有助于提高成功率和战斗力。\n"
            "注意：部分接近工具（如黑客工具、安全制服）需要花费金钱！"
        )
        self.story_label.config(text=shop_text)
        self.equipment_items = [
            {"name": "Camouflage Suit", "price": 500, "desc": "隐蔽服装，降低被发现概率。"},
            {"name": "Hacking Tool", "price": 500, "desc": "黑客工具，辅助无声入侵侧门。"},
            {"name": "Thermite", "price": 1000, "desc": "热化学炸药，用于炸开金库门。"},
            {"name": "Security Uniform", "price": 800, "desc": "安全制服，便于贿赂保安。"},
            {"name": "Kevlar Vest", "price": 300, "desc": "防弹背心，提高护甲。"},
            {"name": "Decoy Crew", "price": 600, "desc": "诱饵小队，撤退时可分散敌人火力。"},
            {"name": "Getaway Vehicle", "price": 1200, "desc": "逃逸工具，有陆地与空中两种型号。"},
            {"name": "Tarkov Brand Backpack", "price": 400, "desc": "大容量背包，减少受击掉钱。"},
            {"name": "Heavy Firepower", "price": 1500, "desc": "重火力支援，增加伤害。"}
        ]
        self.shop_frame = tk.Frame(self.main_frame)
        self.shop_frame.pack(pady=5)
        for idx, item in enumerate(self.equipment_items):
            name = item["name"]
            price = item["price"]
            desc = item["desc"]
            lbl = tk.Label(self.shop_frame, text=f"{name} - ${price}: {desc}", anchor="w", justify="left",
                           font=("Arial", 12))
            lbl.grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            btn = tk.Button(self.shop_frame, text="购买", command=lambda n=name, p=price: self.buy_equipment(n, p))
            btn.grid(row=idx, column=1, padx=5, pady=2)
        done_btn = tk.Button(self.main_frame, text="完成购买", font=("Arial", 14), command=self.finish_equipment_shop)
        done_btn.pack(pady=10)
        self.active_widgets.extend([self.shop_frame, done_btn])
        self.add_log("装备购买阶段完成。")
        self.update_status()

    def buy_equipment(self, name, price):
        if name in self.inventory:
            self.add_log(f"{name} 已购买。")
            return
        if self.player_money >= price:
            self.player_money -= price
            self.inventory.append(name)
            self.add_log(f"成功购买 {name}，花费 ${price}。")
            # 部分装备立即生效
            if name == "Kevlar Vest":
                self.player_max_armor = 150
                self.player_armor = 150
        else:
            self.add_log(f"资金不足，无法购买 {name}。")
        self.update_status()

    def finish_equipment_shop(self):
        self.clear_active_widgets()
        self.add_log("装备购买结束。")
        # 装备购买结束后，进入人员招聘阶段
        self.show_personnel_recruitment()

    # --------------------------
    # 人员招聘阶段（离线支援和同伙招募）
    # --------------------------
    def show_personnel_recruitment(self):
        self.current_stage = "personnel_recruitment"
        self.clear_active_widgets()
        recruitment_text = (
            "人员招聘阶段：\n\n"
            "为确保抢劫成功，你可以选择以下两种招聘方式：\n"
            "1. 离线支援：使用默认资金雇佣专业人员，减少随机不利事件。\n"
            "   可选项：Hacker、Security Personnel、Guard Equipment Manufacturer。\n\n"
            "2. 同伙招募：用未来抢劫收益中的一部分作为分成，招募同伙，他们在战斗中可释放特殊技能。\n"
            "   可选项：Fool (10% share)、Retired Military (30%)、Robot Manufacturer (70%)、Teacher (50%)、SAM (0%)。\n\n"
            "请选择你要采用的招聘方式。"
        )
        self.story_label.config(text=recruitment_text)
        btn_offsite = tk.Button(self.main_frame, text="离线支援", font=("Arial", 14),
                                command=self.show_offsite_recruitment)
        btn_associates = tk.Button(self.main_frame, text="同伙招募", font=("Arial", 14),
                                   command=self.show_associates_recruitment)
        btn_offsite.pack(pady=5)
        btn_associates.pack(pady=5)
        self.active_widgets.extend([btn_offsite, btn_associates])
        self.add_log("进入人员招聘阶段。")
        self.update_status()

    def show_offsite_recruitment(self):
        self.current_stage = "offsite_recruitment"
        self.clear_active_widgets()
        text = (
            "离线支援招聘：\n\n"
            "你可以花费一定金额雇佣以下人员，帮助降低随机不利事件的发生率。\n"
            "1. Hacker - $500\n"
            "2. Security Personnel - $800\n"
            "3. Guard Equipment Manufacturer - $1000\n\n"
            "请选择你要雇佣的人员（可多选，每种仅限一次）。"
        )
        self.story_label.config(text=text)
        self.offsite_options = [
            {"name": "Hacker", "price": 500},
            {"name": "Security Personnel", "price": 800},
            {"name": "Guard Equipment Manufacturer", "price": 1000}
        ]
        self.offsite_frame = tk.Frame(self.main_frame)
        self.offsite_frame.pack(pady=5)
        for idx, option in enumerate(self.offsite_options):
            name = option["name"]
            price = option["price"]
            lbl = tk.Label(self.offsite_frame, text=f"{name} - ${price}", font=("Arial", 12))
            lbl.grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            btn = tk.Button(self.offsite_frame, text="雇佣", command=lambda n=name, p=price: self.hire_offsite(n, p))
            btn.grid(row=idx, column=1, padx=5, pady=2)
        done_btn = tk.Button(self.main_frame, text="完成雇佣", font=("Arial", 14),
                             command=self.after_recruitment_choice)
        done_btn.pack(pady=10)
        self.active_widgets.extend([self.offsite_frame, done_btn])
        self.add_log("选择离线支援人员。")
        self.update_status()

    def hire_offsite(self, name, price):
        if name in self.offsite_team:
            self.add_log(f"{name} 已经雇佣。")
            return
        if self.player_money >= price:
            self.player_money -= price
            self.offsite_team.append(name)
            self.add_log(f"成功雇佣 {name}，花费 ${price}。")
        else:
            self.add_log(f"资金不足，无法雇佣 {name}。")
        self.update_status()

    def show_associates_recruitment(self):
        self.current_stage = "associates_recruitment"
        self.clear_active_widgets()
        text = (
            "同伙招募：\n\n"
            "你可以用未来抢劫收益中的一部分作为分成，招募同伙，他们在战斗中可释放特殊技能。\n"
            "可选项：\n"
            "1. Fool (10% share) - 技能：对所有敌人造成 10 点伤害，但有 10% 反伤风险。\n"
            "2. Retired Military (30%) - 技能：使用热武器，范围伤害，每个敌人 5 点伤害。\n"
            "3. Robot Manufacturer (70%) - 技能：使用机枪，每轮减少 50% 受到的伤害。\n"
            "4. Teacher (50%) - 技能：有 50% 复活机会，并可能令部分敌人叛变。\n"
            "5. SAM (0%) - 技能：测试用，同伙使玩家伤害和血量翻倍。\n\n"
            "请选择你要招募的同伙（可多选，每个同伙仅限一次）。"
        )
        self.story_label.config(text=text)
        self.associates_options = [
            {"name": "Fool", "share": 10, "desc": "不使用热武器，对全体敌人造成 10 点伤害，但有 10% 反伤风险。",
             "skill": self.skill_fool},
            {"name": "Retired Military", "share": 30, "desc": "擅长热武器，范围伤害，每个敌人 5 点伤害。",
             "skill": self.skill_retired_military},
            {"name": "Robot Manufacturer", "share": 70, "desc": "高伤害机枪支援，每轮减少 50% 受到的伤害。",
             "skill": self.skill_robot_manufacturer},
            {"name": "Teacher", "share": 50, "desc": "复活几率 50%，并有 30% 敌人叛变可能。",
             "skill": self.skill_teacher},
            {"name": "SAM", "share": 0, "desc": "测试用同伙，技能使玩家伤害和血量各翻倍。",
             "skill": self.skill_sam}
        ]
        self.associates_frame = tk.Frame(self.main_frame)
        self.associates_frame.pack(pady=5)
        for idx, option in enumerate(self.associates_options):
            name = option["name"]
            share = option["share"]
            desc = option["desc"]
            lbl = tk.Label(self.associates_frame, text=f"{name} ({share}% share): {desc}", font=("Arial", 12),
                           justify="left")
            lbl.grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            btn = tk.Button(self.associates_frame, text="招募", command=lambda opt=option: self.recruit_associate(opt))
            btn.grid(row=idx, column=1, padx=5, pady=2)
        done_btn = tk.Button(self.main_frame, text="完成招募", font=("Arial", 14),
                             command=self.after_recruitment_choice)
        done_btn.pack(pady=10)
        self.active_widgets.extend([self.associates_frame, done_btn])
        self.add_log("选择同伙招募。")
        self.update_status()

    def recruit_associate(self, option):
        name = option["name"]
        if name in self.associates:
            self.add_log(f"{name} 已经招募。")
            return
        assoc = Associate(name, option["share"], option["desc"], option["skill"])
        self.associates[name] = assoc
        self.add_log(f"成功招募同伙：{name}。")
        self.update_status()

    def after_recruitment_choice(self):
        self.clear_active_widgets()
        self.add_log("人员招聘结束。")
        self.show_approach_selection()

    # --------------------------
    # 作案方式选择阶段
    # --------------------------
    def show_approach_selection(self):
        self.current_stage = "approach_selection"
        self.clear_active_widgets()
        text = (
            "作案方式选择：\n\n"
            "你可以选择以下接近银行的方式：\n"
            "1. 徒步接近（隐蔽潜行，可选择正门或侧门进入）\n"
            "2. 陆地载具（驾车撞门，重火力作战）\n"
            "3. 空中载具（直升机从屋顶进入，适合空降渗透）\n\n"
            "请选择你的作案路线。"
        )
        self.story_label.config(text=text)
        btn_foot = tk.Button(self.main_frame, text="徒步接近", font=("Arial", 14), command=self.approach_on_foot)
        btn_land = tk.Button(self.main_frame, text="陆地载具", font=("Arial", 14), command=self.approach_by_land)
        btn_roof = tk.Button(self.main_frame, text="空中载具", font=("Arial", 14), command=self.approach_from_roof)
        btn_foot.pack(pady=5)
        btn_land.pack(pady=5)
        btn_roof.pack(pady=5)
        self.active_widgets.extend([btn_foot, btn_land, btn_roof])
        self.add_log("选择作案方式。")
        self.update_status()

    # 徒步接近分支
    def approach_on_foot(self):
        self.current_stage = "approach_on_foot"
        self.clear_active_widgets()
        text = (
            "你选择徒步接近银行。\n\n"
            "在接近过程中，你可以选择：\n"
            "1. 从正门进入（需穿戴 Camouflage Suit，否则可能触发警报）\n"
            "2. 从侧门进入（需要 Hacking Tool，否则警报会响起）\n\n"
            "请选择进入方式。"
        )
        self.story_label.config(text=text)
        btn_main = tk.Button(self.main_frame, text="正门进入", font=("Arial", 14), command=self.main_entrance_route)
        btn_side = tk.Button(self.main_frame, text="侧门进入", font=("Arial", 14), command=self.side_door_route)
        btn_main.pack(pady=5)
        btn_side.pack(pady=5)
        self.active_widgets.extend([btn_main, btn_side])
        self.add_log("徒步接近分支。")
        self.update_status()

    # 陆地载具分支
    def approach_by_land(self):
        self.current_stage = "approach_by_land"
        self.clear_active_widgets()
        text = (
            "你选择使用陆地载具（如抢车）接近银行。\n\n"
            "你驾车冲向银行门口，但必然会触发警报。\n"
            "请准备迎接守卫的交火。"
        )
        self.story_label.config(text=text)
        btn_enter = tk.Button(self.main_frame, text="撞开银行门", font=("Arial", 14), command=self.land_entry_route)
        btn_enter.pack(pady=5)
        self.active_widgets.append(btn_enter)
        self.add_log("陆地载具分支。")
        self.update_status()

    # 空中载具分支
    def approach_from_roof(self):
        self.current_stage = "approach_from_roof"
        self.clear_active_widgets()
        text = (
            "你选择使用空中载具（直升机）从屋顶进入银行。\n\n"
            "在屋顶，你可以选择：\n"
            "1. 寻找持有金库钥匙的守卫\n"
            "2. 直接设置 Thermite 爆破金库门\n\n"
            "请选择你的行动。"
        )
        self.story_label.config(text=text)
        btn_search = tk.Button(self.main_frame, text="寻找守卫", font=("Arial", 14), command=self.roof_search_guard)
        btn_direct = tk.Button(self.main_frame, text="直接爆破", font=("Arial", 14), command=self.roof_direct_vault)
        btn_search.pack(pady=5)
        btn_direct.pack(pady=5)
        self.active_widgets.extend([btn_search, btn_direct])
        self.add_log("空中载具分支。")
        self.update_status()

    # --------------------------
    # 进入银行的各分支处理
    # --------------------------
    def main_entrance_route(self):
        self.current_stage = "main_entrance"
        self.clear_active_widgets()
        text = "你从正门进入银行……\n\n"
        if "Camouflage Suit" in self.inventory:
            if random.random() < 0.15:
                text += "即便如此，一名警卫发现了你！"
                self.alarm_triggered = True
                self.start_combat("正门警卫", 30, 10, "bullet", self.after_main_entrance_combat)
            else:
                text += "你成功混入人群，顺利进入大堂。"
                self.story_label.config(text=text)
                self.after_main_entrance_combat()
        else:
            text += "你未装备隐蔽服，果然被警卫发现！"
            self.alarm_triggered = True
            self.start_combat("正门警卫", 30, 10, "bullet", self.after_main_entrance_combat)
        self.story_label.config(text=text)
        self.add_log("正门进入分支启动。")
        self.update_status()

    def after_main_entrance_combat(self):
        self.clear_active_widgets()
        text = (
            "正门交火后，你获得了一把枪，但警报已响。\n\n"
            "你必须迅速寻找持有金库钥匙的守卫。\n"
            "请选择：\n"
            "1. 暗杀守卫（需要近战武器，例如 Knife）\n"
            "2. 直接交火（使用枪械）"
        )
        self.story_label.config(text=text)
        btn_assassinate = tk.Button(self.main_frame, text="暗杀守卫", font=("Arial", 14),
                                    command=self.assassinate_guard)
        btn_shoot = tk.Button(self.main_frame, text="直接交火", font=("Arial", 14), command=self.shoot_guard)
        btn_assassinate.pack(pady=5)
        btn_shoot.pack(pady=5)
        self.active_widgets.extend([btn_assassinate, btn_shoot])
        self.add_log("正门进入后选择获取钥匙方式。")
        self.update_status()

    def assassinate_guard(self):
        self.current_stage = "assassinate_guard"
        self.clear_active_widgets()
        text = "你选择悄悄靠近，利用近战武器暗杀持钥匙的守卫。"
        self.story_label.config(text=text)
        if "Knife" in self.inventory:
            self.have_vault_key = True
            text += "\n守卫被你无声暗杀，金库钥匙到手！"
            self.story_label.config(text=text)
            self.after_key_obtained()
        else:
            self.add_log("暗杀失败，缺乏近战武器！")
            self.alarm_triggered = True
            self.start_combat("持钥匙守卫", 40, 15, "bullet", self.after_guard_combat)
        self.update_status()

    def shoot_guard(self):
        self.current_stage = "shoot_guard"
        self.clear_active_widgets()
        text = "你选择使用枪械直接射击持钥匙的守卫！"
        self.story_label.config(text=text)
        self.alarm_triggered = True
        self.start_combat("持钥匙守卫", 40, 15, "bullet", self.after_guard_combat)
        self.update_status()

    def after_guard_combat(self):
        self.clear_active_widgets()
        self.have_vault_key = True
        text = "守卫被击败，你成功获得了金库钥匙。"
        self.story_label.config(text=text)
        self.after_key_obtained()
        self.add_log("持钥匙守卫处理完毕。")
        self.update_status()

    def side_door_route(self):
        self.current_stage = "side_door"
        self.clear_active_widgets()
        text = "你选择从侧门进入银行。\n\n"
        if "Hacking Tool" in self.inventory:
            if random.random() < 0.1:
                text += "即使使用黑客工具，系统故障导致你被发现！"
                self.alarm_triggered = True
                self.start_combat("侧门警卫", 30, 10, "bullet", self.after_side_door_combat)
            else:
                text += "你利用黑客工具成功破解侧门安防，悄然进入银行。"
                self.story_label.config(text=text)
                self.after_side_door_combat()
        else:
            text += "你未装备黑客工具，强行撬门触发警报！"
            self.alarm_triggered = True
            self.start_combat("侧门警卫", 30, 10, "bullet", self.after_side_door_combat)
        self.story_label.config(text=text)
        self.add_log("侧门进入分支。")
        self.update_status()

    def after_side_door_combat(self):
        self.clear_active_widgets()
        text = (
            "侧门交火后，你迅速潜入内部，发现一名守卫正持有金库钥匙。\n"
            "请选择：\n"
            "1. 暗杀该守卫\n"
            "2. 直接交火"
        )
        self.story_label.config(text=text)
        btn_assassinate = tk.Button(self.main_frame, text="暗杀守卫", font=("Arial", 14),
                                    command=self.assassinate_guard)
        btn_shoot = tk.Button(self.main_frame, text="直接交火", font=("Arial", 14), command=self.shoot_guard)
        btn_assassinate.pack(pady=5)
        btn_shoot.pack(pady=5)
        self.active_widgets.extend([btn_assassinate, btn_shoot])
        self.add_log("侧门进入后选择获取钥匙方式。")
        self.update_status()

    def land_entry_route(self):
        self.current_stage = "land_entry"
        self.clear_active_widgets()
        text = "你驾车直冲银行门口，车子撞开大门！\n警报立刻响起，迎面而来的守卫让你不得不迎战。"
        self.story_label.config(text=text)
        self.alarm_triggered = True
        self.start_combat("迎面守卫", 30, 10, "bullet", self.after_land_entry_combat)
        self.add_log("陆地载具进入分支启动。")
        self.update_status()

    def after_land_entry_combat(self):
        self.clear_active_widgets()
        text = (
            "撞门交火后，你得知持有金库钥匙的守卫正待在前厅。\n"
            "请选择：\n"
            "1. 前往击杀该守卫\n"
            "2. 利用混乱直接进入金库（风险较高）"
        )
        self.story_label.config(text=text)
        btn_fight = tk.Button(self.main_frame, text="击杀守卫", font=("Arial", 14), command=self.shoot_guard)
        btn_bypass = tk.Button(self.main_frame, text="直接进入", font=("Arial", 14), command=self.bypass_guard)
        btn_fight.pack(pady=5)
        btn_bypass.pack(pady=5)
        self.active_widgets.extend([btn_fight, btn_bypass])
        self.add_log("陆地进入后选择获取钥匙方式。")
        self.update_status()

    def bypass_guard(self):
        self.current_stage = "bypass_guard"
        self.clear_active_widgets()
        text = "你选择利用现场混乱直接冲向金库门，放弃获取钥匙。这会增加金库抢劫难度。"
        self.story_label.config(text=text)
        self.have_vault_key = False
        btn_continue = tk.Button(self.main_frame, text="继续前往金库", font=("Arial", 14), command=self.vault_phase)
        btn_continue.pack(pady=5)
        self.active_widgets.append(btn_continue)
        self.add_log("选择直接进入金库，不获取钥匙。")
        self.update_status()

    def roof_search_guard(self):
        self.current_stage = "roof_search"
        self.clear_active_widgets()
        text = (
            "你从屋顶潜下楼梯，悄悄进入银行。\n"
            "你发现一名守卫正持有金库钥匙。\n"
            "请选择：\n"
            "1. 暗杀守卫（需 Knife）\n"
            "2. 直接交火"
        )
        self.story_label.config(text=text)
        btn_assassinate = tk.Button(self.main_frame, text="暗杀守卫", font=("Arial", 14),
                                    command=self.assassinate_guard)
        btn_shoot = tk.Button(self.main_frame, text="直接交火", font=("Arial", 14), command=self.shoot_guard)
        btn_assassinate.pack(pady=5)
        btn_shoot.pack(pady=5)
        self.active_widgets.extend([btn_assassinate, btn_shoot])
        self.add_log("屋顶进入分支：选择获取钥匙方式。")
        self.update_status()

    def roof_direct_vault(self):
        self.current_stage = "roof_direct"
        self.clear_active_widgets()
        text = "你决定不与守卫纠缠，直接在屋顶设置 Thermite 爆破金库门。警报必定响起！"
        self.story_label.config(text=text)
        self.alarm_triggered = True
        btn_explode = tk.Button(self.main_frame, text="引爆 Thermite", font=("Arial", 14), command=self.vault_phase)
        btn_explode.pack(pady=5)
        self.active_widgets.append(btn_explode)
        self.add_log("选择直接爆破金库门（屋顶方式）。")
        self.update_status()

    def after_key_obtained(self):
        self.clear_active_widgets()
        text = (
            "持钥匙阶段结束！\n"
            "你已成功获取金库钥匙，现在前往金库阶段。\n\n"
            "请选择是否在前往金库前再进行一次分支选择：\n"
            "1. 等待一会儿，观察银行内部动向（可能降低警报强度）\n"
            "2. 立即进入金库（速度至关重要）"
        )
        self.story_label.config(text=text)
        btn_wait = tk.Button(self.main_frame, text="观察等待", font=("Arial", 14), command=self.wait_before_vault)
        btn_now = tk.Button(self.main_frame, text="立即进入", font=("Arial", 14), command=self.vault_phase)
        btn_wait.pack(pady=5)
        btn_now.pack(pady=5)
        self.active_widgets.extend([btn_wait, btn_now])
        self.add_log("选择是否等待观察银行内部情况。")
        self.update_status()

    def wait_before_vault(self):
        self.current_stage = "wait_before_vault"
        self.clear_active_widgets()
        text = "你决定等待一会儿，观察银行内部动向……\n稍后你发现警报强度似乎有所下降。"
        self.story_label.config(text=text)
        self.alarm_triggered = False  # 观察后警报减弱
        btn_continue = tk.Button(self.main_frame, text="前往金库", font=("Arial", 14), command=self.vault_phase)
        btn_continue.pack(pady=5)
        self.active_widgets.append(btn_continue)
        self.add_log("等待观察后进入金库阶段。")
        self.update_status()

    # --------------------------
    # 金库抢劫阶段
    # --------------------------
    def vault_phase(self):
        self.current_stage = "vault_phase"
        self.clear_active_widgets()
        if self.have_vault_key:
            text = "你使用金库钥匙解锁金库门，门缓缓开启，堆满现金！\n" \
                   "但警报声依然震耳欲聋，你必须迅速抢劫并撤离！"
        else:
            text = "金库门在爆炸声中被炸开，火光闪烁，但你知道里面有大量现金！\n" \
                   "时间紧迫，请立即开始抢劫！"
        self.story_label.config(text=text)
        btn_loot = tk.Button(self.main_frame, text="进入金库抢劫", font=("Arial", 14), command=self.vault_looting_game)
        btn_loot.pack(pady=10)
        self.active_widgets.append(btn_loot)
        self.add_log("进入金库抢劫阶段。")
        self.update_status()

    def vault_looting_game(self):
        self.current_stage = "vault_looting"
        self.clear_active_widgets()
        self.loot_time = 30 if self.alarm_triggered else 60
        self.loot_clicks = 0
        self.money_looted = 0
        text = f"抢劫开始！你有 {self.loot_time} 秒时间抢夺金钱，每次点击获得 $1000，最高可达 $100000。"
        self.story_label.config(text=text)
        self.timer_label = tk.Label(self.main_frame, text=f"剩余时间: {self.loot_time} 秒", font=("Arial", 14))
        self.timer_label.pack(pady=5)
        self.loot_label = tk.Label(self.main_frame, text="已抢金额: $0", font=("Arial", 14))
        self.loot_label.pack(pady=5)
        self.loot_button = tk.Button(self.main_frame, text="抢钱！", font=("Arial", 16), command=self.grab_money)
        self.loot_button.pack(pady=10)
        self.active_widgets.extend([self.timer_label, self.loot_label, self.loot_button])
        self.add_log("金库抢劫迷你游戏开始。")
        self.update_status()
        self.countdown_loot()

    def grab_money(self):
        if self.loot_clicks * 1000 < 100000:
            self.loot_clicks += 1
            amount = self.loot_clicks * 1000
            if amount > 100000:
                amount = 100000
            self.loot_label.config(text=f"已抢金额: ${amount}")
        else:
            self.loot_button.config(state="disabled")

    def countdown_loot(self):
        if self.loot_time > 0:
            self.loot_time -= 1
            self.timer_label.config(text=f"剩余时间: {self.loot_time} 秒")
            if self.loot_time == 15:
                play_sound("sound/jinku.mp3")
            self.root.after(1000, self.countdown_loot)
        else:
            self.loot_button.config(state="disabled")
            self.money_looted = min(self.loot_clicks * 1000, 100000)
            self.player_money += self.money_looted
            self.add_log(f"抢劫结束，抢得 ${self.money_looted}。")
            self.after_loot_phase()

    # --------------------------
    # 撤退阶段
    # --------------------------
    def after_loot_phase(self):
        self.current_stage = "pre_escape"
        self.clear_active_widgets()
        text = (
            "金库抢劫结束，但你仍未脱身！\n\n"
            "撤退阶段：请选择你的撤退路线：\n"
            "1. 后门撤退（可能遭遇敌人追击，选择交火或躲避）\n"
            "2. 下水道逃离（环境复杂，敌人较少）\n"
            "3. 直接冲出大堂（速度快但风险极高）"
        )
        self.story_label.config(text=text)
        btn_backdoor = tk.Button(self.main_frame, text="后门撤退", font=("Arial", 14), command=self.escape_backdoor)
        btn_sewer = tk.Button(self.main_frame, text="下水道逃离", font=("Arial", 14), command=self.escape_sewers)
        btn_direct = tk.Button(self.main_frame, text="直接冲出", font=("Arial", 14), command=self.escape_direct)
        btn_backdoor.pack(pady=5)
        btn_sewer.pack(pady=5)
        btn_direct.pack(pady=5)
        self.active_widgets.extend([btn_backdoor, btn_sewer, btn_direct])
        self.add_log("进入撤退阶段。")
        self.update_status()

    def escape_backdoor(self):
        self.current_stage = "escape_backdoor"
        self.clear_active_widgets()
        text = (
            "你选择从后门撤退。\n\n"
            "在后门出口，你遭遇了追击的敌人！请选择：\n"
            "1. 与敌人交火\n"
            "2. 激活同伙技能获得支援"
        )
        self.story_label.config(text=text)
        btn_fight = tk.Button(self.main_frame, text="交火", font=("Arial", 14), command=self.combat_escape)
        btn_assist = tk.Button(self.main_frame, text="激活同伙技能", font=("Arial", 14),
                               command=self.activate_associate_skill)
        btn_fight.pack(pady=5)
        btn_assist.pack(pady=5)
        self.active_widgets.extend([btn_fight, btn_assist])
        self.add_log("后门撤退分支启动。")
        self.update_status()

    def escape_sewers(self):
        self.current_stage = "escape_sewers"
        self.clear_active_widgets()
        text = (
            "你选择通过下水道逃离银行。\n\n"
            "下水道黑暗且曲折，途中可能遇到突发情况。\n"
            "请选择：\n"
            "1. 快速奔跑\n"
            "2. 小心潜行"
        )
        self.story_label.config(text=text)
        btn_run = tk.Button(self.main_frame, text="快速奔跑", font=("Arial", 14), command=self.sewer_run)
        btn_stealth = tk.Button(self.main_frame, text="小心潜行", font=("Arial", 14), command=self.sewer_stealth)
        btn_run.pack(pady=5)
        btn_stealth.pack(pady=5)
        self.active_widgets.extend([btn_run, btn_stealth])
        self.add_log("下水道撤退分支启动。")
        self.update_status()

    def escape_direct(self):
        self.current_stage = "escape_direct"
        self.clear_active_widgets()
        text = "你选择直接冲出大堂，但迎面而来的警察和保安让你不得不进行激烈交火！"
        self.story_label.config(text=text)
        self.start_combat("警察与保安", 50, 20, "bullet", self.after_escape_combat)
        self.add_log("直接冲出撤退分支启动。")
        self.update_status()

    def combat_escape(self):
        self.current_stage = "combat_escape"
        self.clear_active_widgets()
        text = "你与追击的敌人展开激烈交火！"
        self.story_label.config(text=text)
        self.start_combat("追击敌人", 40, 15, "bullet", self.after_escape_combat)
        self.add_log("撤退交火分支启动。")
        self.update_status()

    def sewer_run(self):
        self.current_stage = "sewer_run"
        self.clear_active_widgets()
        text = "你选择快速奔跑，虽然风险较高，但速度能大大提高成功率！"
        self.story_label.config(text=text)
        if random.random() < 0.3:
            self.add_log("下水道遇到突发状况，遭遇敌人！")
            self.start_combat("下水道敌人", 30, 10, "bullet", self.after_escape_combat)
        else:
            self.after_escape_combat()
        self.update_status()

    def sewer_stealth(self):
        self.current_stage = "sewer_stealth"
        self.clear_active_widgets()
        text = "你选择小心潜行，成功避开了下水道的所有危险，顺利逃离！"
        self.story_label.config(text=text)
        self.after_escape_combat()
        self.update_status()

    def after_escape_combat(self):
        self.clear_active_widgets()
        text = (
            "经过一番激战，你成功脱离险境，安全到达撤退地点。\n"
            "恭喜你完成这次高风险的银行抢劫！\n"
            f"抢劫金额：${self.money_looted}，最终资产：${self.player_money}"
        )
        self.story_label.config(text=text)
        btn_restart = tk.Button(self.main_frame, text="重新开始", font=("Arial", 14), command=self.reset_game)
        btn_quit = tk.Button(self.main_frame, text="退出游戏", font=("Arial", 14), command=self.root.destroy)
        btn_restart.pack(pady=5)
        btn_quit.pack(pady=5)
        self.active_widgets.extend([btn_restart, btn_quit])
        self.add_log("撤退阶段结束，任务完成。")
        self.update_status()

    # --------------------------
    # 战斗系统：掷骰子交火
    # --------------------------
    def start_combat(self, enemy_name, enemy_hp, enemy_damage, enemy_weapon, on_win_callback):
        self.current_stage = "combat"
        self.clear_active_widgets()
        self.enemy_name = enemy_name
        self.enemy_hp = enemy_hp
        self.enemy_damage = enemy_damage
        self.enemy_weapon = enemy_weapon
        self.combat_on_win = on_win_callback
        text = f"战斗开始！你正在与 {enemy_name} 交战！"
        self.story_label.config(text=text)
        self.combat_status_label = tk.Label(self.main_frame, text=f"{enemy_name} HP: {enemy_hp}", font=("Arial", 14))
        self.combat_status_label.pack(pady=5)
        self.combat_attack_btn = tk.Button(self.main_frame, text="掷骰子攻击", font=("Arial", 14),
                                           command=self.roll_dice_combat)
        self.combat_attack_btn.pack(pady=5)
        self.active_widgets.extend([self.combat_status_label, self.combat_attack_btn])
        if self.associates:
            self.associate_btn = tk.Button(self.main_frame, text="激活同伙技能", font=("Arial", 14),
                                           command=self.activate_associate_skill)
            self.associate_btn.pack(pady=5)
            self.active_widgets.append(self.associate_btn)
        self.add_log(f"进入战斗：{enemy_name}。")
        self.update_status()

    def roll_dice_combat(self):
        player_bonus = 0
        if "Heavy Firepower" in self.inventory:
            player_bonus += 1
        if "Getaway Vehicle" in self.inventory:
            player_bonus += 1
        player_roll = random.randint(1, 6) + player_bonus
        enemy_roll = random.randint(1, 6)
        result = ""
        if player_roll == enemy_roll:
            result = f"双方均掷出 {player_roll} 点，平手，未造成伤害。"
        elif player_roll > enemy_roll:
            damage = 15
            if "Heavy Firepower" in self.inventory:
                damage = 30
            elif "Getaway Vehicle" in self.inventory:
                damage = 25
            self.enemy_hp -= damage
            result = f"你掷出 {player_roll} 点，敌人掷出 {enemy_roll} 点，你造成 {damage} 点伤害。"
        else:
            damage = self.enemy_damage
            if self.player_armor > 0:
                if self.player_armor >= damage:
                    self.player_armor -= damage
                    damage = 0
                else:
                    damage -= self.player_armor
                    self.player_armor = 0
            self.player_hp -= damage
            result = f"你掷出 {player_roll} 点，敌人掷出 {enemy_roll} 点，敌人造成 {damage} 点伤害。"
        self.add_log(result)
        self.combat_status_label.config(text=f"{self.enemy_name} HP: {self.enemy_hp}")
        self.update_status()
        if self.enemy_hp <= 0:
            self.add_log(f"{self.enemy_name} 被击败！")
            self.clear_active_widgets()
            if self.combat_on_win:
                self.combat_on_win()
        elif self.player_hp <= 0:
            self.game_over()

    def activate_associate_skill(self):
        if not self.associates:
            self.add_log("没有可用的同伙。")
            return
        for assoc in self.associates.values():
            if not assoc.used:
                self.add_log(f"激活同伙 {assoc.name} 的技能！")
                assoc.activate_skill(self)
                break
        else:
            self.add_log("所有同伙技能均已使用。")
        self.update_status()

    # --------------------------
    # 同伙技能实现
    # --------------------------
    def skill_fool(self, game):
        game.enemy_hp -= 10
        game.add_log("Fool 技能：对敌人造成 10 点伤害。")
        if random.random() < 0.1:
            game.player_hp -= 10
            game.add_log("Fool 反伤：你受到 10 点伤害！")
        game.update_status()

    def skill_retired_military(self, game):
        game.enemy_hp -= 5
        game.add_log("Retired Military 技能：范围伤害，对敌人造成 5 点伤害。")
        game.update_status()

    def skill_robot_manufacturer(self, game):
        game.add_log("Robot Manufacturer 技能：接下来 3 回合内，你受到的伤害减少 50%。")
        game.robot_shield_turns = 3
        game.update_status()

    def skill_teacher(self, game):
        game.add_log("Teacher 技能：激活复活几率，若下一次死亡有 50% 机会复活，同时敌人伤害可能减半。")
        game.teacher_effect = True
        game.update_status()

    def skill_sam(self, game):
        game.player_hp *= 2
        game.player_max_hp *= 2
        game.add_log("SAM 技能：玩家血量翻倍，伤害提升！")
        game.update_status()

    # --------------------------
    # 游戏结束与重启
    # --------------------------
    def game_over(self):
        self.current_stage = "game_over"
        self.clear_active_widgets()
        text = "你已阵亡！\n\n"
        if self.player_money >= 1000:
            text += "你可以选择花费 $1000 贿赂守卫复活。"
            btn_bribe = tk.Button(self.main_frame, text="贿赂复活", font=("Arial", 14),
                                  command=lambda: self.bribe_revive(1000))
            btn_bribe.pack(pady=5)
            self.active_widgets.append(btn_bribe)
        text += "\n或选择重新开始游戏。"
        self.story_label.config(text=text)
        btn_restart = tk.Button(self.main_frame, text="重新开始", font=("Arial", 14), command=self.reset_game)
        btn_quit = tk.Button(self.main_frame, text="退出游戏", font=("Arial", 14), command=self.root.destroy)
        btn_restart.pack(pady=5)
        btn_quit.pack(pady=5)
        self.active_widgets.extend([btn_restart, btn_quit])
        self.add_log("游戏结束。")
        self.update_status()

    def bribe_revive(self, cost):
        if self.player_money >= cost:
            self.player_money -= cost
            self.player_hp = self.player_max_hp
            self.add_log("贿赂成功，获得复活。")
            self.clear_active_widgets()
            self.after_escape_combat()
        else:
            self.add_log("资金不足，无法贿赂。")
        self.update_status()

    def reset_game(self):
        self.current_stage = "intro"
        self.clear_active_widgets()
        self.player_hp = 100
        self.player_max_hp = 100
        self.player_armor = 100
        self.player_max_armor = 100
        self.player_money = self.initial_money
        self.inventory = []
        self.offsite_team = []
        self.associates = {}
        self.alarm_triggered = False
        self.have_vault_key = False
        self.loot_clicks = 0
        self.money_looted = 0
        self.log_messages = []
        self.add_log("游戏重置。")
        self.update_status()
        self.show_intro()

    def save_game(self):
        if not self.can_save:
            self.add_log("当前阶段无法存档。")
            return
        data = {
            "current_stage": self.current_stage,
            "player_hp": self.player_hp,
            "player_max_hp": self.player_max_hp,
            "player_armor": self.player_armor,
            "player_max_armor": self.player_max_armor,
            "player_money": self.player_money,
            "inventory": self.inventory,
            "offsite_team": self.offsite_team,
            "associates": list(self.associates.keys()),
            "alarm_triggered": self.alarm_triggered,
            "have_vault_key": self.have_vault_key,
            "loot_clicks": self.loot_clicks,
            "money_looted": self.money_looted,
            "log_messages": self.log_messages
        }
        try:
            with open("savegame.json", "w") as f:
                json.dump(data, f)
            self.add_log("存档成功。")
        except Exception as e:
            self.add_log(f"存档失败: {e}")
        self.update_status()

    def load_game(self):
        try:
            with open("savegame.json", "r") as f:
                data = json.load(f)
        except Exception as e:
            self.add_log(f"加载存档失败: {e}")
            return
        self.current_stage = data.get("current_stage", "intro")
        self.player_hp = data.get("player_hp", 100)
        self.player_max_hp = data.get("player_max_hp", 100)
        self.player_armor = data.get("player_armor", 100)
        self.player_max_armor = data.get("player_max_armor", 100)
        self.player_money = data.get("player_money", self.initial_money)
        self.inventory = data.get("inventory", [])
        self.offsite_team = data.get("offsite_team", [])
        associates_list = data.get("associates", [])
        self.associates = {}
        self.alarm_triggered = data.get("alarm_triggered", False)
        self.have_vault_key = data.get("have_vault_key", False)
        self.loot_clicks = data.get("loot_clicks", 0)
        self.money_looted = data.get("money_looted", 0)
        self.log_messages = data.get("log_messages", [])
        self.add_log("加载存档成功。")
        self.update_status()
        if self.current_stage == "intro":
            self.show_intro()
        elif self.current_stage == "equipment_shop":
            self.show_equipment_shop()
        elif self.current_stage in ["personnel_recruitment", "offsite_recruitment", "associates_recruitment"]:
            self.show_personnel_recruitment()
        elif self.current_stage == "approach_selection":
            self.show_approach_selection()
        elif self.current_stage in ["main_entrance", "side_door", "land_entry", "approach_from_roof"]:
            self.show_approach_selection()
        elif self.current_stage in ["vault_phase", "vault_looting"]:
            self.vault_phase()
        elif self.current_stage in ["pre_escape", "escape_backdoor", "escape_sewers", "escape_direct"]:
            self.after_loot_phase()
        else:
            self.show_intro()

    def run_all_extensions(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    game = BankRobberyGame(root)
    game.run_all_extensions()
    root.mainloop()
