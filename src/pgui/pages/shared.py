from flask.ext.login import current_user as cu

import pages.index
from page import Page


def Header(params=None, title=None, css=None, js=None):
    p = Page()

    p.content('<!DOCTYPE html>')
    with p.html(close=False):
        with p.head():
            with p.title():
                p.content('pgui - %s/%s' % (cu.database, title))

            with p.meta({'charset': 'utf-8'}): pass
            with p.script({'src': 'static/lib/jquery/jquery-2.1.3.js'}): pass
            with p.script({'src': 'static/pgui.js'}): pass
            with p.link({'href': 'static/pgui.css', 'rel': 'stylesheet'}): pass
            with p.link({'href': 'static/lib/bootstrap/bootstrap-3.3.4-dist/css/bootstrap.css', 'rel': 'stylesheet'}): pass
            with p.link({'href': 'static/lib/codemirror/codemirror-5.1/lib/codemirror.css', 'rel': 'stylesheet'}): pass
            with p.link({'href': 'static/lib/codemirror/codemirror-5.1/theme/neo.css', 'rel': 'stylesheet'}): pass
            with p.link({'href': 'static/lib/codemirror/codemirror-5.1/addon/hint/show-hint.css', 'rel': 'stylesheet'}): pass
            if css:
                for c in css:
                    with p.link({'href': c, 'rel': 'stylesheet'}): pass
            with p.script({'src': 'static/lib/bootstrap/bootstrap-3.3.4-dist/js/bootstrap.js'}): pass
            with p.script({'src': 'static/lib/codemirror/codemirror-5.1/lib/codemirror.js'}): pass
            with p.script({'src': 'static/lib/codemirror/codemirror-5.1/keymap/emacs.js'}): pass
            with p.script({'src': 'static/lib/codemirror/codemirror-5.1/keymap/vim.js'}): pass
            with p.script({'src': 'static/lib/codemirror/codemirror-5.1/keymap/sublime.js'}): pass
            with p.script({'src': 'static/lib/codemirror/codemirror-5.1/mode/sql/sql.js'}): pass
            with p.script({'src': 'static/lib/codemirror/codemirror-5.1/addon/hint/show-hint.js'}): pass
            if js:
                for j in js:
                    with p.script({'src': j}): pass

        with p.body(close=False):
            config = 'PGUI.user = "%s"; PGUI.db = "%s"; PGUI.host = "%s";' % (cu.name, cu.database, cu.host)
            with p.script():
                p.content(config)

    return p


def Navigation(params=None, page=None):
    p = Page()

    with p.nav({'class': 'navbar navbar-default'}):
        with p.div({'class': 'container-fluid'}):
            with p.div({'class': 'navbar-header'}):
                with p.button({'type': 'button',
                               'class': 'navbar-toggle collapsed',
                               'data-toggle': 'collapse',
                               'data-target': '#navbar',
                               'aria-expanded': 'false',
                               'aria-controls': 'navbar'}):
                    with p.span({'class': 'sr-only'}):
                        p.content('Toggle navigation')
                    with p.span({'class': 'icon-bar'}): pass
                    with p.span({'class': 'icon-bar'}): pass
                    with p.span({'class': 'icon-bar'}): pass

                with p.a({'class': 'navbar-brand', 'href': '/'}):
                    p.content('pgui')

            with p.div({'id': 'navbar', 'class': 'navbar-collapse collapse'}):
                with p.ul({'class': 'nav navbar-nav'}):
                    for i, page in enumerate(pages.index.PAGES, 1):
                        active = page['name'] == page and 'active' or ''
                        with p.li({'class': active}):
                            with p.a({'id': 'page-%s' % i, 'href': '/%s' % page['name']}):
                                with p.span({'class': 'glyphicon glyphicon-%s' % page['icon']}): pass
                                p.content(' %s' % page['name'].title())

                with p.ul({'class': 'nav navbar-nav navbar-right'}):
                    with p.li():
                        with p.a({'href': '/logout'}):
                            with p.span({'class': 'glyphicon glyphicon-log-out'}):
                                p.content(' Logout')

    return p


def Footer(params=None):
    p = Page()
    p.close('body').close('html')
    return p
