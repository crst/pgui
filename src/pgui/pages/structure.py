from flask import Blueprint
from flask.ext.login import login_required

from page import Html
from pages.shared import Header, Navigation, Footer
from pg import pg_connection, query


structure_page = Blueprint('structure', __name__)

@structure_page.route('/structure')
@login_required
def structure_view():
    return Structure().render()


def Structure(params=None):
    structure = Html()

    # Header
    structure.add_html(Header(title='Structure'))
    structure.add_html(Navigation(page='structure'))
    structure.div(cls='container-fluid')

    structure.h3('TBD')

    # Footer
    structure.close()
    structure.add_html(Footer())

    return structure
