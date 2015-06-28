
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


PGUI.hash = function(k) {
    var result = 0;
    for (var i = 0; i < k.length; i++) {
        result = (((result << 11) - result) + k.charCodeAt(i)) | 0;
    }
    return result;
};
