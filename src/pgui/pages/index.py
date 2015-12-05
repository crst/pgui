"""
This is the start page for the application and includes all the
different application modules listed in the PAGES variable.

Renders the login page as well as the index page.
"""

from collections import defaultdict

from flask import escape
from flask.ext.login import current_user

from page import Page
from pages.shared import Header, Navigation, Footer
from pg import pg_connection, pg_log_err, query


# Defines all the available modules.
PAGES = [
    {'name': 'index',
     'icon': 'home',
     'caption': '',
     'desc': ''},

    {'name': 'query',
     'icon': 'road',
     'caption': 'Run queries',
     'desc': 'Run queries against the database.'},

    {'name': 'structure',
     'icon': 'lamp',
     'caption': 'View structure',
     'desc': 'Display information about the table structure.'},

    {'name': 'storage',
     'icon': 'scale',
     'caption': 'Monitor storage',
     'desc': 'Display storage size information.'},
]


def Login(params=None, title=None):
    """
    Renders the login page.

    There is no separate login for the application, this is passed to
    the database!
    """
    p = Page()
    p.content('<!DOCTYPE html>')
    with p.html():
        with p.head():
            with p.title():
                p.content('pgui - Login')
            with p.link({'href': 'static/lib/bootstrap/bootstrap-3.3.4-dist/css/bootstrap.css', 'rel': 'stylesheet'}): pass
            with p.link({'href': 'static/login.css', 'rel': 'stylesheet'}): pass

        with p.body():

            with p.div({'class': 'container'}):
                with p.form({'method': 'POST', 'class': 'login'}):
                    with p.h2({'class': 'login-header'}):
                        p.content('Connect to a postgres database server')

                    with p.label({'for': 'name', 'class': 'sr-only'}):
                        p.content('User name')
                    with p.input({'type': 'input', 'id': 'name', 'name': 'name', 'class': 'form-control', 'placeholder': 'User name'}): pass

                    with p.label({'for': 'password', 'class': 'sr-only'}):
                        p.content('Password')
                    with p.input({'type': 'password', 'id': 'password', 'name': 'password', 'class': 'form-control', 'placeholder': 'Password'}): pass

                    with p.label({'for': 'host', 'class': 'sr-only'}):
                        p.control('Host')
                    with p.input({'type': 'input', 'id': 'host', 'name': 'host', 'class': 'form-control', 'value': 'localhost'}): pass

                    with p.label({'for': 'port', 'class': 'sr-only'}):
                        p.content('Port')
                    with p.input({'type': 'input', 'id': 'port', 'name': 'port', 'class': 'form-control', 'value': '5432'}): pass

                    with p.button({'class': 'btn btn-lg btn-success btn-block', 'type': 'submit'}, args=['autofocus']):
                        p.content('Connect')


                with p.div({'class': 'login'}):
                    if 'err' in params and params['err']:
                        for err in params['err']:
                            with p.code():
                                p.content(err)

    return p


def handle_params(params):
    """
    Generic application settings that every module should support as
    GET parameters.
    """
    if 'database' in params:
        current_user.set_database(escape(params['database']))

    if 'keymap' in params:
        current_user.set_keymap(escape(params['keymap']))


def Index(params=None):
    """
    Renders the index page which displays some generic connections
    information and links to all the activated modules.
    """
    handle_params(params)
    p = Page()

    # Header
    p.add_page(Header(title='Index'))
    p.add_page(Navigation(page='index'))

    with p.div({'class': 'container-fluid'}):
        # Connection information
        data, params = [], defaultdict(str)
        param_keys = ('server_version', 'server_encoding', 'client_encoding', 'is_superuser', 'TimeZone')
        with pg_connection(*current_user.get_config()) as (con, cur, err):
            for k in param_keys:
                params[k] = con.get_parameter_status(k)
            with pg_log_err('list databases'):
                cur.execute(query('list-databases'))
                data = cur.fetchall()

        with p.div({'class': 'row'}):
            with p.div({'class': 'col-md-2'}):
                with p.div({'class': 'btn-group'}):
                    with p.button({'class': 'btn btn-default dropdown-toggle', 'data-toggle': 'dropdown', 'aria-expanded': 'false'}):
                        p.content('Switch database <span class="caret"></span>')
                    with p.ul({'class': 'dropdown-menu', 'role': 'menu'}):
                        for n, d in enumerate(data):
                            with p.li():
                                with p.a({'href': 'index?database=%s' % d[0]}):
                                    p.content(d[0])
                            if n < len(data) - 1:
                                with p.li({'class': 'divider'}): pass

            with p.div({'class': 'col-md-4 small'}):
                p.content('<strong>%s</strong>' % current_user.database)
                p.content('<br>%s@%s:%s' % (current_user.name, current_user.host, current_user.port))

            with p.div({'class': 'col-md-6 small'}):
                with p.ul({'class': 'list-inline'}):
                    for k, v in sorted(params.items()):
                        with p.li():
                            p.content('%s: %s' % (k, v))

        with p.hr(): pass

        # Modules
        cols = 12
        col_size = 4
        col = 0
        for page in PAGES[1:]:
            if col == 0:
                with p.div({'class': 'row'}, close=False): pass

            with p.div({'class': 'col-md-%s' % col_size}):
                with p.a({'href': '/%s' % page['name']}):
                    with p.div({'class': 'page-link'}):
                        with p.span({'class': 'page-icon glyphicon glyphicon-%s' % page['icon']}): pass
                        with p.h3():
                            p.content(page['caption'])
                        p.content(page['desc'])

            col = (col + col_size) % cols
            if col == 0:
                p.close('div')

    p.add_page(Footer())

    return p
