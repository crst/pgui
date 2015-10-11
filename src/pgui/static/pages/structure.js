/*
  Main frontend module for the structure page.

  Displays static information about the database structure.

  TODO: there are quite some information available from the catalog
  that are not displayed yet. Also this should probably group
  inherited relations.

  Related files:
    - structure.css: CSS for the structure page.
*/


PGUI.STRUCTURE = {};


PGUI.STRUCTURE.show_table_details = function (schema, table) {
    $('.table-details-' + schema).hide();
    $('#table-details-' + schema + '-' + table).show();
};

// Asynchronously get the column sizes, because this requires a table
// scan and may therefore take a while.
PGUI.STRUCTURE.get_col_size = function (schema, table) {
    var header = $('#col-size-header-' + schema + '-' + table);
    header.html('<span class="glyphicon glyphicon-refresh loading-spinner" aria-hidden="true"></span>');
    $.ajax({
        'method': 'GET',
        'url': 'structure/get-col-size',
        'data': {'table-schema': schema, 'table-name': table}
    }).done(function (data) {
        var col_sizes = JSON.parse(data);
        for (var i=0; i<col_sizes.length; i++) {
            var cols = col_sizes[i];
            $('#col-size-' + schema + '-' + table + '-' + cols[0]).html(cols[1]);
        }
        header.html('Column size');
    });
};
