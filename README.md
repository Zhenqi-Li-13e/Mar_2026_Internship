# Omaka-Internship

## 量化金融实习记录

本仓库用于记录我的量化金融实习过程，总共将完成 **100 个 tasks**。

> 持续更新中...

---

## 已完成项目

### P004 - SQL基础与金融数据查询
- **难度**：⭐ | **预计耗时**：1天
- **目标**：掌握SQL基础，能对金融数据进行查询分析
- **具体内容**：
  - MySQL基本语法学习（SELECT, JOIN, GROUP BY, 窗口函数）
  - 交易日历表创建与数据导入
  - 股票/ETF基本信息表设计与数据导入
  - 查询练习：找出最近30个交易日日均成交额Top20的ETF
- **包含文件**：database.py, data_loader.py, financial_loader.py, sql_exercises.py, top20_query.py, main.py 等

### P005 - Pandas数据处理入门
- **难度**：⭐ | **预计耗时**：1天
- **目标**：掌握pandas处理金融时序数据的基本操作
- **具体内容**：
  - 使用AKShare读取CSV格式股票行情数据
  - 数据清洗：缺失值处理、异常值检测
  - 计算日收益率、累计收益率、移动平均线
  - 实现技术指标：MA5/MA20/MACD/RSI
- **包含文件**：data_fetcher.py, data_cleaner.py, data_analysis.py, technical_indicators.py, visualizer.py, main.py 等
