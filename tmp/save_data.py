# -*- coding: utf-8 -*-
import sys, io, json
sys.path.insert(0, r"C:\Users\ZhouXuan\.openclaw\workspace\tools\daily-research")
import pipeline

websearch = [
    {"kw": "AI Agent 智能体 最新进展", "provider": "tavily", "items": [
        {"title": "一文看懂2025年Agent六大最新趋势", "url": "https://ppio.com/blogs/post/yi-wen-kan-dong-2025nian-agentliu-da-zui-xin-qu-shi-aizhuan-lan"},
        {"title": "8 款领先 AI 智能体框架", "url": "https://www.kimi.ai/zh-hans/resources/best-ai-agent-frameworks"},
        {"title": "自进化智能体综述：通往超级人工智能之路", "url": "https://zhuanlan.zhihu.com/p/1937626679519450682"},
        {"title": "AI 智能体：从Manus引爆到产业重塑 (CCF)", "url": "https://www.ccf.org.cn/ccfdl/ccf_dl_focus/new/25-9-53"},
        {"title": "HuggingAGI/AwesomeAgentPapers", "url": "https://github.com/HuggingAGI/AwesomeAgentPapers"},
    ]},
    {"kw": "大模型 开源 趋势 2026", "provider": "tavily", "items": [
        {"title": "2026 年开源大模型 TOP10 完整榜单", "url": "https://zhuanlan.zhihu.com/p/2009705203163752429"},
        {"title": "开源模型最全盘点（2026年7月版）：中美14家厂商30+模型", "url": "https://deepseek.csdn.net/6a55a1bd10ee7a33f28d37f1.html"},
        {"title": "2026开源大模型终极横评：15款热门模型", "url": "https://cloud.tencent.com/developer/article/2657621"},
        {"title": "2026大模型全景分析报告（DeepSeek V4-Pro / Kimi K2.6）", "url": "https://zhuanlan.zhihu.com/p/2038178950019556726"},
        {"title": "2026年2月AI模型大爆发", "url": "https://jangwook.net/zh/blog/zh/ai-model-rush-february-2026"},
    ]},
    {"kw": "AI 行业 热点新闻", "provider": "tavily", "items": [
        {"title": "AI工具集 每日AI资讯", "url": "https://ai-bot.cn/daily-ai-news"},
        {"title": "AIBase 最新资讯", "url": "https://news.aibase.com/zh/news"},
        {"title": "AI产品榜 每日AI早报", "url": "https://www.aicpb.com/news"},
        {"title": "Artificial Intelligence News", "url": "https://www.artificialintelligence-news.com"},
    ]},
    {"kw": "AI Agent LLM this week 2026", "provider": "tavily", "items": [
        {"title": "Top LLM, RAG and Agent Updates of this week", "url": "https://aixfunda.substack.com/p/top-llm-rag-and-agent-updates-of-03a"},
        {"title": "AI Weekly: Agents, Models, and Chips", "url": "https://dev.to/alexmercedcoder/ai-weekly-agents-models-and-chips-april-9-15-2026-486f"},
        {"title": "AI Trends 2026: OpenClaw Agents, Reasoning LLMs (TWIML)", "url": "https://twimlai.com/podcast/twimlai/ai-trends-2026-openclaw-agents-reasoning-llms"},
        {"title": "Best AI Coding Agents (August 2026) Leaderboard", "url": "https://www.morphllm.com/best-ai-coding-agents-2026"},
    ]},
    {"kw": "new LLM model release architecture 2026", "provider": "tavily", "items": [
        {"title": "Choosing the Right LLM in 2026: 8 Architectures", "url": "https://www.youtube.com/watch?v=fpOEfxNXeJA"},
        {"title": "LLM Architecture in 2026 with Sebastian Raschka", "url": "https://www.youtube.com/watch?v=Y6APnyZT6XU"},
    ]},
    {"kw": "GitHub trending AI projects 2026", "provider": "tavily", "items": [
        {"title": "OSS Insight — Trending AI Repositories", "url": "https://ossinsight.io/trending/ai"},
        {"title": "Top 20 AI Projects on GitHub to Watch in 2026", "url": "https://www.nocobase.com/en/blog/best-open-source-ai-projects-github-2026"},
        {"title": "Top 10 Open-Source AI Projects Trending on GitHub in 2026", "url": "https://shop.zimaspace.com/en-ca/blogs/tech-ai-hub/top-10-open-source-ai-projects-trending-on-github-in-2026"},
        {"title": "Top 100 Best AI Projects on GitHub | 2026", "url": "https://www.aixploria.com/en/category/github-project-ai"},
        {"title": "Top AI GitHub Repositories in 2026 (ByteByteGo)", "url": "https://blog.bytebytego.com/p/top-ai-github-repositories-in-2026"},
    ]},
]

social = [
    {"source": "AI工具集 每日AI快讯", "url": "https://ai-bot.cn/daily-ai-news", "date": "2026-09-07~2026-09-11"},
    {"source": "AIBase 最新资讯", "url": "https://news.aibase.com/zh/news", "date": "2026-09-10~2026-09-11"},
    {"source": "AI产品榜 每日AI早报", "url": "https://www.aicpb.com/news"},
]

r1 = pipeline.save_websearch(json.dumps(websearch, ensure_ascii=False))
r2 = pipeline.save_social(json.dumps(social, ensure_ascii=False))
print(json.dumps({"websearch": r1, "social": r2}, ensure_ascii=False))
