
SELECT
  n.nspname || '.' || c.relname         AS relation_name,
  pg_relation_size(c.oid) / 1024 / 1024 AS relation_size
FROM pg_class c
LEFT JOIN pg_namespace n ON (n.oid = c.relnamespace)
ORDER BY pg_relation_size(c.oid) DESC
LIMIT 10;
