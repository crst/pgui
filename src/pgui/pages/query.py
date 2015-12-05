import json
import time

from page import Page
from pages.index import handle_params
from pages.shared import Header, Navigation, Footer
from pg import pg_connection

from flask import Blueprint, request
from flask.ext.login import current_user, login_required
import psycopg2


query_page = Blueprint('query', __name__)

@query_page.route('/query')
@login_required
def query_view():
    return Query(request.args).render()


def Query(params=None):
    handle_params(params)
    p = Page()

    # Header
    p.add_page(Header(title='Query',
                      js=['static/pages/query.js',
                          'static/pages/query_completion.js',
                          'static/pages/keywords.js',
                          'static/lib/springy/springy.js',
                          'static/lib/springy/springyui.js'],
                      css=['static/pages/query.css']))
    with p.script():
        p.content('PGUI.QUERY.keymap = "%s";' % current_user.keymap)
    p.add_page(Navigation(page='query'))

    with p.div({'class': 'container-fluid'}):
        # Modal dialog for displaying previous queries
        with p.div({'class': 'modal fade', 'id': 'query-history-dialog', 'tabindex': '-1', 'role': 'dialog', 'aria-labelledby': 'Query History'}):
            with p.div({'class': 'modal-dialog', 'role': 'document'}):
                with p.div({'class': 'modal-content'}):
                    with p.div({'class': 'modal-header'}):
                        with p.button({'type': 'button', 'class': 'close', 'data-dismiss': 'modal', 'aria-label': 'Close'}):
                            with p.span({'aria-hidden': 'true'}):
                                p.content('&times;')
                        with p.h4({'class': 'modal-title', 'id': 'query-history-label'}):
                            p.content('Query history')

                    with p.div({'clas': 'modal-body'}):
                        with p.div({'id': 'query-history'}): pass

        # Tab bar controls
        with p.div({'id': 'query-panel', 'role': 'tabpanel'}):
            with p.ul({'id': 'query-nav-tabs', 'class': 'nav nav-tabs', 'role': 'tablist'}):
                with p.li({'role': 'presentation'}):
                    with p.a({'id': 'show-query-history', 'href': 'javascript:void(0);'}):
                        with p.span({'class': 'add-tab glyphicon glyphicon-camera', 'aria-hidden': 'true'}): pass
                with p.li({'role': 'presentation'}):
                    with p.a({'id': 'add-tab', 'href': 'javascript:void(0);'}):
                        with p.span({'class': 'add-tab glyphicon glyphicon-plus', 'aria-hidden': 'true'}): pass
            # Tab bar contents
            with p.div({'id': 'query-tab-panes', 'class': 'tab-content'}): pass

    # Footer
    p.add_page(Footer())

    return p


@query_page.route('/query/run-query', methods=['POST'])
@login_required
def run_query():
    with pg_connection(*current_user.get_config()) as (con, cur, err):
        if err:
            return json.dumps({'success': False,
                               'error-msg': str(err)})
        warning = None
        try:
            t1 = time.time()
            cur.execute(request.form['query'])
            columns = [desc[0] for desc in cur.description]
            t2 = time.time()
            data = cur.fetchall()
            t3 = time.time()
        except psycopg2.Warning as warn:
            # TODO: display
            warning = str(warn)
        except psycopg2.Error as err:
            return json.dumps({'success': False, 'error-msg': err.pgerror})
        except Exception as err:
            # TODO: Display errors only in dev mode?
            return json.dumps({'success': False, 'error-msg': str(err)})

    return json.dumps({'success': True,
                       'warning': warning,
                       'columns': columns,
                       'data': data,
                       'execution-time': (t2 - t1),
                       'fetching-time': (t3 - t2)})


@query_page.route('/query/run-explain', methods=['POST'])
@login_required
def run_explain():
    with pg_connection(*current_user.get_config()) as (con, cur, err):
        if err:
            return json.dumps({'success': False,
                               'error-msg': str(err)})
        warning = None
        try:
            query = 'EXPLAIN (format json) %s' % request.form['query']
            cur.execute(query)
            data = cur.fetchall()
            plan = json.loads(data[0][0])
        except psycopg2.Warning as warn:
            # TODO: display
            warning = str(warn)
        except psycopg2.Error as err:
            return json.dumps({'success': False, 'error-msg': err.pgerror})
        except Exception as err:
            return json.dumps({'success': False, 'error-msg': str(err)})

    return json.dumps({'success': True, 'warning': warning, 'data': plan})
