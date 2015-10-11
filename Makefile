
.PHONY:	create-test-data

create-test-data:
	echo 'DROP DATABASE IF EXISTS pgui_test_data' | psql postgres
	echo 'CREATE DATABASE pgui_test_data' | psql postgres
	cat dev/create_pgui_test_data.sql | psql pgui_test_data
