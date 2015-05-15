import json

from flask import Blueprint, request
from flask.ext.login import current_user, login_required

from page import Html
from pages.index import handle_params
from pages.shared import Header, Navigation, Footer
from pg import pg_connection, pg_log_err, query


storage_page = Blueprint('storage', __name__)

@storage_page.route('/storage')
@login_required
def storage_view():
    return Storage(request.args).render()


def Storage(params=None):
    handle_params(params)
    h = Html()

    # Header
    h.add_html(Header(title='Storage',
                      js=['static/pages/storage.js',
                          'static/lib/d3/d3.js',
                          'static/lib/nvd3/nv.d3.js'],
                      css=['static/pages/storage.css',
                           'static/lib/nvd3/nv.d3.css']))
    h.add_html(Navigation(page='storage'))
    h.div(cls='container-fluid')

    h.div(cls='row').div(cls='col-md-10').x()
    h.div(cls='col-md-2')
    h.form(id='mode-form', cls='form-inline')
    h.label(cls='radio-inline')
    h.input(tpe='radio', name='mode', value='size', args=['checked']).add_text('Size')
    h.x()
    h.label(cls='radio-inline')
    h.input(tpe='radio', name='mode', value='rows').add_text('Rows (est.)')
    h.x().x()
    h.x('div').x('div')

    data = []
    with pg_connection(*current_user.get_config()) as (con, cur, err):
        with pg_log_err('list storage query'):
            cur.execute(query('list-storage'))
            data = cur.fetchall()

    treemap_data = {'name': 'root', 'children': []}
    values = []
    for (schema_name, table_name, t_size, t_tuples) in data:
        treemap_data['children'].append({'schema_name': schema_name, 'name': table_name,
                                         'size': int(t_size), 'rows': int(t_tuples)})
        values.append({'label': table_name, 'value': int(t_size)})
    chart_data = [{
        'key': 'Relation size',
        'values': values[:10]
    }]

    h.div(cls='col-md-12')
    h.div(id='treemap-chart').div().x().x()
    h.script('PGUI.STORAGE.mk_treemap_chart(%s);' % json.dumps(treemap_data)).x()
    h.x()

    h.div(cls='col-md-12').b('Top 10 relations').x()
    h.div(id='storage-chart').svg().x().x()
    h.script('PGUI.STORAGE.mk_relation_chart(%s);' % json.dumps(chart_data)).x()
    h.x()

    h.x('div') # row

    # Footer
    h.x()
    h.add_html(Footer())

    return h
