# Python 作业规范（PEP 8 / 课程常见要求）

## 环境

```bash
python scripts/check_python.py
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 项目结构

```
homework/python-homework/{project}/
├── src/           # 或单文件 main.py
├── tests/         # pytest 若要求
├── requirements.txt
├── README.md      # 运行命令
└── docs/report.md
```

## 标准

| 项 | 要求 |
|----|------|
| 风格 | PEP 8；4 空格；有意义命名 |
| 入口 | `if __name__ == "__main__"` 或 CLI argparse |
| 依赖 | 固定版本 requirements.txt |
| 测试 | pytest 或 handout 给定用例 |
| 文档 | docstring 简述函数用途 |

## 常见课设类型

| 类型 | 要点 |
|------|------|
| 文件/数据处理 | pathlib, csv/json, 异常处理 |
| Web 小作业 | Flask/FastAPI 路由 + README 启动 |
| 爬虫 | robots.txt 意识；请求间隔；不教绕过登录 |

## 报告

目的、环境、设计、运行截图、问题总结
