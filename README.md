# RMC Bank Robbery (Choose Your Own Adventure)  
RMC 银行抢劫（选择你自己的冒险游戏）

## 项目简介 / Project Introduction

**中文说明：**  
这是一个文字互动式冒险游戏，玩家可在终端/命令行中进行银行抢劫冒险。你可以购买装备、雇佣同伴，并选择不同路线入侵银行或控制人质，与警方谈判、对抗，或尝试更具创意的逃生方式。项目中还包含多个不同版本的教学代码和功能演示，以满足教学需求。

**English Description:**  
This is a text-based interactive adventure game where players plan and execute a bank heist. You can purchase equipment, recruit allies, and choose different routes to infiltrate the bank or control hostages, negotiate with or fight the police, or attempt various escape scenarios. The repository also includes multiple teaching/demo versions that illustrate different coding requirements.

---

## 目录结构 / Directory Structure

. ├── DLC.py # 扩展 DLC 内容 ├── rmc_bank_robbery.py # 主程序，包含主要抢劫逻辑 ├── teachv1.py / teachv2.py / teachverison.py / techverion.py # 教学版或不同需求的改写版本 ├── test.py / testverion.py # 测试脚本 ├── sound/ │ └── jinku.mp3 # 测试音频文件 ├── vault.png # 金库图片或示意图 └── README.md # 项目说明文档

markdown
复制
编辑

- **DLC.py**:  
  包含 Hostage Control 等扩展剧本，提供更多分支、随机事件和谈判或威胁的功能。

- **rmc_bank_robbery.py**:  
  游戏主程序，含装备商店、同伴招募、金库阶段和逃跑结局等逻辑。

- **teachv1.py / teachv2.py / teachverison.py / techverion.py**:  
  为满足老师不同要求或特殊写法而做的版本，保留注释与功能。

- **test.py / testverion.py**:  
  测试脚本，用于调试或演示游戏部分功能。

- **sound/**:  
  存放音频文件（如 `jinku.mp3`），可在代码中调用（若已恢复对应播放函数）。

- **vault.png**:  
  银行金库图片，可用作游戏介绍或素材。

---

## 主要功能 / Features

1. **装备系统 / Equipment System**  
   - 购买或升级伪装、黑客工具、爆破物品、护甲背心等。  

2. **同伴招募 / Ally Recruitment**  
   - 可招募不同角色（Fool, Retired Military, Robot Manufacturer, 等），每位同伴具有独特技能。  

3. **多重分支 / Multiple Branches**  
   - 可以徒步或驾车冲撞正门、从侧门潜入、空降屋顶甚至进行人质谈判等。  
   - 包含随机事件（摄像头故障、子弹误伤等）和随机获取额外道具或金钱。  

4. **战斗系统 / Combat**  
   - 通过掷骰子比较攻防点数，并结合武器或护甲影响伤害；有不同敌人血量和伤害值设定。  

5. **DLC - 人质控制 / Hostage Control**  
   - 大型剧情分支，包含70+个选择与随机事件，玩家可控制人质，与警方谈判或威胁，同伴可能背叛等高风险高回报玩法。  

---

## 使用方法 / How to Run

1. **克隆或下载项目 / Clone or Download**  
   ```bash
   git clone https://github.com/zhu-ziyu/CYOA.git
   cd CYOA
安装依赖 / Install Dependencies

该项目主要使用 Python 标准库 (random, time 等)，无需额外第三方库。

如果需要恢复音频播放功能，需安装相应模块（如 playsound），并在代码中取消注释相关部分。

运行主程序 / Run the Main Program

bash
复制
编辑
python rmc_bank_robbery.py
按照终端提示输入 yes 或 no 选择，开始游戏。

后续可在命令行中输入对应选项进行分支选择。

DLC（Hostage Control）使用 / Using the DLC

当游戏提示是否进入人质控制或谈判流程，可输入选项如 "Hostage_Control" 进入 DLC。

也可以在 DLC.py 里查看所有相关函数逻辑，并在主程序中插入调用。

贡献 / Contributing
如果你在游戏过程中发现 Bug 或有新的灵感，欢迎在 Issues 区提交或直接发起 Pull Request。

If you encounter any bugs or have new ideas while playing, feel free to open an Issue or submit a Pull Request.

许可证 / License
目前项目未指定开源协议，若需商用或教学使用，请联系仓库所有者（zhu-ziyu）取得许可。

This project does not specify a license yet. For commercial or educational usage, please contact the repository owner (above) for permission.

感谢你的关注与使用，祝你在这场惊险刺激的银行抢劫冒险中玩得愉快！

(English and Chinese descriptions by ChatGPT.)
