# STEM Homework Skills

面向**理工科学生作业**的 Cursor Agent Skills 套件 v3：**专业 + 作业** → 统一 catalog 打分 → **用户确认** → 自动安装 lab skill 或通用工作流。

| Skill | 作用 |
|-------|------|
| **homework-assistant** | 唯一主入口：路由、确认、install、handoff |
| quartus-lab | 计组 / Quartus FPGA |
| python-lab / java-oop-lab / ds-algorithm-lab / ml-notebook-lab | 编程课设 |
| matlab-simulink-lab / multisim-lab / keil-embedded-lab | 仿真 / 电路 / 嵌入式 |

`simulation-homework-assistant` 与 `coding-homework-assistant` 为别名，统一走 `homework-assistant` catalog。

## 快速开始

```bash
git clone https://github.com/azhimiao/homework.git
cd homework
pip install -r requirements.txt

python skill-core/skill.py install examples/student-homework/homework-assistant --host cursor --scope global
```

Windows 可用 `./skill install examples/student-homework/homework-assistant --host cursor --scope global`。

## 从源码编译

```bash
python skill-core/skill.py batch build student-homework --test
python skill-core/skill.py batch build simulation-lab --test
python skill-core/skill.py batch build coding-homework --test
```

## 关键 refs

| 文件 | 内容 |
|------|------|
| `skill-forge/themes/student-homework/refs/assignment-catalog.yaml` | v3 统一路由表 |
| `refs/stem-tool-matrix.md` | ready / planned 工具矩阵 |
| `refs/universal-stem-workflow.md` | 无 lab skill 时的流程 |
| `refs/board-pins/de10-lite.md` | DE10-Lite 引脚参考 |

## 仓库结构

| 路径 | 说明 |
|------|------|
| `examples/student-homework/` | 入口 + Quartus lab |
| `examples/coding-homework/` | Python / Java / DS / ML lab |
| `examples/simulation-lab/` | MATLAB / Multisim / Keil lab |
| `skill-forge/themes/` | 主题源码 |
| `skill-forge/built/` | 编译输出 |
| `skill-core/` | 编译、测试、安装 CLI |

完整工具链见 [azhimiao/skillforskill](https://github.com/azhimiao/skillforskill)。
