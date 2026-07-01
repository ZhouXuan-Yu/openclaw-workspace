-- ============================================
-- 全文记忆搜索 — 关键词 + 上下文 + 分页
-- ============================================
SELECT 'shell' AS component,
  '全文记忆搜索' AS title,
  'search' AS icon,
  '[{"title":"首页","link":"/index.sql","icon":"home"},{"title":"文件浏览器","link":"/file-browser.sql","icon":"files"}]' AS menu_item;

SET search_query = COALESCE($q, '');
SET page = CAST(COALESCE($p, '1') AS INTEGER);
SET per_page = 20;
SET offset = ($page - 1) * $per_page;

-- ============================================
-- Search Form
-- ============================================
SELECT 'form' AS component, '搜索记忆内容' AS title, '' AS action;
SELECT 'q' AS name, '关键词...' AS placeholder, $q AS value, '' AS autocomplete;
SELECT 'p' AS name, '' AS type, '1' AS value;

-- ============================================
-- Results
-- ============================================
SELECT 'title' AS component,
  '搜索结果: "' || $q || '" — ' ||
  CAST((SELECT COUNT(*) FROM chunks WHERE $q IS NOT NULL AND $q != '' AND text LIKE '%' || $q || '%') AS TEXT) ||
  ' 条匹配' AS contents,
  2 AS level
WHERE $q IS NOT NULL AND $q != '';

-- Paginated results
SELECT 'table' AS component, '搜索结果' AS title, TRUE AS sort, TRUE AS search
WHERE $q IS NOT NULL AND $q != '';

SELECT
  path AS "来源文件",
  start_line || '-' || end_line AS "行号",
  substr(text, 1, 250) || CASE WHEN length(text) > 250 THEN '...' ELSE '' END AS "内容预览",
  datetime(updated_at / 1000, 'unixepoch', 'localtime') AS "更新时间"
FROM chunks
WHERE $q IS NOT NULL AND $q != ''
  AND text LIKE '%' || $q || '%'
ORDER BY updated_at DESC
LIMIT $per_page
OFFSET $offset;

-- ============================================
-- Pagination
-- ============================================
SELECT 'list' AS component, '分页' AS title,
  '(第 ' || $page || ' 页)' AS description
WHERE $q IS NOT NULL AND $q != '';

SELECT '下一页 →' AS title,
  '?q=' || $q || '&p=' || CAST($page + 1 AS TEXT) AS link,
  'green' AS color
FROM (SELECT 1)
WHERE (
  SELECT COUNT(*) FROM chunks WHERE $q IS NOT NULL AND $q != '' AND text LIKE '%' || $q || '%'
) > ($page * $per_page);

SELECT '← 上一页' AS title,
  '?q=' || $q || '&p=' || CAST($page - 1 AS TEXT) AS link,
  'blue' AS color
FROM (SELECT 1)
WHERE $page > 1 AND $q IS NOT NULL AND $q != '';

-- ============================================
-- No query: show index
-- ============================================
SELECT 'title' AS component, '🔍 输入关键词搜索所有记忆片段' AS contents, 2 AS level
WHERE $q IS NULL OR $q = '';

SELECT 'hero' AS component,
  '记忆搜索引擎' AS title,
  '查询 bge-m3:latest · 1024d 向量索引中的 629 个记忆片段。支持中文关键词搜索。' AS description
WHERE $q IS NULL OR $q = '';

-- Chunk density chart
SELECT 'chart' AS component, '文件 Chunk 密度' AS title, 'bar' AS type
WHERE $q IS NULL OR $q = '';

SELECT
  path AS x,
  COUNT(*) AS y
FROM chunks
GROUP BY path
ORDER BY y DESC
LIMIT 15;
