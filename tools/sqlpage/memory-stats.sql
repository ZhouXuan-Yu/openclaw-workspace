-- 记忆统计详情
SELECT
  'shell' AS component,
  '记忆文件统计' AS title,
  'chart-bar' AS icon,
  '[{"title":"首页","link":"/index.sql","icon":"home"}]' AS menu_item;

-- 记忆文件大小排名
SELECT
  'title' AS component,
  '📁 记忆文件大小排名' AS contents;

SELECT
  'table' AS component,
  'Top Files' AS title;
SELECT
  path AS "文件路径",
  size AS "大小(字节)",
  printf('%.1f', size / 1024.0) AS "大小(KB)",
  datetime(mtime / 1000, 'unixepoch', 'localtime') AS "最后修改"
FROM files
ORDER BY size DESC
LIMIT 20;

-- 每日记忆增长趋势
SELECT
  'title' AS component,
  '📈 每日记忆增长趋势' AS contents, 2 AS level;

SELECT
  'chart' AS component,
  '每日文件活动' AS title,
  'bar' AS type;
SELECT
  date(datetime(mtime / 1000, 'unixepoch')) AS x,
  COUNT(*) AS y
FROM files
GROUP BY date(datetime(mtime / 1000, 'unixepoch'))
ORDER BY x DESC
LIMIT 30;

-- 来源分布
SELECT
  'chart' AS component,
  '来源分布' AS title,
  'pie' AS type;
SELECT
  source AS label,
  COUNT(*) AS value
FROM chunks
GROUP BY source;

-- 最新 chunk 内容预览
SELECT
  'title' AS component,
  '📝 最新记忆片段' AS contents, 2 AS level;

SELECT
  'table' AS component,
  'Recent Chunks' AS title;
SELECT
  path AS "来源文件",
  start_line || '-' || end_line AS "行",
  substr(text, 1, 120) || '...' AS "内容摘要",
  datetime(updated_at / 1000, 'unixepoch', 'localtime') AS "更新时间"
FROM chunks
ORDER BY updated_at DESC
LIMIT 15;
