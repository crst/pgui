from contextlib import contextmanager


class Page(object):
    ctags = set(('hr', 'input', 'meta', 'link'))

    def __init__(self):
        self._buffer = []
        self._indent = 0
        self._tabsize = 2

    def render(self):
        return ''.join(self._buffer)

    def add_page(self, page):
        self._buffer.append(page.render())
        return self

    def content(self, text):
        self._buffer.append('%s%s\n' % (self._get_spaces(), text))
        return self

    def close(self, tag):
        self._buffer.append('%s</%s>' % (self._get_spaces(), tag))
        self._indent -= self._tabsize
        return self

    def _get_spaces(self):
        return self._indent * ' '

    def __getattr__(self, name):
        @contextmanager
        def handler(*args, **kwargs):
            params = ''
            if len(args) == 1:
                params = ''.join([' %s="%s"' % (k, v) for k, v in args[0].items()])

            args = ''
            if 'args' in kwargs:
                args = ' ' + ' '.join(kwargs['args'])

            closing = ''
            if name in Page.ctags:
                closing = ' /'

            self._buffer.append('%s<%s%s%s%s>\n' % (self._get_spaces(), name, params, args, closing))
            self._indent += self._tabsize
            yield self
            self._indent -= self._tabsize

            close = True
            if 'close' in kwargs:
                close = kwargs['close']

            if not name in Page.ctags and close:
                self._buffer.append('%s</%s>\n' % (self._get_spaces(), name))

        return handler
