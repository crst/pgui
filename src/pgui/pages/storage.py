import json

from flask import Blueprint, request
from flask.ext.login import current_user, login_required

from page import Page
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

    data = []
    with pg_connection(*current_user.get_config()) as (con, cur, err):
        with pg_log_err('list storage query'):
            cur.execute(query('list-storage'))
            data = cur.fetchall()

    display_schemas = params.getlist('schema')
    schemas = set()
    treemap_data = {'name': 'root', 'children': []}
    for (schema_name, table_name, t_size, t_tuples) in data:
        schemas.add(schema_name)
        if schema_name in display_schemas or len(display_schemas) == 0:
            treemap_data['children'].append({'schema_name': schema_name, 'name': table_name,
                                             'size': int(t_size), 'rows': int(t_tuples)})

    p = Page()

    # Header
    p.add_page(Header(title='Storage',
                      js=['static/pages/storage.js',
                          'static/lib/d3/d3.js',
                          'static/lib/d3/lib/colorbrewer/colorbrewer.js'],
                      css=['static/pages/storage.css']))
    p.add_page(Navigation(page='storage'))
    with p.div({'class': 'container-fluid'}):
        with p.div({'class': 'row form-row'}):
            with p.div({'class': 'col-md-10'}):
                with p.form({'id': 'schema-form', 'class': 'form-inline'}):
                    for schema in schemas:
                        with p.label({'class': 'checkbox-inline'}):
                            checked = (schema in display_schemas or len(display_schemas) == 0) and 'checked' or ''
                            with p.input({'type': 'checkbox', 'name': 'schema', 'value': '%s' % schema}, args=[checked]):
                                p.content(schema)

            with p.div({'class': 'col-md-2'}):
                with p.form({'id': 'mode-form', 'class': 'form-inline'}):
                    with p.label({'class': 'radio-inline'}):
                        with p.input({'type': 'radio', 'name': 'mode', 'value': 'size'}, args=['checked']):
                            p.content('Size')
                    with p.label({'class': 'radio-inline'}):
                        with p.input({'type': 'radio', 'name': 'mode', 'value': 'rows'}):
                            p.content('Rows (est.)')

        with p.div({'class': 'row'}):
            with p.div({'class': 'col-md-12'}):
                with p.div({'id': 'treemap-chart'}): pass
                with p.script():
                    p.content('PGUI.STORAGE.mk_treemap_chart(%s);' % json.dumps(treemap_data))

    p.add_page(Footer())

    return p
