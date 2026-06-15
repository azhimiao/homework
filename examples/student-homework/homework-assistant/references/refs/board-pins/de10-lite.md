# DE10-Lite 常用引脚参考

来源：Terasic DE10-Lite User Manual（使用前请与最新 PDF 核对）  
手册：https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=165&No=1042

## 时钟与按键

| 信号 | PIN | 说明 |
|------|-----|------|
| MAX10_CLK1_50 | PIN_P11 | 50 MHz 时钟（常用主时钟） |
| MAX10_CLK2_50 | PIN_N14 | 第二路 50 MHz |
| KEY[0] | PIN_B8 | 按键 0，低有效 |
| KEY[1] | PIN_A7 | 按键 1 |

## 拨码与 LED（实验常用）

| 信号 | PIN |
|------|-----|
| SW[0] | PIN_C10 |
| SW[1] | PIN_C11 |
| SW[2] | PIN_D12 |
| SW[3] | PIN_C12 |
| LEDR[0] | PIN_A8 |
| LEDR[1] | PIN_A9 |
| LEDR[2] | PIN_A10 |
| LEDR[3] | PIN_B10 |
| LEDR[4] | PIN_D13 |
| LEDR[5] | PIN_C14 |
| LEDR[6] | PIN_A11 |
| LEDR[7] | PIN_B11 |
| LEDR[8] | PIN_C9 |
| LEDR[9] | PIN_D9 |

## Verilog 引脚约束示例（复制到 .qsf 或 Pin Planner）

```tcl
set_location_assignment PIN_P11 -to clk
set_location_assignment PIN_A8  -to led[0]
set_location_assignment PIN_C10 -to sw[0]
```

或在 Pin Planner 中：`Assignments → Pin Planner`，Node Name 填顶层端口名。

## 注意

- 端口名必须与顶层 module 端口**完全一致**（含位宽、命名）
- 上板前确认 **Programmer** 中 USB-Blaster 已识别
- SOF 文件路径：`output_files/{project}.sof`
