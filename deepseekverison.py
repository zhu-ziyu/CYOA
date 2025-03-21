import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import winsound
import json
from math import ceil
from PIL import ImageTk, Image


# ========================
# 游戏核心逻辑类
# ========================
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        # 玩家属性
        self.hp = 100
        self.armor = 100
        self.money = 10000
        self.mental_state = "正常"

        # 装备系统
        self.equipment = {
            'decoy_crew': False,
            'getaway_vehicle': None,  # land/air
            'backpack': False,
            'thermite': False,
            'camouflage': False,
            'heavy_weapon': False
        }

        # 雇佣系统
        self.hired = {
            'hacker': False,
            'security': False,
            'equipment_vendor': False
        }

        # 队友系统
        self.allies = {
            'fool': False,  # 10%分成
            'soldier': False,  # 30%分成
            'robot': False,  # 70%分成
            'teacher': False,  # 彩蛋角色
            'sam': False  # 测试角色
        }

        # 游戏进程
        self.current_stage = "preparation"
        self.entry_method = None  # 进入方式
        self.vault_opened = False
        self.escape_route = None
        self.guard_key = False
        self.vault_money = 0

        # 战斗状态
        self.in_combat = False
        self.enemy_hp = 0
        self.enemy_damage = 0

    def save_game(self):
        with open('save.json', 'w') as f:
            json.dump(self.__dict__, f)

    def load_game(self):
        try:
            with open('save.json', 'r') as f:
                data = json.load(f)
                self.__dict__.update(data)
                return True
        except:
            return False


# ========================
# 游戏GUI主类
# ========================
class HeistGame:
    def __init__(self, root):
        self.root = root
        self.root.title("RMC银行大劫案")
        self.root.geometry("1000x750")

        # 加载图片
        self.load_images()

        # 初始化游戏状态
        self.state = GameState()

        # 创建界面
        self.create_widgets()
        self.show_main_menu()

    def load_images(self):
        try:
            self.camouflage_img = ImageTk.PhotoImage(Image.open("image/gun.png").resize((64, 64)))
            self.thermite_img = ImageTk.PhotoImage(Image.open("image/gun.png").resize((64, 64)))
            self.hacker_img = ImageTk.PhotoImage(Image.open("image/gun.png").resize((64, 64)))
        except Exception as e:
            messagebox.showerror("资源错误", f"无法加载图片资源: {str(e)}")
            self.root.destroy()

    def create_widgets(self):
        # 主框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 状态栏
        self.status_bar = tk.Frame(self.root, bg="#333", height=30)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = tk.Label(self.status_bar, text=self.get_status_text(),
                                     fg="white", bg="#333", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=10)

    def get_status_text(self):
        return f"资金: ${self.state.money} | HP: {self.state.hp} | 护甲: {self.state.armor} | 当前阶段: {self.state.current_stage}"

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def update_status(self):
        self.status_label.config(text=self.get_status_text())

    # ========================
    # 主菜单系统
    # ========================
    def show_main_menu(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="=== RMC银行大劫案 ===",
                 font=("Arial", 24, "bold")).pack(pady=30)

        menu_options = [
            ("新游戏", self.start_new_game),
            ("加载游戏", self.load_game),
            ("退出游戏", self.root.quit)
        ]

        for text, cmd in menu_options:
            btn = tk.Button(self.main_frame, text=text, command=cmd,
                            width=20, font=("Arial", 14))
            btn.pack(pady=10)

    def start_new_game(self):
        self.state.reset()
        self.show_preparation()

    def load_game(self):
        if self.state.load_game():
            self.show_current_stage()
        else:
            messagebox.showerror("错误", "加载存档失败")

    # ========================
    # 准备阶段
    # ========================
    def show_preparation(self):
        self.clear_frame()
        self.state.current_stage = "preparation"

        tk.Label(self.main_frame, text="=== 准备阶段 ===",
                 font=("Arial", 18)).pack(pady=10)

        options = [
            ("购买装备", self.show_equipment_store),
            ("雇佣人员", self.show_hiring_menu),
            ("招募队友", self.show_allies_menu),
            ("开始行动", self.start_action_phase)
        ]

        for text, cmd in options:
            btn = tk.Button(self.main_frame, text=text, command=cmd,
                            width=25, font=("Arial", 12))
            btn.pack(pady=8)

    def show_equipment_store(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="=== 装备商店 ===", font=("Arial", 16)).pack(pady=10)

        # 装备列表
        equipment_list = [
            {
                "name": "伪装服装",
                "price": 5000,
                "image": self.camouflage_img,
                "key": "camouflage",
                "desc": "解锁潜行路线，避免早期战斗"
            },
            {
                "name": "铝热剂",
                "price": 3000,
                "image": self.thermite_img,
                "key": "thermite",
                "desc": "开启新的逃脱方式"
            },
            # 其他装备...
        ]

        for item in equipment_list:
            frame = tk.Frame(self.main_frame)
            frame.pack(fill=tk.X, pady=5)

            tk.Label(frame, image=item["image"]).pack(side=tk.LEFT)
            tk.Label(frame, text=f"{item['name']} - ${item['price']}\n{item['desc']}",
                     justify=tk.LEFT).pack(side=tk.LEFT, padx=10)

            btn = tk.Button(frame, text="购买",
                            command=lambda i=item: self.purchase_equipment(i),
                            state=tk.NORMAL if self.state.money >= i["price"] else tk.DISABLED)
            btn.pack(side=tk.RIGHT)

        tk.Button(self.main_frame, text="返回", command=self.show_preparation,
                  font=("Arial", 12)).pack(pady=20)

    def purchase_equipment(self, item):
        if self.state.money >= item["price"]:
            self.state.money -= item["price"]
            self.state.equipment[item["key"]] = True
            self.update_status()
            messagebox.showinfo("购买成功", f"已购买 {item['name']}!")
            self.show_equipment_store()
        else:
            messagebox.showerror("资金不足", "你的资金不够购买此物品")

    # ========================
    # 行动阶段
    # ========================
    def start_action_phase(self):
        self.clear_frame()
        self.state.current_stage = "action"

        options = []

        # 根据装备生成选项
        if self.state.equipment["camouflage"]:
            options.append(("潜行路线（主入口）", self.stealth_approach))
        if self.state.hired["hacker"]:
            options.append(("侧门渗透（需要黑客）", self.side_door_approach))
        if self.state.equipment["heavy_weapon"]:
            options.append(("正面强攻（重武器）", self.assault_approach))
        if self.state.equipment["getaway_vehicle"] == "air":
            options.append(("屋顶空降（直升机）", self.rooftop_approach))

        # 显示行动选项
        tk.Label(self.main_frame, text="=== 选择行动路线 ===",
                 font=("Arial", 16)).pack(pady=10)

        for text, cmd in options:
            btn = tk.Button(self.main_frame, text=text, command=cmd,
                            width=30, font=("Arial", 12))
            btn.pack(pady=5)

        tk.Button(self.main_frame, text="返回准备阶段",
                  command=self.show_preparation).pack(pady=10)

    def stealth_approach(self):
        # 潜行路线逻辑
        self.clear_frame()
        self.state.entry_method = "stealth"

        if random.random() < 0.3 and not self.state.hired["security"]:
            self.trigger_random_event("警卫发现了你！")
            self.start_combat("普通警卫", 50, 10)
        else:
            self.show_vault_access()

    def side_door_approach(self):
        # 侧门渗透逻辑
        if not self.state.hired["hacker"]:
            messagebox.showinfo("失败", "需要雇佣黑客才能执行此路线！")
            return

        # 黑客小游戏
        success = self.hacking_minigame()
        if success:
            self.show_vault_access()
        else:
            self.trigger_alarm()

    def hacking_minigame(self):
        # 实现黑客小游戏
        return random.random() > 0.5

    # ========================
    # 战斗系统
    # ========================
    def start_combat(self, enemy_type, enemy_hp, enemy_damage):
        self.state.in_combat = True
        self.state.enemy_hp = enemy_hp
        self.state.enemy_damage = enemy_damage

        self.clear_frame()
        tk.Label(self.main_frame, text=f"遭遇 {enemy_type}！",
                 font=("Arial", 16)).pack(pady=10)

        # 战斗界面
        self.combat_text = tk.StringVar()
        tk.Label(self.main_frame, textvariable=self.combat_text).pack()

        tk.Button(self.main_frame, text="攻击", command=self.combat_attack).pack()
        if self.state.allies["soldier"]:
            tk.Button(self.main_frame, text="呼叫支援", command=self.call_backup).pack()

        self.update_combat_display()

    def combat_attack(self):
        # 骰子战斗逻辑
        player_roll = random.randint(1, 6)
        enemy_roll = random.randint(1, 6)

        # 装备加成
        if self.state.equipment["heavy_weapon"]:
            player_roll += 2
        if self.state.hired["equipment_vendor"]:
            enemy_roll -= 1

        if player_roll > enemy_roll:
            damage = player_roll * 5
            self.state.enemy_hp -= damage
            self.combat_text.set(f"你造成 {damage} 点伤害！")
        else:
            self.state.hp -= max(self.state.enemy_damage - self.state.armor // 2, 0)
            self.combat_text.set(f"你受到 {self.state.enemy_damage} 点伤害！")

        self.update_status()
        self.update_combat_display()

        if self.state.enemy_hp <= 0:
            self.end_combat(victory=True)
        elif self.state.hp <= 0:
            self.end_combat(victory=False)

    def update_combat_display(self):
        self.combat_text.set(f"{self.combat_text.get()}\n敌人剩余HP: {self.state.enemy_hp}\n你的HP: {self.state.hp}")

    # ========================
    # 金库系统
    # ========================
    def show_vault_access(self):
        self.clear_frame()
        self.state.current_stage = "vault"

        if self.state.hired["hacker"]:
            self.state.vault_time = 60
        else:
            self.state.vault_time = 30

        # 金库小游戏界面
        self.vault_btn = tk.Button(self.main_frame, text="快速点击抢钱！",
                                   command=self.vault_click,
                                   font=("Arial", 18),
                                   bg="gold")
        self.vault_btn.pack(pady=30)

        self.timer_label = tk.Label(self.main_frame,
                                    text=f"剩余时间: {self.state.vault_time}s",
                                    font=("Arial", 14))
        self.timer_label.pack()

        self.vault_start_time = time.time()
        self.update_vault_timer()

    def vault_click(self):
        self.state.vault_money += 1000
        if time.time() - self.vault_start_time > 15:
            winsound.PlaySound("sound/jinku.mp3", winsound.SND_ASYNC)

    def update_vault_timer(self):
        elapsed = time.time() - self.vault_start_time
        remaining = self.state.vault_time - int(elapsed)

        if remaining > 0:
            self.timer_label.config(text=f"剩余时间: {remaining}s")
            self.root.after(1000, self.update_vault_timer)
        else:
            self.end_vault_phase()

    # ========================
    # 游戏启动
    # ========================


if __name__ == "__main__":
    root = tk.Tk()
    game = HeistGame(root)
    root.mainloop()