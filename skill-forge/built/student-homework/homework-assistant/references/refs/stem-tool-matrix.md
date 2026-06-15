# 理工科工具矩阵

`homework-assistant` 统一路由表。AI **不能替代 GUI 桌面软件**，但可：编辑工程/脚本文件、生成命令行批处理、核对参数与报告、指导你在本机点击操作。

## 状态说明

| status | 含义 |
|--------|------|
| `ready` | 有专用 lab skill，可 `skill install` |
| `planned` | 无专用 skill；走 `universal-stem-workflow.md` + 本表「无 skill 时」列 |

## 已落地（ready）

| 工具 | catalog id | lab skill | 典型专业 |
|------|------------|-----------|----------|
| Intel Quartus | comp-org-quartus | quartus-lab | CS/EE/自动化 |
| Python | python-coursework | python-lab | CS |
| Java | java-oop-coursework | java-oop-lab | CS |
| 数据结构/算法 | ds-algorithm-coursework | ds-algorithm-lab | CS |
| ML/Jupyter | ml-coursework | ml-notebook-lab | CS |
| MATLAB/Simulink | matlab-control-lab | matlab-simulink-lab | EE/自动化/CS |
| Multisim | multisim-circuit-lab | multisim-lab | EE/自动化 |
| Keil MDK | keil-embedded-lab | keil-embedded-lab | EE/自动化/嵌入式 |

## 规划中（planned）— 通用工作流

| 工具 | catalog id | 无 skill 时 Agent 可做 |
|------|------------|------------------------|
| Xilinx Vivado | vivado-fpga-lab | 写 Verilog/VHDL、约束 XDC、Tcl 批编译脚本 |
| LTspice/PSPICE | ltspice-circuit-lab | 写 .asc/.cir 网表、参数扫频说明 |
| Proteus | proteus-embedded-lab | 源码 + 元件清单 + 接线说明 |
| LabVIEW | labview-measurement-lab | 前面板/框图文字规格、VI 检查清单 |
| ANSYS/Abaqus | ansys-fea-lab | 边界条件表、材料参数、结果解读模板 |
| SolidWorks/Creo | solidworks-cad-lab | 零件设计说明、工程图标注清单 |
| AutoCAD | autocad-drafting-lab | 图层/尺寸规范、LISP 或 DXF 片段 |
| Origin | origin-graph-lab | 数据列定义、作图步骤、图注模板 |
| SPSS/Stata | spss-stats-lab | 变量编码表、分析步骤、APA/GB 结果表述 |
| Altium/Cadence | altium-pcb-lab | 原理图网表、BOM、设计规则核对 |
| COMSOL | comsol-multiphysics-lab | 物理场/边界/网格/后处理检查清单 |
| CCS/IAR (TI) | ccs-ti-embedded-lab | 源码、链接脚本、Makefile |

## 路由原则

1. **一条 catalog** — `assignment-catalog.yaml`（勿再分 simulation/coding 子 catalog 做入口）
2. **有 ready skill** → 确认后 install → handoff 到 lab skill
3. **仅 planned** → 不 install；写 checklist + `universal-stem-workflow.md` + 上表对应行
4. **仍无匹配** → `stem-universal-fallback` + 请用户补充软件名与实验指导书
