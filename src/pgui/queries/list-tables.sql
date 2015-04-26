
CREATE OR REPLACE FUNCTION col_size(schema_name TEXT, table_name TEXT, column_name TEXT)
  RETURNS TEXT AS
$$
DECLARE
  r TEXT;
BEGIN
  EXECUTE 'SELECT pg_size_pretty(sum(pg_column_size(''' || column_name || ''')))
             FROM ' || quote_ident(schema_name) || '.' || quote_ident(table_name) INTO r;
  RETURN r;
END
$$
LANGUAGE 'plpgsql' IMMUTABLE;


SELECT
  table_schema                                                      AS table_schema,
  table_name                                                        AS table_name,
  array_agg(column_name :: TEXT)                                    AS column_names,
  array_agg(data_type :: TEXT)                                      AS column_types,
  array_agg(column_default :: TEXT)                                 AS column_defaults,
  array_agg(is_nullable :: TEXT)                                    AS column_is_nullable,
--  array_agg(col_size(table_schema, table_name, column_name))        AS column_size,
  pg_size_pretty(
    pg_table_size(
      quote_ident(table_schema) || '.' || quote_ident(table_name))) AS table_size

FROM information_schema.columns
WHERE table_schema NOT LIKE 'pg_%' AND table_schema <> 'information_schema'
GROUP BY table_schema, table_name
ORDER BY table_schema, table_name;
