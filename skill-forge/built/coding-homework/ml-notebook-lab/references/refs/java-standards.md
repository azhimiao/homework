# Java OOP 作业规范

## 环境

```bash
java -version
javac -version
# Maven: mvn -version
python scripts/check_java.py
```

## 项目结构（Maven 常见）

```
homework/java-homework/{project}/
├── pom.xml
├── src/main/java/...
├── src/test/java/...   # JUnit 5
└── docs/report.md
```

## 标准

| 项 | 要求 |
|----|------|
| OOP | 类职责单一；合理封装 private + getter |
| 命名 | 类 PascalCase；方法 camelCase |
| 测试 | JUnit 5 `@Test`；覆盖核心逻辑 |
| 构建 | `mvn test` 或 handout 指定命令 |

## 常见实验

- 继承/多态演示
- 集合框架（ArrayList/HashMap）
- 简单设计模式（Factory/Strategy 若课程要求）

## 禁止

- 编造 `mvn test` 通过截图；须真实运行
