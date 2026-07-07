# 第13章 智能旅行助手

## Core Idea
完整旅行助手项目，整合 HelloAgents、MCP 协议、多 Agent 协作和前后端分离架构。用户输入目的地/日期/偏好后自动生成完整行程。

## Frameworks Introduced
- **Vue3+TypeScript 前端**: 用户交互和地图可视化
- **FastAPI 后端**: API 路由和数据验证
- **高德地图 API**: 地图标注和路线绘制
- **Unsplash API**: 景点图片

## Key Concepts
- **四层架构** — 前端/后端/智能体/外部服务
- **多 Agent 协作** — 景点/天气/酒店/行程 四个专门 Agent
- **MCP 协议** — Agent 通过 MCP 调用外部 API
- **行程规划 pipeline** — 用户输入→拆分任务→调用工具→整合→渲染
- **预算计算** — 门票/酒店/餐饮/交通自动计算

## Mental Models
1. **"四层管道"**: 用户输入从前端→后端→智能体→外部服务流回
2. **"专家委员会"**: 4 个专门 Agent 各管一个领域

## Anti-patterns
- 一个 Agent 包揽所有能力导致提示词臃肿
- 忽略 API 错误处理
- 缓存欠缺导致重复调用

## Code Examples
```
@app.post("/api/plan-trip")
async def plan_trip(request: TripRequest):
    agents = [AttractionAgent(), WeatherAgent(), HotelAgent(), ItineraryAgent()]
    results = await asyncio.gather(*[a.run(request) for a in agents])
    return assemble_plan(request, results)
```

## Worked Example
**输入"北京3天游，历史文化，中等预算"**: WeatherAgent 查天气→AttractionAgent 搜景点→HotelAgent 找酒店→ItineraryAgent 编排行程→前端展示地图标记和预算明细。

## Key Takeaways
1. 多 Agent 拆分比单 Agent 多工具更稳定
2. MCP 简化外部 API 集成
3. 前后端分离便于独立开发

## Connects To
- Ch01: 第一章旅行助手升级
- Ch10: MCP 协议
