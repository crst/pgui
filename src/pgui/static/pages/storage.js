
PGUI.STORAGE = {};


PGUI.STORAGE.mk_treemap_chart = function (data) {
    var width = $('#treemap-chart').width();
    var height = $('#treemap-chart').height();

    var calculate_position = function () {
        this.style('left', function (d) { return d.x + 'px'; })
            .style('top', function (d) { return d.y + 'px'; })
            .style('width', function (d) { return Math.max(0, d.dx - 1) + 'px'; })
            .style('height', function (d) { return Math.max(0, d.dy - 1) + 'px'; });
    };

    var color = d3.scale.category20c();

    var treemap = d3.layout.treemap()
        .value(function(d) { return d.size; })
        .size([width, height])
        .sticky(true);

    var nodes = treemap.nodes(data);

    var node = d3.select('#treemap-chart div').selectAll('.node')
        .data(nodes)
        .enter()
        .append('div')
        .attr('class', 'node')
        .call(calculate_position)
        .style('background', function(d) { return color(d.schema_name); })
        .text(function (d) { return d.name; });

    $('#schema-form input').change(function () {
        $('#schema-form').submit();
    });

    $('#mode-form input').change(function () {
        var v = $(this).val();
        var mode_func = function (d) { return d[v]; };
        node.data(treemap.value(mode_func).nodes)
            .transition()
            .duration(500)
            .call(calculate_position);
    });
};
