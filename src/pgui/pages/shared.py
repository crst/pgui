import pages.index
from page import Html


def Header(params=None, title=None, css=None, js=None):
    header = Html()

    header.add_text('<!DOCTYPE html>')
    header.html().head()
    if title:
        header.title('pgui - %s' % title).close()

    header.meta(charset='utf-8')
    header.script(src='static/lib/jquery/jquery-2.1.3.js').close()
    header.script(src='static/pgui.js').close()
    header.link(href='static/pgui.css', rel='stylesheet')
    header.link(href='static/lib/bootstrap/bootstrap-3.3.4-dist/css/bootstrap.css', rel='stylesheet')
    header.link(href='static/lib/codemirror/codemirror-5.1/lib/codemirror.css', rel='stylesheet')
    header.link(href='static/lib/codemirror/codemirror-5.1/addon/hint/show-hint.css', rel='stylesheet')
    if css:
        for c in css:
            header.link(href=c, rel='stylesheet')
    header.script(src='static/lib/bootstrap/bootstrap-3.3.4-dist/js/bootstrap.js').close()
    header.script(src='static/lib/codemirror/codemirror-5.1/lib/codemirror.js').close()
    header.script(src='static/lib/codemirror/codemirror-5.1/keymap/emacs.js').close()
    header.script(src='static/lib/codemirror/codemirror-5.1/keymap/vim.js').close()
    header.script(src='static/lib/codemirror/codemirror-5.1/keymap/sublime.js').close()
    header.script(src='static/lib/codemirror/codemirror-5.1/mode/sql/sql.js').close()
    header.script(src='static/lib/codemirror/codemirror-5.1/addon/hint/show-hint.js').close()
    if js:
        for j in js:
            header.script(src=j).close()

    header.close('head').body()
    return header


def Navigation(params=None, page=None):
    nav = Html()

    nav.nav(cls='navbar navbar-default')
    nav.div(cls='container-fluid')
    nav.div(cls='navbar-header')
    nav.button(tpe='button', cls='navbar-toggle collapsed',
               data_toggle='collapse', data_target='#navbar',
               aria_expanded='false', aria_controls='navbar')
    nav.span('Toggle navigation', cls='sr-only').close()
    nav.span(cls='icon-bar').close()
    nav.span(cls='icon-bar').close()
    nav.span(cls='icon-bar').close()
    nav.close()

    nav.a('pgui', cls='navbar-brand', href='/').close()
    nav.close()

    nav.div(id='navbar', cls='navbar-collapse collapse')
    nav.ul(cls='nav navbar-nav')
    for page in pages.index.PAGES:
        active = page['name'] == page and 'active' or ''
        nav.li(cls=active).a(href='/%s' % page['name'])
        nav.span(cls='glyphicon glyphicon-%s' % page['icon']).close()
        nav.add_text(' %s' % page['name'].title())
        nav.close().close()
    nav.close()

    nav.ul(cls='nav navbar-nav navbar-right')
    nav.li().a(href='/logout')
    nav.span(cls='glyphicon glyphicon-log-out').close()
    nav.add_text(' Logout')
    nav.close('a').close('li').close('ul')

    nav.close()
    nav.close()
    nav.close()

    return nav


def Footer(params=None):
    footer = Html()
    footer.close('body').close('html')
    return footer
