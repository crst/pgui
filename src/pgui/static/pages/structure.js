
PGUI.STRUCTURE = {};


PGUI.STRUCTURE.show_table_details = function (schema, table) {
    $('.table-details-' + schema).hide();
    $('#table-details-' + schema + '-' + table).show();
};
