from collections import OrderedDict
import json

from flask import Blueprint, request, escape
from flask.ext.login import current_user, login_required

from page import Page
from pages.index import handle_params
from pages.shared import Header, Navigation, Footer
from pg import pg_connection, pg_log_err, query


structure_page = Blueprint('structure', __name__)

@structure_page.route('/structure')
@login_required
def structure_view():
    return Structure(request.args).render()


def Structure(params=None):
    handle_params(params)
    p = Page()

    # Header
    p.add_page(Header(title='Structure',
                      js=['static/pages/structure.js'],
                      css=['static/pages/structure.css']))
    p.add_page(Navigation(page='structure'))

    with p.div({'class': 'container-fluid'}):
        schemas, schema_cols, table_data, table_cols = get_data()

        with p.ul():
            for schema in schemas:
                with p.div({'class': 'panel panel-default'}):
                    with p.div({'class': 'panel-heading'}):
                        with p.div({'class': 'row'}):
                            with p.div({'class': 'col-md-2'}):
                                with p.a({'class': 'btn btn-success btn-xs schema-btn',
                                          'data-toggle': 'collapse',
                                          'href': '#%s' % schema[0],
                                          'aria-expanded': 'false',
                                          'aria-controls': schema[0]}):
                                    p.content('%s - %s' % (schema[0], schema[1]))

                            with p.div({'class': 'col-md-10'}):
                                with p.ul({'class': 'list-inline'}):
                                    for i, col in enumerate(schema_cols, 2):
                                        with p.li():
                                            p.content('<strong>%s</strong> %s' % (schema[i], col))

                    with p.div({'class': 'panel-body'}):
                        with p.div({'class': 'row collapse', 'id': schema[0]}):
                            with p.div({'class': 'col-md-2'}):
                                with p.div({'class': 'well'}):
                                    with p.b():
                                        p.content('Tables')

                                    with p.ul():
                                        for table in table_data[schema[0]]:
                                            with p.li():
                                                with p.a({'href': '#', 'onclick': 'PGUI.STRUCTURE.show_table_details(\'%s\', \'%s\'); return false;' % (schema[0], table)}):
                                                    p.content(table)

                            with p.div({'class': 'col-md-10'}):
                                for table in table_data[schema[0]]:
                                    with p.div({'id': 'table-details-%s-%s' % (schema[0], table), 'class': 'table-details table-details-%s' % schema[0]}):
                                        data = table_data[schema[0]][table]
                                        with p.p():
                                            p.content('Table size: ')
                                            with p.b():
                                                p.content(data['table-size'])

                                        with p.table({'class': 'table table-condensed'}):
                                            with p.tr():
                                                for tc in table_cols:
                                                    with p.th():
                                                        p.content(tc)
                                                with p.th({'id': 'col-size-header-%s-%s' % (schema[0], table)}):
                                                    with p.a({'href': '#',
                                                              'onclick': 'PGUI.STRUCTURE.get_col_size(\'%s\', \'%s\'); return false;' % (schema[0], table)}):
                                                        p.content('Get column sizes')

                                            for row in zip(*data['column-data'].values()):
                                                with p.tr():
                                                    for col in row:
                                                        with p.td():
                                                            p.content(col)
                                                    with p.td({'id': 'col-size-%s-%s-%s' % (schema[0], table, row[0])}):
                                                        pass

    p.add_page(Footer())

    return p


def get_data():
    schemas, tables = [], []
    with pg_connection(*current_user.get_config()) as (con, cur, err):
        with pg_log_err('list schemas and tables'):
            cur.execute(query('list-schemas'))
            schemas = cur.fetchall()

            cur.execute(query('list-tables'))
            tables = cur.fetchall()

    schema_cols = ['', 'tables', 'views', 'foreign tables', 'temporary tables', 'functions', 'sequences']
    table_cols = ['Column name', 'Column type', 'Column default', 'Column is nullable']
    table_data = {'public': OrderedDict()}
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

        data = []
        with pg_connection(*current_user.get_config()) as (con, cur, err):
            with pg_log_err('fetching column size for %s' % params):
                cur.execute(query('get-column-size'), params)
                data = cur.fetchall()

        return json.dumps(data)

    return 'Please specify a table!'
