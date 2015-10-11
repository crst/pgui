/*
  Main frontend module for the storage page.

  Displays a tree map of all the relations within the currently
  selected database.

  TODO: this sort of works in a basic way, but is not very nice
  (yet). Interactivity of the chart could be improved in various
  ways. Not really tested how this works when there is a considerable
  number of relations, or inherited tables. May also want to add some
  other charts to the page.

  Related files:
    - storage.css: CSS for the storage page.
*/

PGUI.STORAGE = {};


PGUI.STORAGE.mk_treemap_chart = function (data) {
    $('#treemap-chart').html('<div></div>');
    var width = $('#treemap-chart').width();
    var height = $(window).height() - $('#treemap-chart').offset().top - 10;
    $('#treemap-chart').height(height);

    var calculate_position = function () {
        this.style('left', function (d) { return d.x + 'px'; })
            .style('top', function (d) { return d.y + 'px'; })
            .style('width', function (d) { return Math.max(0, d.dx - 1) + 'px'; })
            .style('height', function (d) { return Math.max(0, d.dy - 1) + 'px'; });
    };

    var color = d3.scale.category20c();
    var color = d3.scale.ordinal()
        .range(colorbrewer.Set3[12]);

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

    $(window).resize(function () {
        PGUI.STORAGE.mk_treemap_chart(data);
    });
};
