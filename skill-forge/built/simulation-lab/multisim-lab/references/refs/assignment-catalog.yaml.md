# MD 兼容视图 — `assignment-catalog.yaml`

> **权威源文件**：同目录 `assignment-catalog.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/assignment-catalog.yaml` |
| 用途 | 作业/任务路由 catalog；router skill 打分与 install 列表。 |

## 内容

```yaml
version: "1.0"

majors:
  - id: ee
    aliases: [电子信息, 电子信息工程, 电子, 通信, EE, 电信]
  - id: auto
    aliases: [自动化, 电气工程及其自动化, 电气, 控制]
  - id: cs
    aliases: [计算机, 嵌入式, 物联网]

assignments:
  - id: matlab-control-lab
    title: MATLAB / Simulink 仿真实验
    status: ready
    majors: [ee, auto, cs]
    match_keywords:
      - matlab
      - simulink
      - 自动控制
      - 控制原理
      - 现代控制
      - 传递函数
      - pid
      - 阶跃响应
      - 根轨迹
    skills_to_install:
      - name: matlab-simulink-lab
        scope: project
    workspace_subdir: matlab-lab
    deliverables:
      - .m 或 .slx 源文件
      - 仿真波形/Scope 截图
      - 参数说明 (K, T, 阻尼比等)
      - 实验报告

  - id: multisim-circuit-lab
    title: Multisim 电路仿真实验
    status: ready
    majors: [ee, auto]
    match_keywords:
      - multisim
      - 电路分析
      - 模拟电路
      - 数字电路
      - 电工电子
      - ni multisim
      - 电路仿真
    skills_to_install:
      - name: multisim-lab
        scope: project
    workspace_subdir: multisim-lab
    deliverables:
      - .ms14/.ms15 工程或导出网表
      - 仿真波形截图
      - 元件参数表
      - 实验报告

  - id: keil-embedded-lab
    title: Keil / 嵌入式单片机实验
    status: ready
    majors: [ee, auto, cs]
    match_keywords:
      - keil
      - uvision
      - stm32
      - 51单片机
      - 8051
      - 嵌入式
      - mdk
      - 单片机实验
    skills_to_install:
      - name: keil-embedded-lab
        scope: project
    workspace_subdir: keil-lab
    default_mcu: STM32F103C8
    deliverables:
      - Keil 工程 (.uvprojx)
      - 源码与头文件
      - 编译 log / hex
      - 板级现象说明或仿真截图
      - 实验报告

matching:
  min_score: 2
  tie_threshold: 1
  keyword_weight: 2
  major_weight: 3

install:
  default_host: cursor
  default_scope: project
  cli_template: "python skill-core/skill.py install {skill} --host {host} --scope {scope} --project {project_dir} --force"
  resolve_order:
    - registry
    - examples/{skill}
    - skill-forge/built/simulation-lab/{skill}
    - skill-forge/built/student-homework/{skill}
```
