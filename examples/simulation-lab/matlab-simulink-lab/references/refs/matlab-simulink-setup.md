# MATLAB / Simulink

## 检测

```bash
python scripts/check_matlab.py
matlab -batch "disp(version)"
```

## 版本

R2019b+ 常见；Simulink 需同一安装包。

## 工程结构

```
homework/matlab-lab/{project}/
├── scripts/*.m
├── models/*.slx
├── data/
├── outputs/figures/
└── docs/report.md
```

## 常用流程

| 任务 | 做法 |
|------|------|
| 传递函数分析 | `tf`, `step`, `rlocus`, `bode` |
| Simulink 建模 | 新建 .slx；Solver fixed-step 若离散 |
| PID | 先 Z-N 初值再 handout 要求整定 |
| 保存结果 | `saveas(gcf,...)` 或 Scope log |

## 参数记录

在 `docs/params.md` 记录：Kp,Ki,Kd / 采样时间 Ts / 被控对象参数

## 常见课设

二阶系统阶跃、PID 整定、状态反馈极点配置（按 handout）

## Windows 路径

`C:\Program Files\MATLAB\R20xx\bin\matlab.exe`
