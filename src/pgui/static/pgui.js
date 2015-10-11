/*
  Shared frontend module for all pages.
*/

var PGUI = {};


$(document).ready(function () {
    // Add keyboard shortcuts for modules.
    $('body').keydown(function (e) {
        if (e.ctrlKey) {
            var link = $('a[id="page-' + (e.keyCode - 48) + '"]');
            if (link[0]) {
                link[0].click();
            }
        }
    });
});


// Create localstorage keys in a structured way, so that different
// modules don't get in each others way.
PGUI.get_storage_key = function (module, key) {
    return PGUI.user + '-' + PGUI.host + '-' + PGUI.db + '-' + module + '-' + key;
};


PGUI.hash = function(k) {
    var result = 0;
    for (var i = 0; i < k.length; i++) {
        result = (((result << 11) - result) + k.charCodeAt(i)) | 0;
    }
    return result;
};
