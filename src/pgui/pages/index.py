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

    login.label('Database', fr='database', cls='sr-only').close()
    login.input(tpe='input', id='database', name='database', cls='form-control', placeholder='Database')

    login.label('Host', fr='host', cls='sr-only').close()
    login.input(tpe='input', id='host', name='host', cls='form-control', value='localhost')

    login.label('Port', fr='port', cls='sr-only').close()
    login.input(tpe='input', id='port', name='port', cls='form-control', value='5432')

    login.button('Connect', cls='btn btn-lg btn-success btn-block', tpe='submit').close()
    login.close('form')
    login.close('div')


    login.close('body').close()

    return login


def Index(params=None):
    index = Html()

    # Header
    index.add_html(Header(title='Index'))
    index.add_html(Navigation(page='index'))
    index.div(cls='container-fluid')

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
