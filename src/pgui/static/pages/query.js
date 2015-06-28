
PGUI.QUERY = {};
PGUI.QUERY.EDITORS = {};
PGUI.QUERY.eid = 1;
PGUI.QUERY.config_key = PGUI.user + '-' + PGUI.host + '-' + PGUI.db;


$(document).ready(function () {
    var queries_key = PGUI.QUERY.config_key + '-queries';
    if (PGUI.QUERY.config_key in localStorage && !$.isEmptyObject(JSON.parse(localStorage[queries_key]))) {
        var q = JSON.parse(localStorage[queries_key]);
        for (var k in q) {
            PGUI.QUERY.make_query_tab(k, q[k]);
            PGUI.QUERY.eid = Math.max(PGUI.QUERY.eid, k);
        }
    } else {
        PGUI.QUERY.make_query_tab(PGUI.QUERY.eid, '');
    }
    PGUI.QUERY.bind_events();
});


PGUI.QUERY.refresh_editor = function (eid) {
    window.setTimeout(function() {
        PGUI.QUERY.EDITORS[eid].refresh();
    }, 1);
};


PGUI.QUERY.bind_events = function () {
    $('.run-query').unbind().click(function () {
        var eid = $(this).attr('data-eid');
        PGUI.QUERY.run_query(eid);
    });
    $('.run-explain').unbind().click(function () {
        var eid = $(this).attr('data-eid');
        PGUI.QUERY.run_explain(eid);
    });

    $('#show-query-history').unbind().click(function () {
        PGUI.QUERY.show_query_history();
    });

    $('#add-tab').unbind().click(function () {
        PGUI.QUERY.eid += 1;
        PGUI.QUERY.make_query_tab(PGUI.QUERY.eid, '');
    });

    $('.remove-editor-tab').unbind().click(function () {
        var eid = $(this).attr('data-eid');
        PGUI.QUERY.remove_query_tab(eid);
    });

    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
        var eid = $(e.target).attr('data-eid');
        if (eid) {
            PGUI.QUERY.refresh_editor(eid);
        }
    });

    $(window).unload(function() {
        var storage = {};
        for (var k in PGUI.QUERY.EDITORS) {
            storage[k] = PGUI.QUERY.EDITORS[k].getValue();
        }
        localStorage[PGUI.QUERY.config_key + '-queries'] = JSON.stringify(storage);
    });
};


PGUI.QUERY.make_query_tab = function (eid, query) {
    var active = (eid === 1) ? 'active' : '';
    var nav_content = [
        '<li id="query-editor-nav-', eid, '" role="presentation" class="', active, '">',
        '<a href="#query-editor-tab-', eid, '" data-eid="', eid, '" aria-controls="query-editor-tab-', eid, '" role="tab" data-toggle="tab">Query ', eid,
        '<span id="remove-editor-tab-', eid, '" class="remove-editor-tab glyphicon glyphicon-remove" data-eid=', eid, ' aria-hidden="true"></span></a>',
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
        '<a data-eid="', eid, '" class="run-query btn btn-success" href="javascript:void(0);" role="button">Run</a>',
        '<a data-eid="', eid, '" class="run-explain btn btn-default" href="javascript:void(0);" role="button">Explain</a>',
        '</div>',
        '<div class="col-md-6"></div>',
        '<div class="col-md-4"><div id="query-stats-', eid, '" class="query-stats small"></div></div>',
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

    PGUI.QUERY.EDITORS[eid] = CodeMirror.fromTextArea(document.getElementById('query-editor-' + eid),
                                                      {'mode': 'text/x-sql',
                                                       'keyMap': PGUI.QUERY.keymap,
                                                       'extraKeys': {'Alt-/': 'autocomplete',
                                                                     'Ctrl-Enter': function () { PGUI.QUERY.run_query(eid); },
                                                                     'Alt-Enter': function () { PGUI.QUERY.run_explain(eid); }},
                                                       'lineNumbers': true,
                                                       'cursorBlinkRate': 0,
                                                       'theme': 'neo',
                                                       'autofocus': true});
    PGUI.QUERY.EDITORS[eid].setValue(query);
    PGUI.QUERY.refresh_editor(eid);
    PGUI.QUERY.bind_events();
    $('a[href="#query-editor-tab-' + eid + '"]').tab('show');
};


PGUI.QUERY.remove_query_tab = function (eid) {
    $('li[id="query-editor-nav-' + eid + '"]').prev('li').find('a').tab('show');
    delete PGUI.QUERY.EDITORS[eid];
    $('#query-editor-nav-' + eid).remove();
    $('#query-editor-tab-' + eid).remove();
};


PGUI.QUERY.store_query = function (query) {
    // TODO: build abstraction for keys
    var key = PGUI.QUERY.config_key + '-stored-queries';
    if (!(key in localStorage) || $.isEmptyObject(JSON.parse(localStorage[key]))) {
        localStorage[key] = JSON.stringify({'entry': undefined});
    }
    var stored_queries = JSON.parse(localStorage[key]);

    var h = PGUI.hash(query);
    if(!stored_queries['entry']) {
        stored_queries[h] = {
            'query': query,
            'prev': undefined,
            'next': undefined
        };
        stored_queries['entry'] = h;
    } else if (stored_queries['entry'] !== h) {
        if(stored_queries[h]) {
            var prevHash = stored_queries[h]['prev'];
            var nextHash = stored_queries[h]['next'];
            if (prevHash) {
                stored_queries[prevHash]['next'] = nextHash;
            }
            if (nextHash) {
                stored_queries[nextHash]['prev'] = prevHash;
            }
        }

        var oldEntry = stored_queries['entry'];
        stored_queries[h] = {
            'query': query,
            'prev': h,
            'next': oldEntry
        };
        stored_queries[oldEntry]['prev'] = h;
        stored_queries['entry'] = h;
    }

    // TODO: prune old queries
    localStorage[key] = JSON.stringify(stored_queries);
};


PGUI.QUERY.show_query_history = function () {
    var key = PGUI.QUERY.config_key + '-stored-queries';
    if (!(key in localStorage) || $.isEmptyObject(JSON.parse(localStorage[key]))) {
        localStorage[key] = JSON.stringify({'entry': undefined});
    }
    var stored_queries = JSON.parse(localStorage[key]);

    var make_query_link = function (h) {
        if (h in stored_queries) {
            return '<a class="query-history-select" href="javascript:void(0);">' + stored_queries[h]['query'] + '</a>';
        }
        return '';
    };

    var buff = ['<ul>'];
    var h = stored_queries['entry'];
    while (h in stored_queries && stored_queries[h]['next']) {
        buff.push('<li>' + make_query_link(h) + '</li>');
        h = stored_queries[h]['next'];
    }
    buff.push('<li>' + make_query_link(h) + '</li>');
    buff.push('</ul>');
    $('#query-history').html(buff.join('\n'));

    $('.query-history-select').click(function () {
        var query = $(this).html();
        var active_tab = $('li[class="active"]').find('a')[0];
        var eid = $(active_tab).attr('data-eid');
        PGUI.QUERY.set_query(eid, query);
        $('#query-history-dialog').modal('hide');
    });

    $('#query-history-dialog').modal();
};


PGUI.QUERY.run_query = function (eid) {
    var query = PGUI.QUERY.get_query(eid);
    PGUI.QUERY.store_query(query);
    $('#query-stats-' + eid).html('<span class="glyphicon glyphicon-refresh loading-spinner" aria-hidden="true"></span>');
    $.ajax({
        'method': 'POST',
        'url': 'query/run-query',
        'data': {'query': query}
    }).done(function (data) {
        PGUI.QUERY.display_query_result(eid, JSON.parse(data));
    });
};


PGUI.QUERY.run_explain = function (eid) {
    var query = PGUI.QUERY.get_query(eid);
    PGUI.QUERY.store_query(query);
    $.ajax({
        'method': 'POST',
        'url': 'query/run-explain',
        'data': {'query': query}
    }).done(function (data) {
        PGUI.QUERY.display_explain_result(eid, JSON.parse(data));
    });
};


PGUI.QUERY.get_query = function (eid) {
    var editor = PGUI.QUERY.EDITORS[eid];
    var query = editor.getSelection();
    if (!query) {
        query = editor.getValue();
    }
    return query;
};

PGUI.QUERY.set_query = function (eid, query) {
    var editor = PGUI.QUERY.EDITORS[eid];
    editor.setValue(query);
};


PGUI.QUERY.display_query_result = function (eid, result) {
    $('#query-stats-' + eid).html('');
    $('#result-tab-' + eid).tab('show');

    var t0 = Date.now();
    var tbl = [], csv = [], i, j;
    var stats = '<ul class="list-inline">';
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

        stats += '<li><strong>' + d.length + ' rows</strong></li>';
        stats += '<li><strong>' + result['execution-time'].toFixed(1) + 's</strong> query</li>';
        stats += '<li><strong>' + result['fetching-time'].toFixed(1) + 's</strong> fetching</li>';
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
    stats += '<li><strong>' + ((t1 - t0) / 1000).toFixed(1) + 's</strong> rendering</li></ul>';
    $('#query-stats-' + eid).html(stats);
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
