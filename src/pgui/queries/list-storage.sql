
SELECT
  t.schemaname,
  t.tablename,
  pg_total_relation_size(quote_ident(t.schemaname) || '.' || quote_ident(t.tablename)) / 1024 / 1024  AS schema_size,
  nt.num_tuples :: BIGINT
FROM pg_tables t
JOIN (
  SELECT
   n.nspname AS schemaname,
   relname   AS tablename,
   reltuples AS num_tuples
  FROM pg_class c
  JOIN pg_namespace n ON c.relnamespace = n.oid
) nt ON nt.schemaname = t.schemaname AND nt.tablename = t.tablename
WHERE t.schemaname <> 'information_schema' AND t.schemaname NOT LIKE 'pg_%'
ORDER BY schema_size DESC;
