
CREATE SCHEMA common;

CREATE TABLE common.years (
  year_id SMALLINT PRIMARY KEY
);

INSERT INTO common.years
  SELECT
    t
  FROM generate_series(1900, 2100, 1) t;

-------------------------------------------------------------------------------

CREATE SCHEMA programming;

CREATE TABLE programming.languages (
  language_id   SMALLSERIAL PRIMARY KEY,
  language_name TEXT,
  language_year SMALLINT
);

INSERT INTO programming.languages (language_name, language_year) VALUES
  ('Basic',      1964),
  ('C',          1972),
  ('Clojure',    2007),
  ('Delphi',     1995),
  ('Erlang',     1986),
  ('Forth',      1970),
  ('Go',         2009),
  ('Haskell',    1990),
  ('JavaScript', 1995),
  ('Lisp',       1958),
  ('ML',         1973),
  ('OCaml',      1996),
  ('Python',     1991),
  ('Racket',     1994),
  ('Scheme',     1975);

ALTER TABLE programming.languages ADD FOREIGN KEY (language_year) REFERENCES common.years (year_id);
