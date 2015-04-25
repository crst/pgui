
var PGUI = {};

$(document).ready(function () {
    $('body').keydown(function (e) {
        if (e.ctrlKey) {
            var link = $('a[id="page-' + (e.keyCode - 48) + '"]');
            if (link[0]) {
                link[0].click();
            }
        }
    });
});
