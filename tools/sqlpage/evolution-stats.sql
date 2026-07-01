-- ============================================
-- 进化引擎 — 能力状态 + 信任注册表
-- ============================================
SELECT 'shell' AS component,
  '进化引擎' AS title,
  'trending-up' AS icon,
  '[{"title":"首页","link":"/index.sql","icon":"home"}]' AS menu_item;

-- Overview Cards
SELECT 'card' AS component, 4 AS columns;

SELECT '总能力' AS title,
  '6' AS description,
  '1 passed · 4 practicing · 1 recorded' AS footer,
  'purple' AS color, 'stars' AS icon
FROM (SELECT 1);

SELECT '信任条目' AS title,
  '6' AS description,
  '5 条高信任 (>=0.8)' AS footer,
  'green' AS color, 'shield-check' AS icon
FROM (SELECT 1);

SELECT '进化文件' AS title,
  '39' AS description,
  '11 observations + 6 traces' AS footer,
  'blue' AS color, 'archive' AS icon
FROM (SELECT 1);

SELECT '协议版本' AS title,
  'v5' AS description,
  'Think+ModeRouter+Verify' AS footer,
  'orange' AS color, 'settings' AS icon
FROM (SELECT 1);

-- ============================================
-- Capability Status (using list instead of progress)
-- ============================================
SELECT 'title' AS component, '能力进化状态' AS contents, 2 AS level;

SELECT 'list' AS component, '研究分析 (cap-research-analyze)' AS title;
SELECT 'Level: PASSED' AS title,
  '连续 10 次成功 · 已通过迁移测试 · 可晋升 (promotionEligible=true)' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT 'list' AS component, 'Skill 自进化 (cap-skill-evolution)' AS title;
SELECT 'Level: PRACTICED → 接近 PASSED' AS title,
  '连续 13 次成功 · 9 条成功证据 · 从空壳进化到稳定运行' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT 'list' AS component, '记忆架构管理 (cap-memory-management)' AS title;
SELECT 'Level: PRACTICED' AS title,
  '记忆 4 层 + 智能检索 + 进化引擎全量审计' AS description,
  'blue' AS color
FROM (SELECT 1);

SELECT 'list' AS component, '多平台内容发布 (cap-multi-platform-publish)' AS title;
SELECT 'Level: PRACTICED' AS title,
  '5 平台 CLI · 小红书草稿模式修复 · 1 次成功' AS description,
  'yellow' AS color
FROM (SELECT 1);

SELECT 'list' AS component, '架构进化 v3 (cap-architecture-evolution)' AS title;
SELECT 'Level: PRACTICED' AS title,
  'v5 Think+ModeRouter+Verify → v3 惰性检测器+长任务循环+RuleMaturity' AS description,
  'blue' AS color
FROM (SELECT 1);

SELECT 'list' AS component, '惰性检测器 (cap-laziness-detection)' AS title;
SELECT 'Level: RECORDED (新建)' AS title,
  'CAPTURED from v3 架构升级 · 7 种检测器 · 待首次实战验证' AS description,
  'blue' AS color
FROM (SELECT 1);

-- ============================================
-- Trust Registry
-- ============================================
SELECT 'title' AS component, '信任注册表' AS contents, 2 AS level;

SELECT 'list' AS component, 'Iron Law (trust=1.0, 永久不可降)' AS title;

SELECT '浏览器策略: 统一使用 Edge' AS title,
  '信任度 1.0 · 来源 MEMORY.md · 层级 core_profile' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT '记忆架构4层方案' AS title,
  '信任度 1.0 · 来源 decisions.md · 层级 decision' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT 'list' AS component, 'High Trust (>0.8)' AS title;

SELECT 'Wechatsync CLI 模式' AS title,
  '信任度 0.9 · 层级 fact · 不封装 MCP' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT '多平台发布 5 平台 CLI' AS title,
  '信任度 0.9 · 层级 fact · 已验证通过' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT 'v5 进化架构' AS title,
  '信任度 0.9 · 层级 decision · Think+ModeRouter+Verify' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT '小红书草稿模式' AS title,
  '信任度 0.8 · 层级 fact · AI 托管检测修复' AS description,
  'blue' AS color
FROM (SELECT 1);

-- ============================================
-- Evolution Files
-- ============================================
SELECT 'title' AS component, '进化引擎文件' AS contents, 2 AS level;

SELECT 'list' AS component, '核心文件' AS title;

SELECT 'capability-state.json' AS title,
  '能力状态机 — 6 个能力追踪' AS description,
  'green' AS color,
  '/file-browser.sql?file_path=memory/evolution/capability-state.json' AS link
FROM (SELECT 1);

SELECT 'trust-registry.json' AS title,
  '信任注册表 — 6 条事实 + 5 层衰减规则' AS description,
  'blue' AS color,
  '/file-browser.sql?file_path=memory/evolution/trust-registry.json' AS link
FROM (SELECT 1);

SELECT 'evolution-log.md' AS title,
  '进化日志 — 完整能力变更记录' AS description,
  'orange' AS color,
  '/file-browser.sql?file_path=memory/evolution/evolution-log.md' AS link
FROM (SELECT 1);

SELECT 'EVOLUTION-PROTOCOL.md' AS title,
  '进化协议规范 — FIX/DERIVED/CAPTURED' AS description,
  'purple' AS color,
  '/file-browser.sql?file_path=memory/evolution/EVOLUTION-PROTOCOL.md' AS link
FROM (SELECT 1);

SELECT 'SELF-IMPROVE-PROTOCOL.md' AS title,
  '自举协议 — 自我增强流程' AS description,
  'blue' AS color,
  '/file-browser.sql?file_path=memory/evolution/SELF-IMPROVE-PROTOCOL.md' AS link
FROM (SELECT 1);

SELECT 'skill-evolution.md' AS title,
  'Skill 自进化追踪' AS description,
  'green' AS color,
  '/file-browser.sql?file_path=memory/evolution/skill-evolution.md' AS link
FROM (SELECT 1);
