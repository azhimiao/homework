java-oop-lab

---

# 0. Compilation Target

```yaml
host: any
invocation: auto
output_profile: hybrid
```

---

# 1. Intent（意图）

Theme: coding-homework

## Goal
Complete Java OOP lab: verify JDK/Maven, scaffold Maven project, implement classes, JUnit tests, report.

## Context
After coding-homework-assistant routes Java/OOP. Triggers: "Java实验", "JUnit", "面向对象", "Maven 作业".

## Constraints
- 精度：java-standards.md; mvn test must pass if claimed
- 诚信：no fabricated test screenshots

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- lab_task: string

## Optional
- jdk_version, project_path, handout, use_maven: boolean

---

# 3. Outputs（输出定义）

**Profile:** hybrid

1. Maven or handout layout under `homework/java-homework/{project}/`
2. `src/main/java`, `src/test/java`
3. `docs/report.md`

---

# 5. Execution Plan（执行流程）

1. READ refs/java-standards.md
2. RUN scripts/check_java.py; IF JAVA_NOT_FOUND → guide JDK install; STOP
3. ASK lab_task; READ handout
4. CREATE pom.xml if Maven; package src/main/java structure per handout
5. IMPLEMENT OOP design; WRITE JUnit tests
6. RUN mvn test or javac/java; LOG output
7. DRAFT docs/report.md; UPDATE checklist

---

# 6. Decision Logic（决策系统）

```
IF no Maven in course → plain javac layout ok
IF tests fail → fix before claim pass
IF cheat request → refuse F4
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| shell | | |
| file_read, | | |

---

# 10. Failure Modes（失败模式）

## F1: java-missing
- Signal: JAVA_NOT_FOUND
- Recovery: install JDK
- Severity: block

## F2: test-fail
- Signal: JUnit fail
- Recovery: fix
- Severity: block

## F3: vague-task
- Signal: no spec
- Recovery: ask handout
- Severity: block

## F4: integrity-violation
- Signal: cheat
- Recovery: refuse
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - coding-homework-assistant
provides:
  - java-oop-lab
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
status: stable
```
