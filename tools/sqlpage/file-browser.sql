-- ============================================
-- 文件浏览器 — 导航 + 阅读
-- ============================================
SELECT 'shell' AS component,
  '文件浏览器' AS title,
  'files' AS icon,
  '[{"title":"首页","link":"/index.sql","icon":"home"},{"title":"搜索","link":"/content-search.sql","icon":"search"}]' AS menu_item;

SET dir = COALESCE($dir, '');
SET fp = COALESCE($file_path, '');

-- File Reader — Markdown rendering
SELECT 'title' AS component, $file_path AS contents, 2 AS level
WHERE $file_path IS NOT NULL AND $file_path != '';

SELECT 'text' AS component,
  sqlpage.read_file_as_text('/data/clean/' || $file_path) AS contents_md
WHERE $file_path IS NOT NULL AND $file_path != '';

-- File Picker
SELECT 'title' AS component, '打开文件' AS contents, 2 AS level;

SELECT 'form' AS component, '输入完整路径' AS title;
SELECT 'file_path' AS name, '如 MEMORY.md 或 memory/topics/preferences.md' AS placeholder, $file_path AS value, '' AS type;

-- ============================================
-- File Index
-- ============================================

-- Config files
SELECT 'list' AS component, '核心配置' AS title;

SELECT 'MEMORY.md' AS title, 'L1 记忆索引' AS description, 'green' AS color, '?file_path=MEMORY.md' AS link FROM (SELECT 1);
SELECT 'AGENTS.md' AS title, '会话引导 + v5 架构' AS description, 'blue' AS color, '?file_path=AGENTS.md' AS link FROM (SELECT 1);
SELECT 'AGENTS-DETAILS.md' AS title, '详细规则' AS description, 'blue' AS color, '?file_path=AGENTS-DETAILS.md' AS link FROM (SELECT 1);
SELECT 'RULES.md' AS title, '硬约束 + RuleMaturity' AS description, 'orange' AS color, '?file_path=RULES.md' AS link FROM (SELECT 1);
SELECT 'SOUL.md' AS title, '人格+安全红线' AS description, 'purple' AS color, '?file_path=SOUL.md' AS link FROM (SELECT 1);
SELECT 'HEARTBEAT.md' AS title, '心跳 + 主动智能' AS description, 'green' AS color, '?file_path=HEARTBEAT.md' AS link FROM (SELECT 1);
SELECT 'TOOLS.md' AS title, '工具箱速查' AS description, 'blue' AS color, '?file_path=TOOLS.md' AS link FROM (SELECT 1);
SELECT 'CONTEXT.md' AS title, '术语表' AS description, 'blue' AS color, '?file_path=CONTEXT.md' AS link FROM (SELECT 1);

-- memory/topics/
SELECT 'list' AS component, '知识主题 (memory/topics/)' AS title;

SELECT 'preferences.md' AS title, '用户偏好' AS description, 'green' AS color, '?file_path=memory/topics/preferences.md' AS link FROM (SELECT 1);
SELECT 'learnings.md' AS title, '技术学习笔记' AS description, 'blue' AS color, '?file_path=memory/topics/learnings.md' AS link FROM (SELECT 1);
SELECT 'decisions.md' AS title, '架构决策记录' AS description, 'purple' AS color, '?file_path=memory/topics/decisions.md' AS link FROM (SELECT 1);
SELECT 'projects.md' AS title, '项目索引' AS description, 'orange' AS color, '?file_path=memory/topics/projects.md' AS link FROM (SELECT 1);
SELECT 'work-tools.md' AS title, '工具链' AS description, 'blue' AS color, '?file_path=memory/topics/work-tools.md' AS link FROM (SELECT 1);
SELECT 'people.md' AS title, '人际关系' AS description, 'green' AS color, '?file_path=memory/topics/people.md' AS link FROM (SELECT 1);
SELECT 'github-may-2026-projects.md' AS title, 'GitHub 5月热门项目' AS description, 'blue' AS color, '?file_path=memory/topics/github-may-2026-projects.md' AS link FROM (SELECT 1);
SELECT 'openspec-analysis.md' AS title, 'OpenSpec 分析' AS description, 'purple' AS color, '?file_path=memory/topics/openspec-analysis.md' AS link FROM (SELECT 1);
SELECT 'openspec-arch-enhancements.md' AS title, '架构增强' AS description, 'orange' AS color, '?file_path=memory/topics/openspec-arch-enhancements.md' AS link FROM (SELECT 1);

-- memory/evolution/
SELECT 'list' AS component, '进化引擎 (memory/evolution/)' AS title;

SELECT 'EVOLUTION-PROTOCOL.md' AS title, '进化协议' AS description, 'purple' AS color, '?file_path=memory/evolution/EVOLUTION-PROTOCOL.md' AS link FROM (SELECT 1);
SELECT 'SELF-IMPROVE-PROTOCOL.md' AS title, '自举协议' AS description, 'blue' AS color, '?file_path=memory/evolution/SELF-IMPROVE-PROTOCOL.md' AS link FROM (SELECT 1);
SELECT 'skill-evolution.md' AS title, 'Skill 自进化追踪' AS description, 'green' AS color, '?file_path=memory/evolution/skill-evolution.md' AS link FROM (SELECT 1);
SELECT 'evolution-log.md' AS title, '进化日志' AS description, 'orange' AS color, '?file_path=memory/evolution/evolution-log.md' AS link FROM (SELECT 1);
SELECT 'SELF-EVOLUTION-SUMMARY.md' AS title, '自进化摘要' AS description, 'green' AS color, '?file_path=memory/evolution/SELF-EVOLUTION-SUMMARY.md' AS link FROM (SELECT 1);
SELECT 'skill-candidates.md' AS title, 'Skill 候选池' AS description, 'blue' AS color, '?file_path=memory/evolution/skill-candidates.md' AS link FROM (SELECT 1);

-- hooks/
SELECT 'list' AS component, '钩子系统 (hooks/)' AS title;

SELECT 'hooks.yaml' AS title, 'v3 主配置' AS description, 'blue' AS color, '?file_path=hooks/hooks.yaml' AS link FROM (SELECT 1);
SELECT 'laziness-detectors.yaml' AS title, '7种惰性检测器' AS description, 'green' AS color, '?file_path=hooks/laziness-detectors.yaml' AS link FROM (SELECT 1);
SELECT 'task-loop.md' AS title, '长任务循环' AS description, 'purple' AS color, '?file_path=hooks/task-loop.md' AS link FROM (SELECT 1);

-- workflows/
SELECT 'list' AS component, '工作流 (workflows/)' AS title;

SELECT 'daily-social-content.md' AS title, '每日社交内容' AS description, 'blue' AS color, '?file_path=workflows/daily-social-content.md' AS link FROM (SELECT 1);
SELECT 'multi-platform-publish.yaml' AS title, '多平台发布' AS description, 'orange' AS color, '?file_path=workflows/multi-platform-publish.yaml' AS link FROM (SELECT 1);
SELECT 'publish-report.yaml' AS title, '发布报告' AS description, 'green' AS color, '?file_path=workflows/publish-report.yaml' AS link FROM (SELECT 1);
SELECT 'test-and-validate.yaml' AS title, '测试验证' AS description, 'purple' AS color, '?file_path=workflows/test-and-validate.yaml' AS link FROM (SELECT 1);
