
PGUI.STORAGE = {};

PGUI.STORAGE.mk_relation_chart = function (data) {
    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            .tooltips(true)
            .showValues(true)
        ;

        d3.select('#storage-chart svg')
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
};
