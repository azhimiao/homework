multisim-lab

---

# 0. Compilation Target

```yaml
host: any
invocation: auto
output_profile: hybrid
```

---

# 1. Intent（意图）

Theme: simulation-lab

## Goal
Complete NI Multisim circuit simulation lab: verify install, build circuit, run interactive sim, waveform capture, component table, report.

## Context
电路分析, 模拟电路, Multisim. After homework-assistant routes (unified catalog).

## Constraints
- 精度：multisim-setup.md; power/ground required; no fake scope shots
- 工具：check_multisim.py

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- lab_task: string

## Optional
- multisim_path, project_path, handout

---

# 3. Outputs（输出定义）

**Profile:** hybrid

1. `circuit.ms14` or `.ms15`
2. `docs/components.md`
3. `outputs/waveforms/`
4. `docs/report.md`

---

# 5. Execution Plan（执行流程）

1. READ refs/multisim-setup.md, report-template.md
2. RUN scripts/check_multisim.py; IF MULTISIM_NOT_FOUND → guide NI install; STOP
3. ASK lab_task; READ handout schematic requirements
4. GUIDE place components; WRITE docs/components.md (RefDes, value)
5. RUN interactive simulation; CAPTURE oscilloscope to outputs/waveforms/
6. VERIFY DC paths and grounds before claiming success
7. DRAFT docs/report.md per report-template; UPDATE checklist

---

# 6. Decision Logic（决策系统）

```
IF missing ground → fix before delivery
IF component values differ from handout → document in report
IF fabricated waveform → refuse F4
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| shell | | |
| file_read, | | |

---

# 10. Failure Modes（失败模式）

## F1: multisim-missing
- Signal: MULTISIM_NOT_FOUND
- Recovery: install Multisim
- Severity: block

## F2: sim-fail
- Signal: circuit error
- Recovery: fix wiring/values
- Severity: block

## F3: vague-task
- Signal: no spec
- Recovery: ask handout
- Severity: block

## F4: fabricated-plot
- Signal: fake scope
- Recovery: rerun simulation
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - homework-assistant
provides:
  - multisim-lab
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
status: stable
```
