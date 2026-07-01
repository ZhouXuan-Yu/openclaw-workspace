-- Cron 执行日志
SELECT 'shell' AS component,
  'Cron 执行日志' AS title,
  'clock' AS icon,
  '[{"title":"首页","link":"/index.sql","icon":"home"},{"title":"Cron 面板","link":"/cron-dashboard.sql","icon":"clock"}]' AS menu_item;

SELECT 'text' AS component, sqlpage.read_file_as_text('/data/clean/memory/cron-log.md') AS contents_md;
