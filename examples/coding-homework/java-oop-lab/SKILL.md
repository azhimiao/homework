---
name: java-oop-lab
description: >-
  Complete Java OOP lab: verify JDK/Maven, scaffold Maven project, implement classes, JUnit
  tests, report. Use when after coding-homework-assistant routes Java/OOP. Triggers:
  "Java实验", "JUnit", "面向对象", "Maven 作业".
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
---

# Java Oop Lab

## Quick Start

1. READ refs/java-standards.md
2. RUN scripts/check_java.py; IF JAVA_NOT_FOUND → guide JDK install; STOP
3. ASK lab_task; READ handout
4. CREATE pom.xml if Maven; package src/main/java structure per handout
5. IMPLEMENT OOP design; WRITE JUnit tests

## Workflow

### Step 1
READ refs/java-standards.md

### Step 2
RUN scripts/check_java.py; IF JAVA_NOT_FOUND → guide JDK install; STOP

### Step 3
ASK lab_task; READ handout

### Step 4
CREATE pom.xml if Maven; package src/main/java structure per handout

### Step 5
IMPLEMENT OOP design; WRITE JUnit tests

### Step 6
RUN mvn test or javac/java; LOG output

### Step 7
DRAFT docs/report.md; UPDATE checklist

### Decision logic

```
IF no Maven in course → plain javac layout ok
IF tests fail → fix before claim pass
IF cheat request → refuse F4
```

## Outputs

Profile: `hybrid`

Return artifacts plus a narrative summary.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| shell |  |  |
| file_read, |  |  |

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | JAVA_NOT_FOUND | install JDK |
| F2 | JUnit fail | fix |
| F3 | no spec | ask handout |
| F4 | cheat | refuse |

## Dependencies

- `skill-core`
- `coding-homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
