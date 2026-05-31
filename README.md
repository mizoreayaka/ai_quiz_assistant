# 语文课堂AI出题助手
A smart quiz generator for Chinese Language Arts classes, powered by DeepSeek & Streamlit.

## 项目简介
本工具是一款专为初中语文教师设计的课堂互动出题助手。它基于国产大模型DeepSeek，通过Streamlit框架实现即开即用的网页应用。老师无需备课，点击“出题”按钮即可实时生成涵盖成语、诗词、文学常识等五种题型的语文知识题，有效提升课堂互动效率。

## 功能特点
- **零备课成本**：无需预设题库，AI实时生成题目。
- **即开即用**：单文件脚本，`streamlit run` 即可启动。
- **题型多样**：支持成语填空、诗词接龙、文学常识、修辞手法、字音字形随机切换。

## 安装与运行
1. 确保已安装 Python 3.8~3.11。
2. 安装依赖库：
```bash
pip install streamlit openai