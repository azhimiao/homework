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
  - id: cs
    aliases: [计算机, 计算机科学, 计算机科学与技术, 软件工程, CS, 计科, 人工智能, AI]
  - id: ds
    aliases: [数据科学, 大数据, 统计]

assignments:
  - id: python-coursework
    title: Python 程序设计 / 程设作业
    status: ready
    majors: [cs, ds]
    match_keywords:
      - python
      - 程序设计
      - 程设
      - py作业
      - 爬虫作业
      - flask
      - django
      - 脚本
    skills_to_install:
      - name: python-lab
        scope: project
    workspace_subdir: python-homework
    deliverables:
      - 源代码 (.py) 与 requirements.txt
      - 运行截图或终端输出
      - README 运行说明
      - 实验/课程报告（若要求）

  - id: java-oop-lab
    title: Java / 面向对象程序设计
    status: ready
    majors: [cs]
    match_keywords:
      - java
      - 面向对象
      - oop
      - junit
      - maven
      - gradle
      - spring基础
    skills_to_install:
      - name: java-oop-lab
        scope: project
    workspace_subdir: java-homework
    deliverables:
      - 源码与项目结构 (src/)
      - 单元测试 (JUnit)
      - 编译运行截图
      - 实验报告

  - id: ds-algorithm-lab
    title: 数据结构 / 算法实验
    status: ready
    majors: [cs]
    match_keywords:
      - 数据结构
      - 算法
      - 链表
      - 二叉树
      - 排序
      - 图论
      - leetcode
      - 复杂度
    skills_to_install:
      - name: ds-algorithm-lab
        scope: project
    workspace_subdir: ds-homework
    default_language: python
    deliverables:
      - 实现代码 + 复杂度说明
      - 测试用例与运行结果
      - 可选可视化截图
      - 实验报告

  - id: ml-notebook-lab
    title: 机器学习 / 数据分析课设
    status: ready
    majors: [cs, ds]
    match_keywords:
      - 机器学习
      - 深度学习
      - ml
      - notebook
      - jupyter
      - pandas
      - numpy
      - sklearn
      - pytorch
      - tensorflow
      - 课设
      - 数据分析
    skills_to_install:
      - name: ml-notebook-lab
        scope: project
    workspace_subdir: ml-homework
    deliverables:
      - .ipynb 或 .py 流水线
      - requirements.txt / environment.yml
      - 结果图表与 metrics
      - 实验报告（方法、数据、结论）

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
    - skill-forge/built/coding-homework/{skill}
    - skill-forge/built/student-homework/{skill}
```
