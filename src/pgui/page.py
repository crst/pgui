from functools import partial, reduce

class Html(object):
    def __init__(self):
        self.data = []
        self.stack = []
        self.tags = (
            'html', 'head', 'title', 'meta', 'link', 'script', 'body',
            'a',
            'b', 'button',
            'canvas', 'code',
            'div',
            'form',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'input',
            'label', 'li',
            'nav',
            'p', 'pre',
            'span', 'svg',
            'table', 'td', 'th', 'tr', 'textarea',
            'ul',
        )
        self.ctags = set(('meta', 'link'))
        self.tokens = {
            'cls': 'class',
            'fr' : 'for',
            'tpe': 'type',
            '_': '-',
        }

        def add_tag(tag_name, content='', **kwargs):
            return self.add(tag_name, content, **kwargs)

        for tag in self.tags:
            setattr(self, tag, partial(add_tag, tag))

    def _replace_tokens(self, text):
        return reduce(lambda acc, val: acc.replace(val[0], val[1]), self.tokens.items(), text)

    def add(self, tag, content='', **kwargs):
        params = ''.join([' %s="%s"' % (self._replace_tokens(k), v) for k, v in kwargs.items() if k != 'args'])
        args = 'args' in kwargs and ' '.join(kwargs['args']) or ''
        if tag in self.ctags:
            closing = ' /'
        else:
            self.stack.append(tag)
            closing = ''
        self.data.append('<%s %s%s%s>%s\n' % (tag, args, params, closing, content))
        return self

    def add_text(self, text):
        self.data.append(text)
        return self

    def add_html(self, data):
        self.data.append(data.render())
        return self

    def close(self, tag=None):
        if len(self.stack) > 0 and (not tag or tag == self.stack[-1]):
            tag = self.stack.pop()
        if tag:
            self.data.append('</%s>\n' % tag)
        return self

    def render(self):
        return ''.join(self.data)
