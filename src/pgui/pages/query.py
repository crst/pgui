import json
import time

from page import Html
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
    h = Html()

    # Header
    h.add_html(Header(title='Query',
                       js=['static/pages/query.js',
                           'static/pages/query_completion.js',
                           'static/pages/keywords.js',
                           'static/lib/springy/springy.js',
                           'static/lib/springy/springyui.js'],
                       css=['static/pages/query.css']))
    h.script('PGUI.QUERY.keymap = "%s";' % current_user.keymap).x()
    h.add_html(Navigation(page='query'))
    h.div(cls='container-fluid')

    h.div(cls='modal fade', id='query-history-dialog', tabindex='-1', role='dialog', aria_labelledby='Query History')
    h.div(cls='modal-dialog', role='document')
    h.div(cls='modal-content')
    h.div(cls='modal-header')
    h.button(tpe='button', cls='close', data_dismiss='modal', aria_label='Close')
    h.span('&times;', aria_hidden='true').x()
    h.x('button')
    h.h4('Query history', cls='modal-title', id='query-history-label').x()
    h.x('div')
    h.div(cls='modal-body')
    h.div(id='query-history').x()
    h.x('div').x('div').x('div').x('div')

    h.div(id='query-panel', role='tabpanel')
    h.ul(id='query-nav-tabs', cls='nav nav-tabs', role='tablist')
    h.li(role='presentation').a(id='show-query-history', href='javascript:void(0);')
    h.span(cls='add-tab glyphicon glyphicon-camera', aria_hidden='true').x()
    h.x('a').x('li')
    h.li(role='presentation').a(id='add-tab', href='javascript:void(0);')
    h.span(cls='add-tab glyphicon glyphicon-plus', aria_hidden='true').x()
    h.x('a').x('li')
    h.x('ul')

    h.div(id='query-tab-panes', cls='tab-content')
    h.x('div')
    h.x('div')

    # Footer
    h.x('div')
    h.add_html(Footer())

    return h


@query_page.route('/query/run-query', methods=['POST'])
@login_required
def run_query():
    with pg_connection(*current_user.get_config()) as (con, cur, err):
        if err:
            return json.dumps({'success': False,
                               'error-msg': str(err)})
        try:
            t1 = time.time()
            cur.execute(request.form['query'])
            columns = [desc[0] for desc in cur.description]
            t2 = time.time()
            data = cur.fetchall()
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
    with pg_connection(*current_user.get_config()) as (con, cur, err):
        if err:
            return json.dumps({'success': False,
                               'error-msg': str(err)})
        try:
            query = 'EXPLAIN (format json) %s' % request.form['query']
            cur.execute(query)
            data = cur.fetchall()
            plan = json.loads(data[0][0])
        except psycopg2.Warning as warn:
            # TODO
            pass
        except psycopg2.Error as err:
            return json.dumps({'success': False, 'error-msg': err.pgerror})
        except Exception as err:
            return json.dumps({'success': False, 'error-msg': str(err)})

    return json.dumps({'success': True, 'data': plan})
