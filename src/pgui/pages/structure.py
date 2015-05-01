from collections import OrderedDict
import json

from flask import Blueprint, request, escape
from flask.ext.login import current_user, login_required

from page import Html
from pages.index import handle_params
from pages.shared import Header, Navigation, Footer
from pg import pg_connection, query


structure_page = Blueprint('structure', __name__)

@structure_page.route('/structure')
@login_required
def structure_view():
    return Structure(request.args).render()


def Structure(params=None):
    handle_params(params)
    h = Html()

    # Header
    h.add_html(Header(title='Structure',
                      js=['static/pages/structure.js'],
                      css=['static/pages/structure.css']))
    h.add_html(Navigation(page='structure'))
    h.div(cls='container-fluid')

    schemas, schema_cols, table_data, table_cols = get_data()

    h.ul()
    for schema in schemas:
        h.div(cls='panel panel-default')

        h.div(cls='panel-heading')
        h.div(cls='row')
        h.div(cls='col-md-2')
        h.a('%s - %s' % (schema[0], schema[1]), cls='btn btn-success btn-xs schema-btn',
            data_toggle='collapse', href='#%s' % schema[0], aria_expanded='false', aria_controls=schema[0])
        h.x()
        h.x('div') # col-md-2

        h.div(cls='col-md-10')
        h.ul(cls='list-inline')
        for i, col in enumerate(schema_cols, 2):
            h.li('<strong>%s</strong> %s' % (schema[i], col)).x()
        h.x()
        h.x()
        h.x() # row
        h.x() # panel header

        h.div(cls='panel-body')
        h.div(cls='row collapse', id=schema[0])
        h.div(cls='col-md-2')
        h.div(cls='well')

        h.b('Tables').x()
        h.ul()
        for table in table_data[schema[0]]:
            h.li()
            h.a(table, href='#', onclick='PGUI.STRUCTURE.show_table_details(\'%s\', \'%s\'); return false;' % (schema[0], table)).x()
            h.x('li')
        h.x('ul')

        h.x()
        h.x()

        h.div(cls='col-md-10')
        for table in table_data[schema[0]]:
            h.div(id='table-details-%s-%s' % (schema[0], table), cls='table-details table-details-%s' % schema[0])
            data = table_data[schema[0]][table]
            h.p('Table size: ').b(data['table-size']).x().x()
            h.table(cls='table table-condensed')
            h.tr()
            for tc in table_cols:
                h.th(tc).x()
            h.th(id='col-size-header-%s-%s' % (schema[0], table))
            h.a('Get column sizes',
                href='#',
                onclick='PGUI.STRUCTURE.get_col_size(\'%s\', \'%s\'); return false;' % (schema[0], table)).x()
            h.x()
            h.x('tr')
            for row in zip(*data['column-data'].values()):
                h.tr()
                for col in row:
                    h.td(col).x()
                h.td(id='col-size-%s-%s-%s' % (schema[0], table, row[0])).x()
                h.x('tr')
            h.x('table')
            h.x('div')
        h.x()

        h.x()
        h.x() # panel body

        h.x() # panel
    h.x()

    # Footer
    h.x()
    h.add_html(Footer())

    return h


def get_data():
    with pg_connection(*current_user.get_config()) as (c, e):
        c.execute(query('list-schemas'))
        schemas = c.fetchall()

        c.execute(query('list-tables'))
        tables = c.fetchall()

    schema_cols = ['', 'tables', 'views', 'foreign tables', 'temporary tables', 'functions', 'sequences']
    table_cols = ['Column name', 'Column type', 'Column default', 'Column is nullable']
    table_data = {}
    for table in tables:
        if table[0] not in table_data:
            table_data[table[0]] = OrderedDict()
        table_data[table[0]][table[1]] = {
            'column-data': OrderedDict([
                ('colum-names', parse_pg_array(table[2])),
                ('column-types', parse_pg_array(table[3])),
                ('column-defaults', parse_pg_array(table[4])),
                ('column-is-nullable', parse_pg_array(table[5])),
            ]),
            'table-size': table[6],
        }
    return (schemas, schema_cols, table_data, table_cols)


def parse_pg_array(arr):
    return arr.replace('{', '').replace('}', '').split(',')


@structure_page.route('/structure/get-col-size', methods=['GET'])
@login_required
def get_col_size():
    if 'table-schema' in request.args and 'table-name' in request.args:
        params = {'table-schema': escape(request.args['table-schema']),
                  'table-name': escape(request.args['table-name'])}

        with pg_connection(*current_user.get_config()) as (c, e):
            c.execute(query('get-column-size'), params)
            data = c.fetchall()

        return json.dumps(data)

    return 'Please specify a table!'
