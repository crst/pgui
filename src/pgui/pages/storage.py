import json

from flask import Blueprint, request
from flask.ext.login import current_user, login_required

from page import Html
from pages.index import handle_params
from pages.shared import Header, Navigation, Footer
from pg import pg_connection, query


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
                            css=['static/lib/nvd3/nv.d3.css']))
    h.add_html(Navigation(page='storage'))
    h.div(cls='container-fluid')

    with pg_connection(*current_user.get_config()) as (c, e):
        # TODO
        c.execute(query('list-storage'))
        data = c.fetchall()

    values = []
    for (table_name, rel_size) in data:
        values.append({'label': table_name, 'value': int(rel_size)})
    chart_data = [{
        'key': 'Relation size',
        'values': values
    }]

    h.div(id='storage-chart').svg().x().x()
    h.script('PGUI.STORAGE.mk_relation_chart(%s);' % json.dumps(chart_data)).x()

    # Footer
    h.x()
    h.add_html(Footer())

    return h
