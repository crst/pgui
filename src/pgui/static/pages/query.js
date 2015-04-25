
PGUI.QUERY = {};

$(document).ready(function () {
    PGUI.QUERY.editor = CodeMirror.fromTextArea($('#query-editor').get(0),
                                                {'mode': 'text/x-sql',
                                                 'keyMap': PGUI.QUERY.keymap,
                                                 'extraKeys': {'Alt-/': 'autocomplete',
                                                               'Ctrl-Enter': PGUI.QUERY.run_query,
                                                               'Alt-Enter': PGUI.QUERY.run_explain},
                                                 'lineNumbers': true,
                                                 'autofocus': true});
    PGUI.QUERY.bind_events();
});


PGUI.QUERY.bind_events = function () {
    $('#run-query').click(PGUI.QUERY.run_query);
    $('#run-explain').click(PGUI.QUERY.run_explain);
};


PGUI.QUERY.run_query = function () {
    var query = PGUI.QUERY.editor.getSelection();
    if (!query) {
        query = PGUI.QUERY.editor.getValue();
    }
    $.ajax({
        'method': 'POST',
        'url': 'query/run-query',
        'data': {'query': query}
    }).done(function (data) {
        PGUI.QUERY.display_query_result(JSON.parse(data));
    });
};


PGUI.QUERY.run_explain = function () {
    var query = PGUI.QUERY.editor.getValue();
    $.ajax({
        'method': 'POST',
        'url': 'query/run-explain',
        'data': {'query': query}
    }).done(function (data) {
        PGUI.QUERY.display_explain_result(JSON.parse(data));
    });
};


PGUI.QUERY.display_query_result = function (result) {
    $('#query-stats').html('');
    $('#result-tab').tab('show');

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

    $('#query-result').html(tbl.join(''));
    $('#csv-result').val(csv.join(''));
    var t1 = Date.now();
    $('#query-stats').append('<p><h6>Result rendering: ' + ((t1 - t0) / 1000).toFixed(2) + ' seconds</h6></p>');
};


PGUI.QUERY.display_explain_result = function (result) {
    $('#explain-tab').tab('show');
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

        var springy = window.springy = $('#explain-result').springy({
            'graph': graph,
        });
    }
};
