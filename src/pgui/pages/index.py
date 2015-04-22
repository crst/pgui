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
    login = Html()
    login.add_text('<!DOCTYPE html>')
    login.html().head().title('pgui - Login').close()
    login.link(href='static/lib/bootstrap/bootstrap-3.3.4-dist/css/bootstrap.css', rel='stylesheet')
    login.link(href='static/login.css', rel='stylesheet')
    login.close()
    login.body()

    login.div(cls='container')
    login.form(method='POST', cls='login')
    login.h2('Connect to a database', cls='login-header').close()

    login.label('User name', fr='name', cls='sr-only').close()
    login.input(tpe='input', id='name', name='name', cls='form-control', placeholder='User name')

    login.label('Password', fr='password', cls='sr-only').close()
    login.input(tpe='password', id='password', name='password', cls='form-control', placeholder='Password')

    login.label('Host', fr='host', cls='sr-only').close()
    login.input(tpe='input', id='host', name='host', cls='form-control', value='localhost')

    login.label('Port', fr='port', cls='sr-only').close()
    login.input(tpe='input', id='port', name='port', cls='form-control', value='5432')

    login.button('Connect', cls='btn btn-lg btn-success btn-block', tpe='submit').close()
    login.close('form')
    login.close('div')


    login.close('body').close()

    return login


def handle_params(params):
    if 'database' in params:
        current_user.set_database(escape(params['database']))


def Index(params=None):
    handle_params(params)
    index = Html()

    # Header
    index.add_html(Header(title='Index'))
    index.add_html(Navigation(page='index'))
    index.div(cls='container-fluid')

    with pg_connection(*current_user.get_config()) as (c, e):
        c.execute(query('list-databases'))
        data = c.fetchall()

    index.div(cls='row').div(cls='col-md-2')
    index.div(cls='btn-group')
    index.button('Switch database', cls='btn btn-default dropdown-toggle', data_toggle='dropdown', aria_expanded='false').close()
    index.ul(cls='dropdown-menu', role='menu')
    for i, d in enumerate(data):
        index.li().a(d[0], href='index?database=%s' % d[0]).close().close()
        if i < len(data) - 1:
            index.li(cls='divider').close()
    index.close()
    index.close()
    index.close()

    index.div(cls='col-md-10')
    index.add_text('Current database: %s' % current_user.database)
    index.close()

    index.close()

    # Pages
    cols = 12
    col_size = 4
    col = 0
    for page in PAGES[1:]:
        if col == 0:
            index.div(cls='row')

        index.div(cls='col-md-%s' % col_size)
        index.a(href='/%s' % page['name'])
        index.div(cls='page-link')
        index.span(cls='page-icon glyphicon glyphicon-%s' % page['icon']).close()
        index.h3(page['caption']).close()
        index.add_text(page['desc'])
        index.close()
        index.close('a')
        index.close('div')

        col = (col + col_size) % cols
        if col == 0:
            index.close()

    # Footer
    index.close()
    index.add_html(Footer())

    return index
