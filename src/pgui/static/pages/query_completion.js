
PGUI.QUERY_COMPLETION = {};

$(document).ready(function () {
    for (var i=0; i<PGUI.QUERY_COMPLETION.sql_keywords.length; i++) {
        PGUI.QUERY_COMPLETION.insert_word(PGUI.QUERY_COMPLETION.completion_trie, PGUI.QUERY_COMPLETION.sql_keywords[i]);
    }
});


CodeMirror.commands.autocomplete = function (editor) {
    CodeMirror.showHint(editor, PGUI.QUERY_COMPLETION.complete);
};


PGUI.QUERY_COMPLETION.completion_trie = {
    'val': 'root',
    'leaf': false,
    'next': {}
};


PGUI.QUERY_COMPLETION.insert_word = function (root, word) {
    word = word.toUpperCase();
    var node = root, i, val;
    for (i=0; i<word.length; i++) {
        val = word[i];
        if (!(val in node.next)) {
            var next = {'val': val, 'next': {}};
            next.leaf = i === word.length - 1;
            node.next[val] = next;
        }
        node = node.next[val];
    }
};


PGUI.QUERY_COMPLETION.search_completions = function (root, prefix) {
    var node = root, nx, i;
    for (i=0; i<prefix.length; i++) {
        nx = prefix[i];
        if (nx in node.next) {
            node = node.next[nx];
        }
    }

    var result = [], key, n;
    var make_completions = function (node, prefix) {
        if (node.leaf) {
            result.push(prefix);
        }
        for (key in node.next) {
            n = node.next[key];
            make_completions(n, prefix + n.val);
        }
    };
    make_completions(node, prefix);
    return result;
};


PGUI.QUERY_COMPLETION.complete = function (editor) {
    var cur = editor.getCursor();
    var token = editor.getTokenAt(cur);
    var prefix = token.string.toUpperCase();
    var completions = PGUI.QUERY_COMPLETION.search_completions(PGUI.QUERY_COMPLETION.completion_trie, prefix);

    var Pos = CodeMirror.Pos;
    return {'list': completions, 'from': Pos(cur.line, token.start), 'to': Pos(cur.line, token.end)};
};
