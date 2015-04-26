
CREATE OR REPLACE FUNCTION pg_temp.col_size(schema_name TEXT, table_name TEXT, column_name TEXT)
  RETURNS TEXT AS $$
DECLARE
  r TEXT;
BEGIN
  EXECUTE 'SELECT pg_size_pretty(sum(pg_column_size(''' || column_name || ''')))
             FROM ' || quote_ident(schema_name) || '.' || quote_ident(table_name) INTO r;
  RETURN r;
END
$$ LANGUAGE 'plpgsql' IMMUTABLE;


SELECT
  column_name,
  pg_temp.col_size(table_schema, table_name, column_name)
FROM information_schema.columns
WHERE table_schema = %(table-schema)s AND table_name = %(table-name)s
ORDER BY ordinal_position;
