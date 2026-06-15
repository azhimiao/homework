matlab-simulink-lab

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
Complete MATLAB/Simulink control or signal labs: verify MATLAB, build .m/.slx, run simulation, capture plots, params doc, report per report-template.md.

## Context
After homework-assistant routes (unified STEM catalog). Triggers: 自动控制原理, Simulink, 阶跃响应, PID.

## Constraints
- 精度：matlab-simulink-setup.md; document K,T,PID; no fake plots
- 工具：check_matlab.py first

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- lab_task: string

## Optional
- matlab_path, project_path, use_simulink: boolean, handout

---

# 3. Outputs（输出定义）

**Profile:** hybrid

1. `scripts/*.m`, `models/*.slx` if needed
2. `docs/params.md`, `outputs/figures/`
3. `docs/report.md` six-section

---

# 5. Execution Plan（执行流程）

1. READ refs/matlab-simulink-setup.md, report-template.md
2. RUN scripts/check_matlab.py; IF MATLAB_NOT_FOUND → guide install; STOP
3. ASK lab_task; READ handout
4. CREATE project under homework/matlab-lab/
5. IMPLEMENT .m or .slx; RECORD params in docs/params.md
6. RUN simulation; SAVE figures to outputs/figures/
7. IF Simulink → verify solver settings match handout
8. DRAFT docs/report.md; UPDATE checklist

---

# 6. Decision Logic（决策系统）

```
IF lab_task vague → ASK handout
IF simulation diverges from theory → note in analysis section
IF user claims results without run → refuse fabricated plots
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| shell | | |
| file_read, | | |

---

# 10. Failure Modes（失败模式）

## F1: matlab-missing
- Signal: MATLAB_NOT_FOUND
- Recovery: install MATLAB
- Severity: block

## F2: sim-error
- Signal: model does not run
- Recovery: fix equations/blocks
- Severity: block

## F3: vague-task
- Signal: no spec
- Recovery: ask handout
- Severity: block

## F4: fabricated-plot
- Signal: no run claimed
- Recovery: rerun and capture
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - homework-assistant
provides:
  - matlab-simulink-lab
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
status: stable
```
