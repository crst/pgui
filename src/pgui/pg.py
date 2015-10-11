"""
This should encapsulate all interactions with the database. Connection
parameters are stored as properties of the User object.
"""

from contextlib import contextmanager
import logging
import os
from pkg_resources import resource_string

from flask import flash
import psycopg2
# We do not want psycopg to convert results to Python objects, as we
# generally just pass them to the frontend.
psycopg2.extensions.string_types.clear()

from config import DEFAULT_KEYMAP


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
        yield None, None, err
    else:
        try:
            yield con, cur, None
        finally:
            cur.close()
            con.close()


@contextmanager
def pg_log_err(log_msg=''):
    try:
        yield
    except psycopg2.Error as err:
        logging.error('%s: %s', log_msg, err)


# TODO: Different postgres versions may require different queries. Add
# functionality to automatically select the query that matches with
# the version of the current database connection.
def query(name):
    fn = 'queries/%s.sql' % name
    return resource_string(__name__, fn)


# User object for the flask.ext.login extension.
class User(object):
    # TODO: Using just the name as key is not a good idea, and we
    # probably also shouldn't remember the password here.
    users = {}

    def __init__(self, name, pw, db, host='localhost', port=5432, keymap=DEFAULT_KEYMAP):
        self.name = name
        self.password = pw
        self.database = db
        self.host = host
        self.port = port
        self.keymap = keymap
        self._update_settings()


    def set_database(self, database):
        self.database = database
        self._update_settings()

    def set_keymap(self, keymap):
        self.keymap = keymap
        self._update_settings()

    def _update_settings(self):
        User.users[self.name] = (self.password, self.database, self.host, self.port, self.keymap)

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
