# 理工科作业路由规则（统一入口）

**唯一 catalog**：`refs/assignment-catalog.yaml` v3 — 含 FPGA、编程、MATLAB/Multisim/Keil 及多数工科 planned 工具。

`simulation-homework-assistant` / `coding-homework-assistant` 仅为别名，**勿**再读各自 theme 的独立 catalog 做路由。

## 数据源

| 文件 | 用途 |
|------|------|
| `assignment-catalog.yaml` | 路由表（机器可读）；**MD-only 读 `assignment-catalog.yaml.md`** |
| `md-compat-index.md` | 全部 YAML/PY 镜像清单 |
| `stem-tool-matrix.md` | ready vs planned 工具一览 |
| `universal-stem-workflow.md` | 无 lab skill 时的通用流程 |
| `board-devices.yaml` / `board-pins/` | Quartus 板卡（quartus-lab handoff） |

## 匹配算法

1. 合并 `major` + `assignment` → 小写文本
2. major → `major_id`：与 `majors[].aliases` 子串匹配（最长优先）
3. 对每条 assignment（**最后**才考虑 `stem-universal-fallback`）：
   - `score = keyword_hits × keyword_weight + (major_id in majors ? major_weight : 0)`
4. 最高分 `< min_score` → Top 3 + 请用户补充
5. 分差 ≤ `tie_threshold` → ASK 确认
6. `status: planned` → **不 install**；走 universal-stem-workflow

## 安装前确认（必做）

```
匹配：{title} (id: {id}, score: {score}, status: {status})
将安装：{skills_to_install 或「无 — 通用工作流」}
目标：{host}/{scope} → {project_dir}
继续？[Y/n]
```

## 路径解析

`install.resolve_order`：

1. registry / `skill list`
2. `examples/{skill}`
3. `skill-forge/built/simulation-lab/{skill}`
4. `skill-forge/built/coding-homework/{skill}`
5. `skill-forge/built/student-homework/{skill}`

## handoff 首问

| skill | 首问 |
|-------|------|
| quartus-lab | 实验任务 + 板卡 |
| python-lab / java-oop-lab / ds-algorithm-lab / ml-notebook-lab | 作业描述 + 环境 |
| matlab-simulink-lab | 实验内容 + MATLAB 版本 |
| multisim-lab | 电路任务 + Multisim 版本 |
| keil-embedded-lab | MCU 型号 + 实验要求 |
| planned | 软件版本 + 指导书 + checklist 逐步 |

## 专业工具无法在 AI 里直接用的对策

见 `stem-tool-matrix.md`：Agent 编辑工程/脚本/报告，GUI 步骤写清单由用户本机执行，禁止伪造运行结果。
