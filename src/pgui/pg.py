from contextlib import contextmanager
import os
from pkg_resources import resource_string

import psycopg2
psycopg2.extensions.string_types.clear()


@contextmanager
def pg_connection(user, password=None, db='postgres', host='localhost', port=5432):
    try:
        con = psycopg2.connect(user=user,
                               password=password,
                               database=db,
                               host=host,
                               port=port)
        cur = con.cursor()
    except psycopg2.Error as err:
        yield None, err
    else:
        try:
            yield cur, None
        finally:
            cur.close()
            con.close()


def query(name):
    fn = 'queries/%s.sql' % name
    return resource_string(__name__, fn)


class User(object):
    users = {}

    def __init__(self, name, pw, db, host='localhost', port=5432):
        self.name = name
        self.password = pw
        self.database = db
        self.host = host
        self.port = port
        self._update_settings()

    def set_database(self, database):
        self.database = database
        self._update_settings()

    def _update_settings(self):
        User.users[self.name] = (self.password, self.database, self.host, self.port)

    def get_config(self):
        return (self.name, self.password, self.database, self.host, self.port)

    def is_authenticated(self):
        try:
            con = psycopg2.connect(user=self.name,
                                   password=self.password,
                                   database=self.database,
                                   host=self.host,
                                   port=self.port)
            con.close()
        except psycopg2.Error as err:
            flash(str(err))
            return False

        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name
