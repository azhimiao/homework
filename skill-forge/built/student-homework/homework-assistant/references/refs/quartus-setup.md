# Quartus 环境与工程（准确版）

## 安装

1. https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/download.html
2. 选 **Quartus Prime Lite**（教学免费）
3. **Device support 必选对**（见 `board-devices.yaml`）：
   - DE10-Lite → **MAX 10**
   - DE1-SoC / DE2-115 等 → 对应 Cyclone 系列

Windows 典型路径：`C:\intelFPGA_lite\<version>\quartus\bin64\quartus.exe`

## 自动检测

```bash
python scripts/check_quartus.py
# 或 skill 内：python references/scripts/check_quartus.py
```

输出 `QUARTUS_PATH=...` 与 `--version` 信息；`QUARTUS_NOT_FOUND` 表示未安装或未加入 PATH。

## 命令行编译（与 GUI 等价）

工程目录含 `{name}.qpf` 时：

```bash
quartus_sh --flow compile {project_name}
```

仅综合：

```bash
quartus_map --analysis_and_elaboration {project_name}
```

## GUI 流程（菜单准确）

| 步骤 | 菜单 |
|------|------|
| 新建工程 | File → New Project Wizard… |
| 引脚 | Assignments → Pin Planner |
| 综合 | Processing → Start Analysis & Synthesis |
| 全编译 | Processing → Start Compilation |
| 下载 | Tools → Programmer → Hardware Setup → Start |

## 板卡与器件

**以 `board-devices.yaml` 为准**，勿凭记忆填写。DE10-Lite = MAX 10 **10M50DAF484C7G**。

引脚示例见 `board-pins/de10-lite.md`（须与 Terasic 手册核对）。

## 实验报告结构

1. 实验目的  2. 原理  3. 设计与代码  4. 引脚表  5. 仿真/上板结果  6. 总结

## 常见错误

| 现象 | 原因 | 处理 |
|------|------|------|
| Can't fit design | Device 选错 | 对照 board-devices.yaml |
| Pin not found | 端口名与 Pin Planner 不一致 | 统一顶层命名 |
| Programmer no hardware | 驱动/USB-Blaster | 设备管理器检查 |
| Error: can't launch | PATH 未配置 | 运行 check_quartus.py |
