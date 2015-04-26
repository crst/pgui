
SELECT
  s.schema_name                             AS schema_name,
  s.schema_owner                            AS schema_owner,

  COALESCE(storage.schema_size, '0 MB')     AS schema_size,

  COALESCE(t.number_of_tables, 0)           AS number_of_tables,
  COALESCE(t.number_of_views, 0)            AS number_of_views,
  COALESCE(t.number_of_foreign_tables, 0)   AS number_of_foreign_tables,
  COALESCE(t.number_of_temporary_tables, 0) AS number_of_temporary_tables,

  COALESCE(f.number_of_functions, 0)        AS number_of_functions,

  COALESCE(seq.number_of_sequences, 0)      AS number_of_sequences


FROM information_schema.schemata s

LEFT JOIN (
  SELECT
    schemaname,
    pg_size_pretty(sum(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename)))) AS schema_size
  FROM pg_tables
  GROUP BY schemaname
) storage ON s.SCHEMA_NAME = storage.schemaname

LEFT JOIN (
  SELECT
    table_schema,
    SUM(CASE WHEN table_type = 'BASE TABLE' THEN 1 ELSE 0 END) AS number_of_tables,
    SUM(CASE WHEN table_type = 'VIEW' THEN 1 ELSE 0 END) AS number_of_views,
    SUM(CASE WHEN table_type = 'FOREIGN TABLE' THEN 1 ELSE 0 END) AS number_of_foreign_tables,
    SUM(CASE WHEN table_type = 'LOCAL TEMPORARY' THEN 1 ELSE 0 END) AS number_of_temporary_tables
  FROM information_schema.tables
  GROUP BY table_schema
) t ON s.schema_name = t.table_schema

LEFT JOIN (
  SELECT
    specific_schema,
    COUNT(*) AS number_of_functions
  FROM information_schema.routines
  GROUP BY specific_schema
) f ON s.schema_name = f.specific_schema

LEFT JOIN (
  SELECT
    sequence_schema,
    COUNT(*) AS number_of_sequences
  FROM information_schema.sequences
  GROUP BY sequence_schema
) seq ON s.schema_name = seq.sequence_schema

WHERE s.schema_name NOT LIKE 'pg_%' AND s.schema_name <> 'information_schema'
ORDER BY s.schema_name;
