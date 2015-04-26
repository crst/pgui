
SELECT
  table_schema                                                      AS table_schema,
  table_name                                                        AS table_name,
  array_agg(column_name :: TEXT ORDER BY ordinal_position)          AS column_names,
  array_agg(data_type :: TEXT ORDER BY ordinal_position)            AS column_types,
  array_agg(column_default :: TEXT ORDER BY ordinal_position)       AS column_defaults,
  array_agg(is_nullable :: TEXT ORDER BY ordinal_position)          AS column_is_nullable,
  pg_size_pretty(
    pg_table_size(
      quote_ident(table_schema) || '.' || quote_ident(table_name))) AS table_size

FROM information_schema.columns
WHERE table_schema NOT LIKE 'pg_%' AND table_schema <> 'information_schema'
GROUP BY table_schema, table_name
ORDER BY table_schema, table_name;
