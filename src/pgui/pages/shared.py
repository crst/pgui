from flask.ext.login import current_user as cu

import pages.index
from page import Html


def Header(params=None, title=None, css=None, js=None):
    h = Html()

    h.add_text('<!DOCTYPE html>')
    h.html().head()
    if title:
        h.title('pgui - %s' % title).x()

    h.meta(charset='utf-8')
    h.script(src='static/lib/jquery/jquery-2.1.3.js').x()
    h.script(src='static/pgui.js').x()
    h.link(href='static/pgui.css', rel='stylesheet')
    h.link(href='static/lib/bootstrap/bootstrap-3.3.4-dist/css/bootstrap.css', rel='stylesheet')
    h.link(href='static/lib/codemirror/codemirror-5.1/lib/codemirror.css', rel='stylesheet')
    h.link(href='static/lib/codemirror/codemirror-5.1/theme/solarized.css', rel='stylesheet')
    h.link(href='static/lib/codemirror/codemirror-5.1/addon/hint/show-hint.css', rel='stylesheet')
    if css:
        for c in css:
            h.link(href=c, rel='stylesheet')
    h.script(src='static/lib/bootstrap/bootstrap-3.3.4-dist/js/bootstrap.js').x()
    h.script(src='static/lib/codemirror/codemirror-5.1/lib/codemirror.js').x()
    h.script(src='static/lib/codemirror/codemirror-5.1/keymap/emacs.js').x()
    h.script(src='static/lib/codemirror/codemirror-5.1/keymap/vim.js').x()
    h.script(src='static/lib/codemirror/codemirror-5.1/keymap/sublime.js').x()
    h.script(src='static/lib/codemirror/codemirror-5.1/mode/sql/sql.js').x()
    h.script(src='static/lib/codemirror/codemirror-5.1/addon/hint/show-hint.js').x()
    if js:
        for j in js:
            h.script(src=j).x()

    h.x('head').body()
    config = 'PGUI.user = "%s"; PGUI.db = "%s"; PGUI.host = "%s";' % (cu.name, cu.database, cu.host)
    h.script().add_text(config).x()
    return h


def Navigation(params=None, page=None):
    h = Html()

    h.nav(cls='navbar navbar-default')
    h.div(cls='container-fluid')
    h.div(cls='navbar-header')
    h.button(tpe='button', cls='navbar-toggle collapsed',
               data_toggle='collapse', data_target='#navbar',
               aria_expanded='false', aria_controls='navbar')
    h.span('Toggle navigation', cls='sr-only').x()
    h.span(cls='icon-bar').x()
    h.span(cls='icon-bar').x()
    h.span(cls='icon-bar').x()
    h.x()

    h.a('pgui', cls='navbar-brand', href='/').x()
    h.x()

    h.div(id='navbar', cls='navbar-collapse collapse')
    h.ul(cls='nav navbar-nav')
    for i, page in enumerate(pages.index.PAGES, 1):
        active = page['name'] == page and 'active' or ''
        h.li(cls=active).a(id='page-%s' % i, href='/%s' % page['name'])
        h.span(cls='glyphicon glyphicon-%s' % page['icon']).x()
        h.add_text(' %s' % page['name'].title())
        h.x().x()
    h.x()

    h.ul(cls='nav navbar-nav navbar-right')
    h.li().a(href='/logout')
    h.span(cls='glyphicon glyphicon-log-out').x()
    h.add_text(' Logout')
    h.x('a').x('li').x('ul')

    h.x()
    h.x()
    h.x()

    return h


def Footer(params=None):
    h = Html()
    h.x('body').x('html')
    return h
