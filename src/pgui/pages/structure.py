from collections import OrderedDict

from flask import Blueprint, request
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
    structure = Html()

    # Header
    structure.add_html(Header(title='Structure',
                              js=['static/pages/structure.js'],
                              css=['static/pages/structure.css']))
    structure.add_html(Navigation(page='structure'))
    structure.div(cls='container-fluid')

    schemas, schema_cols, table_data, table_cols = get_data()

    structure.ul()
    for schema in schemas:
        structure.div(cls='panel panel-default')

        structure.div(cls='panel-heading')
        structure.div(cls='row')
        structure.div(cls='col-md-2')
        structure.a('%s - %s' % (schema[0], schema[1]), cls='btn btn-success btn-xs schema-btn',
                    data_toggle='collapse', href='#%s' % schema[0], aria_expanded='false', aria_controls=schema[0])
        structure.close()
        structure.close('div') # col-md-2

        structure.div(cls='col-md-10')
        structure.ul(cls='list-inline')
        for i, col in enumerate(schema_cols, 2):
            structure.li('<strong>%s</strong> %s' % (schema[i], col)).close()
        structure.close()
        structure.close()
        structure.close() # row
        structure.close() # panel header

        structure.div(cls='panel-body')
        structure.div(cls='row collapse', id=schema[0])
        structure.div(cls='col-md-2')
        structure.div(cls='well')

        structure.b('Tables').close()
        structure.ul()
        for table in table_data[schema[0]]:
            structure.li()
            structure.a(table, href='#', onclick='PGUI.STRUCTURE.show_table_details(\'%s\', \'%s\'); return false;' % (schema[0], table)).close()
            structure.close('li')
        structure.close('ul')

        structure.close()
        structure.close()

        structure.div(cls='col-md-10')
        for table in table_data[schema[0]]:
            structure.div(id='table-details-%s-%s' % (schema[0], table), cls='table-details table-details-%s' % schema[0])
            data = table_data[schema[0]][table]
            structure.p('Table size: ').b(data['table-size']).close().close()
            structure.table(cls='table table-condensed')
            structure.tr()
            for tc in table_cols:
                structure.th(tc).close()
            structure.close('tr')
            for row in zip(*data['column-data'].values()):
                structure.tr()
                for col in row:
                    structure.td(col).close()
                structure.close('tr')
            structure.close('table')
            structure.close('div')
        structure.close()

        structure.close()
        structure.close() # panel body

        structure.close() # panel
    structure.close()

    # Footer
    structure.close()
    structure.add_html(Footer())

    return structure


def get_data():
    with pg_connection(*current_user.get_config()) as (c, e):
        c.execute(query('list-schemas'))
        schemas = c.fetchall()

        c.execute(query('list-tables'))
        tables = c.fetchall()

    schema_cols = ['', 'tables', 'views', 'foreign tables', 'temporary tables', 'functions', 'sequences']
    table_cols = ['Column name', 'Column type', 'Column default', 'Column is nullable'] #, 'Column size']
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
                #('column-size', parse_pg_array(table[6])),
            ]),
            'table-size': table[6],
        }
    return (schemas, schema_cols, table_data, table_cols)


def parse_pg_array(arr):
    return arr.replace('{', '').replace('}', '').split(',')
