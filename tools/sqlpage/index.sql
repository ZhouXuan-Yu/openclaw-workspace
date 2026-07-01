-- ============================================
-- OpenClaw System Dashboard — 主入口
-- ============================================
SELECT 'shell' AS component,
  'OpenClaw System Dashboard' AS title,
  'dashboard' AS icon,
  '[{"title":"记忆搜索","link":"/content-search.sql","icon":"search"},{"title":"文件浏览器","link":"/file-browser.sql","icon":"files"},{"title":"Cron 面板","link":"/cron-dashboard.sql","icon":"clock"},{"title":"执行日志","link":"/cron-log.sql","icon":"list-check"},{"title":"进化引擎","link":"/evolution-stats.sql","icon":"trending-up"}]' AS menu_item;

-- ============================================
-- Metrics Cards (clickable)
-- ============================================
SELECT 'card' AS component, 4 AS columns;

SELECT '记忆文档' AS title,
  '96' AS description,
  '96 个索引文件' AS footer,
  'blue' AS color, 'book' AS icon,
  '/file-browser.sql' AS link
FROM (SELECT 1);

SELECT '记忆片段' AS title,
  '629' AS description,
  'bge-m3:latest · 1024d' AS footer,
  'green' AS color, 'puzzle' AS icon,
  '/content-search.sql' AS link
FROM (SELECT 1);

SELECT 'Cron 任务' AS title,
  '12 / 14' AS description,
  '2 个异常' AS footer_md,
  'orange' AS color, 'clock' AS icon,
  '/cron-dashboard.sql' AS link
FROM (SELECT 1);

SELECT '进化引擎' AS title,
  'v5 · 6 能力' AS description,
  'Think+ModeRouter+Verify' AS footer,
  'purple' AS color, 'trending-up' AS icon,
  '/evolution-stats.sql' AS link
FROM (SELECT 1);

-- ============================================
-- Quick Search
-- ============================================
SELECT 'form' AS component, '快速搜索记忆' AS title, '/content-search.sql' AS action;
SELECT 'q' AS name, '输入关键词搜索所有记忆内容...' AS placeholder, '' AS value, '' AS type;

-- ============================================
-- Recent Activity (from DB)
-- ============================================
SELECT 'title' AS component, '最近活跃文件' AS contents, 2 AS level;

SELECT 'table' AS component, 'Recent' AS title, TRUE AS sort, TRUE AS search;
SELECT
  path AS "文件路径",
  printf('%.1f KB', size / 1024.0) AS "大小",
  datetime(mtime / 1000, 'unixepoch', 'localtime') AS "修改时间"
FROM files
ORDER BY mtime DESC
LIMIT 12;

-- ============================================
-- Core Config Files
-- ============================================
SELECT 'title' AS component, '核心配置' AS contents, 2 AS level;

SELECT 'list' AS component, 'Core Files' AS title;

SELECT 'MEMORY.md' AS title,
  'L1 记忆索引 — 星标记忆 + Topic + Tag' AS description,
  'green' AS color,
  '/file-browser.sql?file_path=MEMORY.md' AS link
FROM (SELECT 1);

SELECT 'AGENTS.md' AS title,
  '会话启动引导 — 记忆4层 + v5进化引擎' AS description,
  'blue' AS color,
  '/file-browser.sql?file_path=AGENTS.md' AS link
FROM (SELECT 1);

SELECT 'RULES.md' AS title,
  '硬约束 — must-always/must-never + RuleMaturity' AS description,
  'orange' AS color,
  '/file-browser.sql?file_path=RULES.md' AS link
FROM (SELECT 1);

SELECT 'SOUL.md' AS title,
  '人格定义 + 安全红线' AS description,
  'purple' AS color,
  '/file-browser.sql?file_path=SOUL.md' AS link
FROM (SELECT 1);

-- ============================================
-- Quick Evolution Status
-- ============================================
SELECT 'title' AS component, '能力进化状态' AS contents, 2 AS level;

SELECT 'list' AS component, '已掌握 (PASSED)' AS title;
SELECT '研究分析' AS title, '10次连续成功 · 已通过迁移测试 · 可晋升' AS description, 'green' AS color FROM (SELECT 1);

SELECT 'list' AS component, '应用熟练 (PRACTICED)' AS title;
SELECT 'Skill 自进化' AS title, '13次连续成功 · 接近晋升' AS description, 'green' AS color FROM (SELECT 1);
SELECT '记忆架构管理' AS title, '4层架构 + 智能检索' AS description, 'blue' AS color FROM (SELECT 1);
SELECT '多平台内容发布' AS title, '5平台CLI + 小红书草稿修复' AS description, 'yellow' AS color FROM (SELECT 1);
SELECT '架构进化 v3' AS title, '惰性检测器+长任务循环+RuleMaturity' AS description, 'blue' AS color FROM (SELECT 1);

SELECT 'list' AS component, '新建 (RECORDED)' AS title;
SELECT '惰性检测器' AS title, 'CAPTURED from v3 · 7种检测器 · 待验证' AS description, 'blue' AS color FROM (SELECT 1);
