# NI Multisim

## 检测

```bash
python scripts/check_multisim.py
```

Multisim 主要为 GUI；脚本检测常见安装路径。

## 版本

Multisim 14/15 (Education) 常见；扩展名 .ms14 / .ms15

## 工程

```
homework/multisim-lab/{project}/
├── circuit.ms15
├── docs/components.md
├── outputs/waveforms/
└── docs/report.md
```

## 流程

1. 按原理图放置元件（电源、地、示波器）
2. 设置元件参数（电阻容差按 handout）
3. Run → Interactive Simulation
4. 双踪示波器读相位/幅值

## 文档

`docs/components.md`：位号、型号、参数表

## 禁止

- 未接地/电源缺失仍声称仿真通过
