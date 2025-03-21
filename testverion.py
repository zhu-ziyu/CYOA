import tkinter as tk
import json
import random
import threading
import time
import os




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



# 装备购买阶段
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



# 人员招聘阶段（离线支援和同伙招募）
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
