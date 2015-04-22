
SELECT
 datname
FROM pg_database
WHERE NOT datistemplate;
