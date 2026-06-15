# Skill Forge

批量生产 Agent Skills 的工作区。**源文件以 `.md` / `.txt` 为主**；`.yaml` / `.json` / `.py` 会在 `batch build` 时自动生成 **MD 兼容视图**（`foo.yaml` → `foo.yaml.md`）。

```
skill-forge/
├── README.md           ← 本文件
├── themes/             ← 你按主题建文件夹，往里放 md/txt
│   ├── _template/      ← 复制这个开始新主题
│   └── <你的主题>/
│       ├── THEME.md    ← 主题说明（不参与编译）
│       ├── foo.skill.md
│       ├── bar.skill.txt
│       └── refs/
│           ├── catalog.yaml      ← 权威源
│           └── catalog.yaml.md   ← 自动生成，Agent 可读 Markdown 镜像
└── built/              ← 编译输出（自动生成，勿手改）
    └── <主题>/
        └── <skill-name>/
            ├── SKILL.md
            └── references/
```

---

## 1. 新建主题

```bash
python skill-core/skill.py batch new-theme my-topic --title "My Topic"
```

会在 `themes/my-topic/` 创建 `THEME.md` 和示例 `.skill.md`。

## 2. 写 skill 源文件

在主题文件夹里新增文件，支持：

| 格式 | 示例 |
|------|------|
| Markdown | `code-review.skill.md` |
| 纯文本 | `email-draft.skill.txt` |

**不要**把 `THEME.md` / `README.md` 当 skill 源文件。

### 非 Markdown 源文件（YAML / JSON / Python）

| 权威源 | MD 兼容视图（自动） |
|--------|---------------------|
| `refs/catalog.yaml` | `refs/catalog.yaml.md` |
| `refs/profile-schema.json` | `refs/profile-schema.json.md` |
| `scripts/check_foo.py` | `scripts/check_foo.py.md` |

`batch build` 会先生成/更新 `*.yaml.md` 等镜像，再编译进 `references/refs/`。**改 YAML/JSON/PY 后重新 build 即可同步 MD 视图。**

仅同步 MD 镜像、不编译：

```bash
python skill-core/skill.py batch compat              # 全部 theme
python skill-core/skill.py batch compat student-homework
python skill-core/skill.py batch compat companion-memory
```

工科与记忆主题的镜像清单见各 theme `refs/md-compat-index.md`。

### 精简格式（.skill.md）

```markdown
---
name: my-skill
profile: narrative
status: experimental
---

# Goal
一句话说明解决什么问题。

# Context
什么时候用这个 skill。

# Steps
1. READ 输入
2. GENERATE 输出
3. VALIDATE 结果非空

# Decision
IF 缺少输入 → ASK author

# Tools
- ask_user
- file_read

# Failures
F1: missing-input | 输入为空 | ask author
F2: vague-scope | 意图不清 | ask to clarify
F3: empty-output | 输出为空 | regenerate
```

### 纯文本格式（.skill.txt）

```text
name: my-skill
profile: narrative

[goal]
一句话目标

[context]
使用场景

[steps]
- READ 输入
- GENERATE 输出

[failures]
F1: missing-input | 输入为空 | ask author
```

## 3. 批量编译

```bash
# 编译单个主题
python skill-core/skill.py batch build my-topic

# 编译全部主题
python skill-core/skill.py batch build-all

# 编译并跑测试
python skill-core/skill.py batch build my-topic --test
```

输出在 `skill-forge/built/<主题>/<skill-name>/`。

### 导出到 `examples/`（按 theme 分组）

`examples/` 与 `built/` **同构**，不再把 35 个 skill 摊平在根目录：

```
examples/
  research/research-survey/
  student-homework/homework-assistant/
  coding-homework/python-lab/
  demo/simple-readme-writer/   # 模板 skill
```

```bash
python skill-core/skill.py batch build-all --test   # 或分 theme build
python skill-core/scripts/export_examples.py
python skill-core/skill.py registry build
```

## 4. 安装到 IDE

```bash
python skill-core/skill.py install examples/student-homework/homework-assistant --host cursor --scope global
# 或直接从 built：
python skill-core/skill.py install skill-forge/built/student-homework/homework-assistant --host cursor --scope global
```

## 5. 工作流建议

```
定主题 → themes/xxx/ 里写多个 .skill.md
       → batch build xxx
       → batch build-all --test
       → install / 推 registry
```

---

## 主题列表

在 `themes/` 下每个子文件夹 = 一个主题。你说要设定多个主题时，直接：

```bash
skill batch new-theme dev-tools --title "开发工具"
skill batch new-theme writing --title "写作助手"
skill batch new-theme data --title "数据分析"
```

然后在各自文件夹里批量加 md/txt 即可。
