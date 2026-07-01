-- ============================================
-- Cron 仪表盘 — 任务状态 + 健康检查
-- ============================================
SELECT 'shell' AS component,
  'Cron 仪表盘' AS title,
  'clock' AS icon,
  '[{"title":"首页","link":"/index.sql","icon":"home"},{"title":"执行日志","link":"/cron-log.sql","icon":"list-check"}]' AS menu_item;

-- ============================================
-- Summary Cards
-- ============================================
SELECT 'card' AS component, 4 AS columns;

SELECT '活跃任务' AS title,
  '14' AS description,
  '12 OK · 2 ERROR' AS footer,
  'green' AS color, 'clock-check' AS icon
FROM (SELECT 1);

SELECT 'ISO 时间' AS title,
  'cron 0 23 * * *' AS description,
  '每日 23:00 记忆反射' AS footer,
  'blue' AS color, 'calendar' AS icon
FROM (SELECT 1);

SELECT 'memory-health-sync' AS title,
  '每日 02:15' AS description,
  '健康度同步' AS footer,
  'purple' AS color, 'heartbeat' AS icon
FROM (SELECT 1);

SELECT 'security-check' AS title,
  '每日 10:00' AS description,
  '⚠️ 上次 ERROR' AS footer,
  'red' AS color, 'shield-x' AS icon
FROM (SELECT 1);

-- ============================================
-- Cron Tasks Table
-- ============================================
SELECT 'title' AS component, '全部 Cron 任务' AS contents, 2 AS level;

SELECT 'table' AS component, 'Cron Tasks' AS title, TRUE AS sort;

SELECT
  'content-evolution' AS "任务",
  'cron 0 23 * * *' AS "调度",
  'OK' AS "状态"
FROM (SELECT 1)
UNION ALL
SELECT 'daily-social-content', 'cron 0 23 * * *', 'ERROR ⚠️' FROM (SELECT 1)
UNION ALL
SELECT 'memory-reflection', 'cron 30 23 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'daily-obsidian-update', 'cron 0 0 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'memory-consolidation', 'cron 0 2 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'memory-health-sync', 'cron 15 2 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'Memory Dreaming Promotion', 'cron 0 3 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'memory-patrol', 'cron 0 9 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'younavi-meeting-sync', 'cron 0 9 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'security-check', 'cron 0 10 * * *', 'ERROR ⚠️' FROM (SELECT 1)
UNION ALL
SELECT 'github-key-scan-daily', 'cron 0 12 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'daily-report-reminder', 'cron 30 17 * * *', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'openclaw-update-check', 'cron 0 10 * * 1', 'OK' FROM (SELECT 1)
UNION ALL
SELECT 'younavi-weekly-research', 'cron 0 9 * * 0', 'ERROR ⚠️' FROM (SELECT 1);

-- ============================================
-- Memory Health
-- ============================================
SELECT 'title' AS component, '记忆系统健康度' AS contents, 2 AS level;

SELECT 'list' AS component, 'Health Checks' AS title;

SELECT '记忆索引' AS title,
  '96 文件 / 629 chunks — 正常' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT '嵌入模型' AS title,
  'bge-m3:latest · 1024d — 正常' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT 'Chunk/File 比' AS title,
  '629/96 = 6.6 chunks per file — 健康' AS description,
  'green' AS color
FROM (SELECT 1);

SELECT 'WinDefend' AS title,
  '已停止 — ⚠️ 请核查安全软件' AS description,
  'red' AS color
FROM (SELECT 1);
