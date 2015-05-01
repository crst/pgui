
PGUI.QUERY = {};
PGUI.QUERY.EDITORS = {};
PGUI.QUERY.eid = 1;

$(document).ready(function () {
    PGUI.QUERY.make_query_tab(PGUI.QUERY.eid);
    PGUI.QUERY.bind_events();
});


PGUI.QUERY.bind_events = function () {
    $('.run-query').unbind().click(function () {
        var eid = $(this).attr('data-id');
        PGUI.QUERY.run_query(eid);
    });
    $('.run-explain').unbind().click(function () {
        var eid = $(this).attr('data-id');
        PGUI.QUERY.run_explain(eid);
    });

    $('#add-tab').unbind().click(function () {
        PGUI.QUERY.eid += 1;
        PGUI.QUERY.make_query_tab(PGUI.QUERY.eid);
    });
};


PGUI.QUERY.make_query_tab = function (eid) {
    var active = (eid === 1) ? 'active' : '';
    var nav_content = [
        '<li role="presentation" class="', active, '">',
        '<a href="#query-editor-tab-', eid, '" aria-controls="query-editor-tab-', eid, '" role="tab" data-toggle="tab">Editor ', eid, '</a>',
        '</li>',
    ];

    var tab_content = [
        '<div role="tabpanel" class="tab-pane ', active, '" id="query-editor-tab-', eid, '">',

        // Editor
        '<div class="row">',
        '<div class="col-md-12">',
        '<textarea id="query-editor-', eid, '" name="query-editor-', eid, '" class="query-editor" cols="80" rows="20"></textarea>',
        '</div>',
        '</div>',

        // Actions
        '<div class="row">',
        '<div class="col-md-2">',
        '<a data-id="', eid, '" class="run-query btn btn-success" href="javascript:void(0);" role="button">Run</a>',
        '<a data-id="', eid, '"class="run-explain btn btn-default" href="javascript:void(0);" role="button">Explain</a>',
        '</div>',
        '<div class="col-md-8"></div>',
        '<div class="col-md-2"><div id="query-stats-', eid, '" class="query-stats"></div></div>',
        '</div>',

        // Results
        '<div class="row">',
        '<div class="col-md-12">',
        '<div role="tabpanel">',
        '<ul class="nav nav-tabs" role="tablist">',
        '<li role="presentation" class="active">',
        '<a href="#result-', eid, '" id="result-tab-', eid, '" role="tab" data-toggle="tab" aria-controls="result-', eid, '" aria-expanded="true">Result</a>',
        '</li>',
        '<li role="presentation">',
        '<a href="#csv-', eid, '" id="csv-tab-', eid, '" role="tab" data-toggle="tab" aria-controls="csv-', eid,'" aria-expanded="true">CSV</a>',
        '</li>',
        '<li role="presentation">',
        '<a href="#explain-', eid, '" id="explain-tab-', eid, '" role="tab" data-toggle="tab" aria-controls="explain-', eid, '" aria-expanded="true">Explain</a>',
        '</li>',
        '</ul>',

        '<div class="tab-content">',
        '<div role="tabpanel" class="tab-pane fade in active" id="result-', eid, '", aria-labelledBy="result-tab-', eid, '">',
        '<div id="query-result-', eid, '" class="query-result"></div>',
        '</div>',
        '<div role="tabpanel" class="tab-pane fade" id="csv-', eid, '", aria-labelledBy="csv-tab-', eid, '">',
        '<textarea id="csv-result-', eid, '" class="csv-result" rows=10></textarea>',
        '</div>',
        '<div role="tabpanel" class="tab-pane fade" id="explain-', eid, '", aria-labelledBy="explain-tab-', eid, '">',
        '<canvas id="explain-result-', eid, '" width=800 height=600></canvas>',
        '</div>',
        '</div>',

        '</div>', // tabpanel
        '</div>', // col
        '</div>', // row

        '</div>',
    ];

    $('#query-nav-tabs').append(nav_content.join(''));
    $('#query-tab-panes').append(tab_content.join(''));

    PGUI.QUERY.EDITORS[eid] = CodeMirror.fromTextArea($('#query-editor-' + eid).get(0),
                                                      {'mode': 'text/x-sql',
                                                       'keyMap': PGUI.QUERY.keymap,
                                                       'extraKeys': {'Alt-/': 'autocomplete',
                                                                     'Ctrl-Enter': function () { PGUI.QUERY.run_query(eid); },
                                                                     'Alt-Enter': function () { PGUI.QUERY.run_explain(eid); }},
                                                       'lineNumbers': true});
};


PGUI.QUERY.run_query = function (eid) {
    var editor = PGUI.QUERY.EDITORS[eid];
    var query = editor.getSelection();
    if (!query) {
        query = editor.getValue();
    }
    $.ajax({
        'method': 'POST',
        'url': 'query/run-query',
        'data': {'query': query}
    }).done(function (data) {
        PGUI.QUERY.display_query_result(eid, JSON.parse(data));
    });
};


PGUI.QUERY.run_explain = function (eid) {
    var editor = PGUI.QUERY.EDITORS[eid];
    var query = editor.getValue();
    $.ajax({
        'method': 'POST',
        'url': 'query/run-explain',
        'data': {'query': query}
    }).done(function (data) {
        PGUI.QUERY.display_explain_result(eid, JSON.parse(data));
    });
};


PGUI.QUERY.display_query_result = function (eid, result) {
    $('#query-stats-' + eid).html('');
    $('#result-tab-' + eid).tab('show');

    var t0 = Date.now();
    var tbl = [], csv = [], i, j;
    if (result.success) {
        var d = result.data;

        tbl.push('<table class="table table-condensed table-striped table-hover"><tr>');
        var columns = result.columns;
        for (i=0; i<columns.length; i++) {
            tbl.push('<th>' + columns[i] + '</th>');
            csv.push('"' + columns[i] + '"' + (i === columns.length - 1 ? '' : ','));
        }
        tbl.push('</tr>');
        csv.push('\n');

        for (i=0; i<d.length; i++) {
            tbl.push('<tr>');
            for (j=0; j<d[i].length; j++) {
                tbl.push('<td>' + d[i][j] + '</td>');
                csv.push('"' + d[i][j] + '"' + (j === d[i].length - 1 ? '' : ','));
            }
            tbl.push('</tr>');
            csv.push('\n');
        }
        tbl.push('</table>');
        csv.push('\n');

        var stats = '<p><h6>Result: ' + d.length + ' rows</h6></p>';
        stats += '<p><h6>Query execution: ' + result['execution-time'].toFixed(2) + ' seconds</h6></p>';
        stats += '<p><h6>Fetching results: ' + result['fetching-time'].toFixed(2) + ' seconds</h6></p>';
        $('#query-stats').html(stats);
    } else {
        tbl = ['\
<div class="alert alert-danger" role="alert">\
  <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>\
  <span class="sr-only">Error:</span>\
', result['error-msg'], '\
</div>'];
    }

    $('#query-result-' + eid).html(tbl.join(''));
    $('#csv-result-' + eid).val(csv.join(''));
    var t1 = Date.now();
    $('#query-stats-' + eid).append('<p><h6>Result rendering: ' + ((t1 - t0) / 1000).toFixed(2) + ' seconds</h6></p>');
};


PGUI.QUERY.display_explain_result = function (eid, result) {
    $('#explain-tab-' + eid).tab('show');
    var plans = result.data;

    // TODO
    for (var i in plans) {
        var plan = plans[i];
        var graph = new Springy.Graph();

        var plan_root = plan.Plan;
        var graph_root = graph.newNode({
            'label': plan_root['Node Type']
        });
        var plan_nodes = [{'graph_node': graph_root,
                           'plan_node': plan_root}];

        while (plan_nodes.length > 0) {
            var node = plan_nodes.shift();

            if ('Plans' in node.plan_node) {
                for (var j in node.plan_node.Plans) {
                    var plan_sub_node = node.plan_node.Plans[j];
                    var graph_sub_node = graph.newNode({'label': plan_sub_node['Node Type']});
                    graph.newEdge(graph_sub_node, node.graph_node, {'color': 'red'});

                    plan_nodes.push({
                        'graph_node': graph_sub_node,
                        'plan_node': plan_sub_node
                    });
                }
            }
        }

        var springy = window.springy = $('#explain-result-' + eid).springy({
            'graph': graph,
        });
    }
};
