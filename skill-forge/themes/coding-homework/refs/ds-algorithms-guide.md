# 数据结构 / 算法实验

## 依据

- CLRS / 《算法导论》课程常见实验
- 复杂度：时间/空间 O() 必须写清

## 语言

默认 Python；handout 指定 Java/C++ 则跟随

## 结构

```
homework/ds-homework/{topic}/
├── src/{algorithm}.py
├── tests/test_{algorithm}.py
├── docs/complexity.md
└── docs/report.md
```

## 必交付

1. 正确性：对拍 / 给定测例全过
2. 复杂度分析（最好/最坏/平均）
3. 关键数据结构说明（数组/链表/树）

## 常见题

排序、BST、图 BFS/DFS、最短路径基础、堆

## 测试

```bash
python -m pytest tests/ -v
```

禁止仅贴 LeetCode 链接无本地可运行代码（除非 handout 允许）
