import json
import time

from page import Html
from pages.index import handle_params
from pages.shared import Header, Navigation, Footer
from pg import pg_connection, query

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
    query = Html()

    # Header
    query.add_html(Header(title='Query',
                          js=['static/pages/query.js',
                              'static/pages/query_completion.js',
                              'static/pages/keywords.js',
                              'static/lib/springy/springy.js',
                              'static/lib/springy/springyui.js'],
                          css=['static/pages/query.css']))
    query.script('PGUI.QUERY.keymap = "%s";' % current_user.keymap).close()
    query.add_html(Navigation(page='query'))
    query.div(cls='container-fluid')

    query.div(id='query-panel', role='tabpanel')
    query.ul(id='query-nav-tabs', cls='nav nav-tabs', role='tablist')
    query.a(id='add-tab', href='javascript:void(0);')
    query.span(cls='add-tab glyphicon glyphicon-plus', aria_hidden='true').close()
    query.close()
    query.close()
    query.div(id='query-tab-panes', cls='tab-content').close()
    query.close()

    # Footer
    query.close()
    query.add_html(Footer())

    return query


@query_page.route('/query/run-query', methods=['POST'])
@login_required
def run_query():
    with pg_connection(*current_user.get_config()) as (c, e):
        if e:
            return json.dumps({'success': False,
                               'error-msg': str(e)})
        try:
            t1 = time.time()
            c.execute(request.form['query'])
            columns = [desc[0] for desc in c.description]
            t2 = time.time()
            data = c.fetchall()
            t3 = time.time()
        except psycopg2.Warning as warn:
            # TODO
            pass
        except psycopg2.Error as err:
            return json.dumps({'success': False, 'error-msg': err.pgerror})
        except Exception as err:
            return json.dumps({'success': False, 'error-msg': str(err)})

    return json.dumps({'success': True,
                       'columns': columns,
                       'data': data,
                       'execution-time': (t2 - t1),
                       'fetching-time': (t3 - t2)})


@query_page.route('/query/run-explain', methods=['POST'])
@login_required
def run_explain():
    with pg_connection(*current_user.get_config()) as (c, e):
        if e:
            return json.dumps({'success': False,
                               'error-msg': str(e)})
        try:
            query = 'EXPLAIN (format json) %s' % request.form['query']
            c.execute(query)
            data = c.fetchall()
            plan = json.loads(data[0][0])
        except psycopg2.Warning as warn:
            # TODO
            pass
        except psycopg2.Error as err:
            return json.dumps({'success': False, 'error-msg': err.pgerror})
        except Exception as err:
            return json.dumps({'success': False, 'error-msg': str(err)})

    return json.dumps({'success': True, 'data': plan})
