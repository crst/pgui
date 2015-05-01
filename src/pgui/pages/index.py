from flask import escape
from flask.ext.login import current_user

from page import Html
from pages.shared import Header, Navigation, Footer
from pg import pg_connection, query


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
    h = Html()
    h.add_text('<!DOCTYPE html>')
    h.html().head().title('pgui - Login').x()
    h.link(href='static/lib/bootstrap/bootstrap-3.3.4-dist/css/bootstrap.css', rel='stylesheet')
    h.link(href='static/login.css', rel='stylesheet')
    h.x()
    h.body()

    h.div(cls='container')
    h.form(method='POST', cls='login')
    h.h2('Connect to a database', cls='login-header').x()

    h.label('User name', fr='name', cls='sr-only').x()
    h.input(tpe='input', id='name', name='name', cls='form-control', placeholder='User name')

    h.label('Password', fr='password', cls='sr-only').x()
    h.input(tpe='password', id='password', name='password', cls='form-control', placeholder='Password')

    h.label('Host', fr='host', cls='sr-only').x()
    h.input(tpe='input', id='host', name='host', cls='form-control', value='localhost')

    h.label('Port', fr='port', cls='sr-only').x()
    h.input(tpe='input', id='port', name='port', cls='form-control', value='5432')

    h.button('Connect', args=['autofocus'], cls='btn btn-lg btn-success btn-block', tpe='submit').x()
    h.x('form')

    h.div(cls='login')
    if 'err' in params and params['err']:
        for err in params['err']:
            h.code(err).x()
    h.x()

    h.x('div')
    h.x('body').x()

    return h


def handle_params(params):
    if 'database' in params:
        current_user.set_database(escape(params['database']))

    if 'keymap' in params:
        current_user.set_keymap(escape(params['keymap']))


def Index(params=None):
    handle_params(params)
    h = Html()

    # Header
    h.add_html(Header(title='Index'))
    h.add_html(Navigation(page='index'))
    h.div(cls='container-fluid')

    with pg_connection(*current_user.get_config()) as (c, e):
        c.execute(query('list-databases'))
        data = c.fetchall()

    h.div(cls='row').div(cls='col-md-2')
    h.div(cls='btn-group')
    h.button('Switch database', cls='btn btn-default dropdown-toggle', data_toggle='dropdown', aria_expanded='false').x()
    h.ul(cls='dropdown-menu', role='menu')
    for n, d in enumerate(data):
        h.li().a(d[0], href='index?database=%s' % d[0]).x().x()
        if n < len(data) - 1:
            h.li(cls='divider').x()
    h.x()
    h.x()
    h.x()

    h.div(cls='col-md-10')
    h.add_text('Current database: %s' % current_user.database)
    h.x()

    h.x()

    # Pages
    cols = 12
    col_size = 4
    col = 0
    for page in PAGES[1:]:
        if col == 0:
            h.div(cls='row')

        h.div(cls='col-md-%s' % col_size)
        h.a(href='/%s' % page['name'])
        h.div(cls='page-link')
        h.span(cls='page-icon glyphicon glyphicon-%s' % page['icon']).x()
        h.h3(page['caption']).x()
        h.add_text(page['desc'])
        h.x()
        h.x('a')
        h.x('div')

        col = (col + col_size) % cols
        if col == 0:
            h.x()

    # Footer
    h.x()
    h.add_html(Footer())

    return h
