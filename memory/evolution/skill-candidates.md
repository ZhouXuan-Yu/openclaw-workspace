# Skill 候选列表

从成功模式中捕获的可复用流程。验证 ≥2 次后创建正式 Skill。

---

## 候选: 源码分析工作流

**触发**: 用户要求分析某个开源项目
**状态**: candidate (验证 1/2)
**工具链**:
1. `web_search` — 搜索项目概览
2. `web_fetch` — 抓取 GitHub README
3. `exec curl` — 获取 GitHub API 数据 (stars/forks/etc)
4. `exec Get-ChildItem` — 分析目录结构
5. `read` — 读取关键源文件
6. `write` — 写入分析报告到 topics/

**输出**: `memory/topics/<project>-analysis.md`

**验证记录**:
- 2026-06-12: OpenSpec 分析 ✅ 成功
- 2026-06-12: OpenGAP 规范分析 ✅ 成功（第 2 次验证，达到创建 Skill 阈值）

---

## 候选: 架构增强整合

**触发**: 分析完外部项目后，整合到当前架构
**状态**: candidate (验证 1/2)
**工具链**:
1. 读取当前架构文件 (AGENTS.md, AGENTS-DETAILS.md, MEMORY.md)
2. 对比外部架构 vs 当前架构
3. 提取可借鉴模式
4. 写入增强方案到 `topics/<project>-arch-enhancements.md`
5. 更新 AGENTS-DETAILS.md
6. 更新 MEMORY.md 索引

**输出**: 架构增强方案 + 实际文件更新

**验证记录**:
- 2026-06-12: OpenSpec → Delta 变更追踪 ✅ 成功
- 2026-06-12: OpenGAP → 14 设计模式整合 ✅ 成功（第 2 次验证，达到创建 Skill 阈值）
