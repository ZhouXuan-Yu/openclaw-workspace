-- 记忆片段全文搜索
SELECT
  'shell' AS component,
  '记忆搜索引擎' AS title,
  'search' AS icon,
  '[{"title":"首页","link":"/index.sql","icon":"home"}]' AS menu_item;

SELECT
  'form' AS component,
  'Search Memory' AS title;
SELECT
  'q' AS name,
  '关键词...' AS placeholder,
  '' AS value,
  'search' AS type;

-- 关键词搜索
SELECT
  'table' AS component,
  '搜索结果' AS title;

WITH search AS (
  SELECT $q AS query_text
)
SELECT
  path AS "文件",
  start_line AS "起始行",
  end_line AS "结束行",
  substr(text, 1, 200) AS "匹配内容",
  datetime(updated_at / 1000, 'unixepoch', 'localtime') AS "更新时间"
FROM chunks, search
WHERE search.query_text IS NOT NULL
  AND search.query_text != ''
  AND text LIKE '%' || search.query_text || '%'
ORDER BY updated_at DESC
LIMIT 50;

-- 无关键词时显示热力图
SELECT
  'title' AS component,
  '🔍 输入关键词搜索记忆内容' AS contents
WHERE $q IS NULL OR $q = '';

SELECT
  'title' AS component,
  '📊 热门文件 (chunks 数量排名)' AS contents, 2 AS level
WHERE $q IS NULL OR $q = '';

SELECT
  'chart' AS component,
  '文件 Chunk 分布' AS title,
  'bar' AS type
WHERE $q IS NULL OR $q = '';

SELECT
  path AS x,
  COUNT(*) AS y
FROM chunks
WHERE $q IS NULL OR $q = ''
GROUP BY path
ORDER BY y DESC
LIMIT 15;
