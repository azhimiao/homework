# ML / Notebook 课设

## 环境

```bash
python scripts/check_python.py
pip install jupyter pandas numpy scikit-learn
jupyter --version
```

## 结构

```
homework/ml-homework/{project}/
├── notebooks/experiment.ipynb  # 或 src/train.py
├── data/README.md            # 数据来源说明，勿提交大文件
├── requirements.txt
├── outputs/figures/
└── docs/report.md
```

## 规范

| 项 | 要求 |
|----|------|
| 可复现 | 固定 random seed；记录 hyperparams |
| 数据 | 训练/验证划分说明；避免泄漏 |
| 评估 | 与任务匹配的 metrics（acc/F1/RMSE） |
| 图表 | 轴标签、图例、样本量说明 |

## 常见任务

分类、回归、聚类、简单 CNN（若课程要求）

## 伦理

- 不用未授权私人数据
- 不伪造 metrics 或 loss 曲线

## 报告

问题、数据、特征、模型、结果、误差分析、改进方向
