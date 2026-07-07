# 第14章 自动化深度研究智能体

## Core Idea
知识密集型深度研究助手，具备问题剖析、多轮采集、反思总结三大能力。将 1-2 小时研究压缩到 5-10 分钟。

## Frameworks Introduced
- **SSE (Server-Sent Events)**: 流式推送进度
- **SearchTool / NoteTool**: 搜索和笔记工具

## Key Concepts
- **问题剖析** — 开放主题拆解为可检索查询语句
- **TODO Planner Agent** — 规划子任务
- **Task Summarizer Agent** — 总结搜索结果
- **Report Writer Agent** — 整合生成结构化报告
- **多轮信息采集** — 多种搜索 API 去重整合
- **反思与总结** — 识别知识空白决定继续/结束
- **NoteTool** — 渐进式知识积累

## Mental Models
1. **"研究流水线"**: 规划→搜索→总结→再搜索→报告
2. **"知识增量"**: 信息累积到饱和后生成报告

## Anti-patterns
- 一次搜索就生成报告
- 无限制搜索
- 忽略来源引用

## Code Examples
```
@router.get("/research/stream")
async def research_stream(topic: str):
    async def event_generator():
        sub_tasks = planner_agent.plan(topic)
        for task in sub_tasks:
            result = search_tool.run(task)
            summary = summarizer_agent.summarize(result)
            note_tool.save(task, summary)
        report = report_writer.generate(all_notes)
        yield {"type": "report", "content": report}
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

## Worked Example
**研究"Transformer 在 Agent 中的应用"**: 分解为子任务→逐个搜索总结→NoteTool 保存→Report Writer 整合 Markdown 报告含来源。

## Key Takeaways
1. "分解-搜索-总结-整合"是核心循环
2. SSE 流式推送提升用户体验
3. NoteTool 实现渐进式知识积累
4. 反思机制防止信息过载

## Connects To
- Ch08: NoteTool 依赖记忆系统
- Ch13: 项目架构复用
