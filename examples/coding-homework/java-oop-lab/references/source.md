---
name: java-oop-lab
profile: hybrid
status: stable
version: "1.0.0"
invocation: auto
host: any
---

# Goal
Complete Java OOP lab: verify JDK/Maven, scaffold Maven project, implement classes, JUnit tests, report.

# Context
After coding-homework-assistant routes Java/OOP. Triggers: "Java实验", "JUnit", "面向对象", "Maven 作业".

# Constraints
- 精度：java-standards.md; mvn test must pass if claimed
- 诚信：no fabricated test screenshots

# Inputs
## Required
- lab_task: string

## Optional
- jdk_version, project_path, handout, use_maven: boolean

# Outputs
**Profile:** hybrid

1. Maven or handout layout under `homework/java-homework/{project}/`
2. `src/main/java`, `src/test/java`
3. `docs/report.md`

# Steps
1. READ refs/java-standards.md
2. RUN scripts/check_java.py; IF JAVA_NOT_FOUND → guide JDK install; STOP
3. ASK lab_task; READ handout
4. CREATE pom.xml if Maven; package src/main/java structure per handout
5. IMPLEMENT OOP design; WRITE JUnit tests
6. RUN mvn test or javac/java; LOG output
7. DRAFT docs/report.md; UPDATE checklist

# Decision
IF no Maven in course → plain javac layout ok
IF tests fail → fix before claim pass
IF cheat request → refuse F4

# Tools
- shell — javac, java, mvn
- file_read, file_write, ask_user

# Failures
F1: java-missing | JAVA_NOT_FOUND | install JDK
F2: test-fail | JUnit fail | fix
F3: vague-task | no spec | ask handout
F4: integrity-violation | cheat | refuse

# Deps
depends_on:
  - skill-core
  - coding-homework-assistant
provides:
  - java-oop-lab

# Version
version: "1.0.0"
status: stable
