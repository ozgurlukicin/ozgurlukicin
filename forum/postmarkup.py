# -*- coding: latin-1 -*-

"""
Post Markup
Author: Will McGugan (http://www.willmcgugan.com)
"""

__version__ = "1.0.7"

import re
from urllib import quote, unquote, quote_plus
from urlparse import urlparse, urlunparse
from copy import copy


pygments_available = True
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, ClassNotFound
    from pygments.formatters import HtmlFormatter
except ImportError:
    # Make Pygments optional
    pygments_available = False


re_url = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE| re.UNICODE)
def url_tagify(s, tag=u'url'):
        
    def repl(match):
        item = match.group(0)
        return '[%s]%s[/%s]' % (tag, item, tag)
    
    return re_url.sub(repl, s)
    
    


def create(include=None, exclude=None, use_pygments=True, *args, **kwargs):

    """Create a postmarkup object that coverts bbcode to XML snippets.

    include -- List or similar iterable containing the names of the tags to use
               If omitted, all tags will be used
    exclude -- List or similar iterable containing the names of the tags to exclude.
               If omitted, no tags will be excluded
    use_pygments -- If True, Pygments (http://pygments.org/) will be used for the code tag,
                    otherwise it will use <pre>code</pre>
    """

    markup = PostMarkup()

    def add_tag(name, tag_class, *args, **kwargs):
        if include is None or name in include:
            if exclude is not None and name in exclude:
                return
            markup.add_tag(name, tag_class, *args, **kwargs)

    #add_tag(u'b', SimpleTag, u'b', u'strong', *args, **kwargs)
    #add_tag(u'i', SimpleTag, u'i', u'em', *args, **kwargs)
    #add_tag(u'u', SimpleTag, u'u', u'u', *args, **kwargs)
    #add_tag(u's', SimpleTag, u's', u'strike', *args, **kwargs)
    #add_tag(u'link', LinkTag, u'link', *args, **kwargs)
    #add_tag(u'url', LinkTag, u'url', *args, **kwargs)
    add_tag(u'quote', QuoteTag, *args, **kwargs)
    #add_tag(u'img', ImgTag, u'img', *args, **kwargs)

    #add_tag(u'wiki', SearchTag, u'wiki',
    #        u"http://en.wikipedia.org/wiki/Special:Search?search=%s", u'wikipedia.com', *args, **kwargs)
    #add_tag(u'google', SearchTag, u'google',
    #        u"http://www.google.com/search?hl=en&q=%s&btnG=Google+Search", u'google.com', *args, **kwargs)
    #add_tag(u'dictionary', SearchTag, u'dictionary',
    #        u"http://dictionary.reference.com/browse/%s", u'dictionary.com', *args, **kwargs)
    #add_tag(u'dict', SearchTag, u'dict',
    #        u"http://dictionary.reference.com/browse/%s", u'dictionary.com', *args, **kwargs)

    #add_tag(u'list', ListTag, *args, **kwargs)
    #add_tag(u'*', ListItemTag, *args, **kwargs)

    if use_pygments:
        assert pygments_available, "Install pygments (http://pygments.org/) or call create with use_pygments=False"
        add_tag(u'code', PygmentsCodeTag, u'code', *args, **kwargs)
    else:
        add_tag(u'code', SimpleTag, u'code', u'pre', *args, **kwargs)

    return markup


def render_bbcode(bbcode, encoding="ascii", *args, **kwargs):

    """Renders a bbcode string in to XHTML. This is a shortcut if you don't
    need to customize any tags.

    bbcode -- A string containing the bbcode
    encoding -- If bbcode is not unicode, then then it will be encoded with
    this encoding (defaults to 'ascii'). Ignore the encoding if you already have
    a unicode string

    """

    _bbcode_postmarkup = create(use_pygments=pygments_available, *args, **kwargs)
    return _bbcode_postmarkup(bbcode, encoding, *args, **kwargs)


re_html=re.compile('<.*?>|\&.*?\;')
def textilize(s):
    """Remove markup from html"""
    return re_html.sub("", s)

re_excerpt = re.compile(r'\[".*?\]+?.*?\[/".*?\]+?', re.DOTALL)
re_remove_markup = re.compile(r'\[.*?\]', re.DOTALL)

def remove_markup(post):
    """Removes html tags from a string."""
    return re_remove_markup.sub("", post)

def get_excerpt(post):
    """Returns an excerpt between ["] and [/"]

    post -- BBCode string"""

    match = re_excerpt.search(post)
    if match is None:
        return ""
    excerpt = match.group(0)
    excerpt = excerpt.replace(u'\n', u"<br/>")
    return remove_markup(excerpt)


class TagBase(object):
    """
    Base class for a Post Markup tag.
    """

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.params = None
        self.auto_close = False
        self.enclosed = False
        self.open_pos = None
        self.close_pos = None
        self.raw = None
        self.args = args
        self.kwargs = kwargs

    def open(self, open_pos):
        """Called when the tag is opened. Should return a string or a
        stringifyable object."""
        self.open_pos = open_pos
        return ''

    def close(self, close_pos, content):
        """Called when the tag is closed. Should return a string or a
        stringifyable object."""
        self.close_pos = close_pos
        self.content = content
        return ''

    def get_tag_contents(self):
        """Gets the contents of the tag."""
        content_elements = self.content[self.open_pos+1:self.close_pos]
        contents = u"".join([unicode(element) for element in content_elements\
                             if isinstance(element, StringToken)])
        return contents

    def get_raw_tag_contents(self):
        """Gets the raw contents (includes html tags) of the tag."""
        content_elements = self.content[self.open_pos+1:self.close_pos]
        contents = u"".join(element.raw for element in content_elements)
        return contents

# A proxy object that calls a callback when converted to a string
class TagStringify(object):
    def __init__(self, callback, raw, *args, **kwargs):
        self.callback = callback
        self.raw = raw
    def __unicode__(self):
        return self.callback()
    def __repr__(self):
        return self.__unicode__()


class SimpleTag(TagBase):

    """Simple substitution tag."""

    def __init__(self, name, substitute, *args, **kwargs):
        TagBase.__init__(self, name, *args, **kwargs)
        self.substitute = substitute

    def open(self, open_pos):
        """Called to render the opened tag."""
        return u"<%s>"%(self.substitute)

    def close(self, close_pos, content):
        """Called to render the closed tag."""
        return u"</%s>"%(self.substitute)


class LinkTag(TagBase):

    """Tag that generates a link (</a>)."""

    def __init__(self, name, *args, **kwargs):
        TagBase.__init__(self, name, *args, **kwargs)

    def open(self, open_pos):
                
        self.open_pos = open_pos
        return TagStringify(self._open, self.raw)

    def close(self, close_pos, content):        

        self.close_pos = close_pos
        self.content = content
        return TagStringify(self._close, self.raw)

    def _open(self):
        
        self.domain = u''
        nest_level = self.tag_data['link_nest_level'] = self.tag_data.get('link_nest_level', 0) + 1
        
        if nest_level > 1:
            return u""            
        
        if self.params:
            url = self.params
        else:
            url = self.get_tag_contents()

        self.domain = ""
        #Unquote the url
        self.url = unquote(url)

        #Disallow javascript links
        if u"javascript:" in self.url.lower():
            return ""

        #Disallow non http: links
        url_parsed = urlparse(self.url)
        if url_parsed[0] and not url_parsed[0].lower().startswith(u'http'):
            return ""

        #Prepend http: if it is not present
        if not url_parsed[0]:
            self.url="http://"+self.url
            url_parsed = urlparse(self.url)

        #Get domain
        self.domain = url_parsed[1].lower()

        #Remove www for brevity
        if self.domain.startswith(u'www.'):
            self.domain = self.domain[4:]

        #Quote the url
        #self.url="http:"+urlunparse( map(quote, (u"",)+url_parsed[1:]) )
        self.url= unicode( urlunparse(quote(component, safe='/=&?:+') for component in url_parsed) )

        #Sanity check
        if not self.url:
            return u""

        if self.domain:
            return u'<a href="%s">'%self.url
        else:
            return u""

    def _close(self):
        
        self.tag_data['link_nest_level'] -= 1
        
        if self.tag_data['link_nest_level'] > 0:
            return u''
                
        if self.domain:
            return u'</a>'+self.annotate_link(self.domain)
        else:
            return u''

    def annotate_link(self, domain):
        """Annotates a link with the domain name.
        Override this to disable or change link annotation.
        """
        return u" [%s]"%domain


class QuoteTag(TagBase):
    """
    Generates a blockquote with a message regarding the author of the quote.
    """
    def __init__(self, *args, **kwargs):
        TagBase.__init__(self, 'quote', *args, **kwargs)

    def open(self, open_pos):
        # render for email quotation.
        if self.kwargs.has_key('render_for_email'):
            return u'%s\n >> ' % (self.params)
        else:
            return u'<div class="quote">%s<p>'%(self.params)

    def close(self, close_pos, content):
        if self.kwargs.has_key("render_for_email"):
            return u"\n"
        else:
            return u"</p></div>"


class SearchTag(TagBase):
    """
    Creates a link to a search term.
    """

    def __init__(self, name, url, label=u"", *args, **kwargs):
        TagBase.__init__(self, name, *args, **kwargs)
        self.url = url
        self.search = u""
        self.label = label or name

    def __unicode__(self):

        link = u'<a href="%s">'%self.url

        if u'%' in link:
            return link%quote_plus(self.get_tag_contents().encode('latin-1'))
        else:
            return link

    def open(self, open_pos):
        self.open_pos = open_pos
        return TagStringify(self._open, self.raw)

    def close(self, close_pos, content):

        self.close_pos = close_pos
        self.content = content
        return TagStringify(self._close, self.raw)

    def _open(self):
        if self.params:
            search=self.params
        else:
            search=self.get_tag_contents()
        link = u'<a href="%s">' % self.url
        if u'%' in link:
            return link%quote_plus(search.encode('latin-1'))
        else:
            return link

    def _close(self):

        if self.label:
            return u'</a>' + self.annotate_link(self.label)
        else:
            return u''

    def annotate_link(self, domain):
        return u" [%s]"%domain


class ImgTag(TagBase):

    def __init__(self, name, *args, **kwargs):
        TagBase.__init__(self, name, *args, **kwargs)
        self.enclosed=True

    def open(self, open_pos):
        self.open_pos = open_pos
        return TagStringify(self._open, self.raw)

    def close(self, close_pos, content):

        self.close_pos = close_pos
        self.content = content
        return TagStringify(self._close, self.raw)

    def _open(self):
        contents = self.get_raw_tag_contents()
        contents = contents.replace(u'"', "%22")
        return u'<img src="%s"></img><div style="display:none">'%(contents)

    def _close(self):
        return u"</div>"



class ListTag(TagBase):

    """Simple substitution tag."""

    def __init__(self, *args, **kwargs):
        TagBase.__init__(self, "list", *args, **kwargs)

    def open(self, open_pos):
        """Called to render the opened tag."""
        if self.params == "1":
            self.close_tag = u"</ol>"
            return u"<ol>"
        elif self.params == "a":
            self.close_tag = u"</ol>"
            return u'<ol style="list-style-type: lower-alpha;">'
        elif self.params == "A":
            self.close_tag = u"</ol>"
            return u'<ol style="list-style-type: upper-alpha;">'
        else:
            self.close_tag = u"</ul>"
            return u"<ul>"

    def close(self, close_pos, content):
        """Called to render the closed tag."""
        return self.close_tag


class ListItemTag(TagBase):

    _open_tag = None

    def __init__(self, *args, **kwargs):
        TagBase.__init__(self, u"*", *args, **kwargs)
        self.closed = False

    def open(self, open_pos):
        """Called to render the opened tag."""

        if self.closed:
            return u""

        tag_data = self.tag_data

        ret = u""
        if ( "ListItemTag.open_tag" in tag_data and
            tag_data["ListItemTag.open_tag"] is not None ):

            ret = u"</li>"
            tag_data["ListItemTag.open_tag"].closed = True

        tag_data["ListItemTag.open_tag"] = self
        return ret + u"<li>"

    def close(self, close_pos, content):
        """Called to render the closed tag."""

        if self.closed:
            return u""

        self.closed = True
        self.tag_data["ListItemTag.open_tag"] = None
        return u"</li>"



class PygmentsCodeTag(TagBase):

    # Set this to True if you want to display line numbers
    line_numbers = False

    def __init__(self, name, *args, **kwargs):
        TagBase.__init__(self, name, *args, **kwargs)
        self.enclosed = True

    def open(self, open_pos):
        self.open_pos = open_pos
        return TagStringify(self._open, self.raw)

    def close(self, close_pos, content):

        self.close_pos = close_pos
        self.content = content
        return TagStringify(self._close, self.raw)

    def _open(self):

        try:
            lexer = get_lexer_by_name(self.params, stripall=True)
        except ClassNotFound:
            contents = _escape(self.get_raw_tag_contents())
            self.no_close = True
            return u'''<div class="code"><pre>%s</pre></div><div style='display:none'>'''%contents
        formatter = HtmlFormatter(linenos=self.line_numbers, cssclass="code")
        code = self.get_raw_tag_contents()
        result = highlight(code, lexer, formatter)
        return result + u"\n<div style='display:none'>"

    def _close(self):

        return u"</div>"


# http://effbot.org/zone/python-replace.htm
class MultiReplace:

    def __init__(self, repl_dict, *args, **kwargs):
        # "compile" replacement dictionary

        # assume char to char mapping
        charmap = map(chr, range(256))
        for k, v in repl_dict.items():
            if len(k) != 1 or len(v) != 1:
                self.charmap = None
                break
            charmap[ord(k)] = v
        else:
            self.charmap = string.join(charmap, "")
            return

        # string to string mapping; use a regular expression
        keys = repl_dict.keys()
        keys.sort() # lexical order
        keys.reverse() # use longest match first
        pattern = "|".join(re.escape(key) for key in keys)
        self.pattern = re.compile(pattern)
        self.dict = repl_dict

    def replace(self, str):
        # apply replacement dictionary to string
        if self.charmap:
            return string.translate(str, self.charmap)
        def repl(match, get=self.dict.get):
            item = match.group(0)
            return get(item, item)
        return self.pattern.sub(repl, str)


class StringToken(object):

    def __init__(self, raw, *args, **kwargs):
        self.raw = raw

    def __unicode__(self):
        ret = PostMarkup.standard_replace.replace(self.raw)
        return ret


def _escape(s):
    return PostMarkup.standard_replace.replace(s.rstrip('\n'))

class PostMarkup(object):

    standard_replace = MultiReplace({ u'\n':u''})

    TOKEN_TAG, TOKEN_PTAG, TOKEN_TEXT = range(3)


    @staticmethod
    def TagFactory(tag_class, *args, **kwargs):
        """
        Returns a callable that returns a new tag instance.
        """
        def make():
            return tag_class(*args, **kwargs)

        return make


    # I tried to use RE's. Really I did.
    def tokenize(self, post):

        text = True
        pos = 0

        def find_first(post, pos, c):
            f1 = post.find(c[0], pos)
            f2 = post.find(c[1], pos)
            if f1 == -1:
                return f2
            if f2 == -1:
                return f1
            return min(f1, f2)

        while True:

            brace_pos = post.find(u'[', pos)
            if brace_pos == -1:
                yield PostMarkup.TOKEN_TEXT, post[pos:]
                return
            if brace_pos - pos > 0:
                yield PostMarkup.TOKEN_TEXT, post[pos:brace_pos]

            pos = brace_pos
            end_pos = pos+1

            open_tag_pos = post.find(u'[', end_pos)
            end_pos = find_first(post, end_pos, u']=')
            if end_pos == -1:
                yield PostMarkup.TOKEN_TEXT, post[pos:]
                return
            
            if open_tag_pos != -1 and open_tag_pos < end_pos:                
                yield PostMarkup.TOKEN_TEXT, post[pos:open_tag_pos]
                end_pos = open_tag_pos
                pos = end_pos
                continue

            if post[end_pos] == ']':
                yield PostMarkup.TOKEN_TAG, post[pos:end_pos+1]
                pos = end_pos+1
                continue

            if post[end_pos] == '=':
                try:
                    end_pos += 1
                    while post[end_pos] == ' ':
                        end_pos += 1
                    if post[end_pos] != '"':
                        end_pos = post.find(u']', end_pos+1)
                        if end_pos == -1:
                            return
                        yield PostMarkup.TOKEN_TAG, post[pos:end_pos+1]
                    else:
                        end_pos = find_first(post, end_pos, u'"]')
                        if end_pos==-1:
                            return
                        if post[end_pos] == '"':
                            end_pos = post.find(u'"', end_pos+1)
                            if end_pos == -1:
                                return
                            end_pos = post.find(u']', end_pos+1)
                            if end_pos == -1:
                                return
                            yield PostMarkup.TOKEN_PTAG, post[pos:end_pos+1]
                        else:
                            yield PostMarkup.TOKEN_TAG, post[pos:end_pos+1]
                    pos = end_pos+1
                except IndexError:
                    return


    def __init__(self):

        self.tags={}


    def default_tags(self):
        """
        Sets up a minimal set of tags.
        """
        self.tags[u'b'] = PostMarkup.TagFactory(SimpleTag, u'b', u'strong')
        self.tags[u'i'] = PostMarkup.TagFactory(SimpleTag, u'i', u'em')
        self.tags[u'u'] = PostMarkup.TagFactory(SimpleTag, u'u', u'u')
        self.tags[u's'] = PostMarkup.TagFactory(SimpleTag, u's', u'strike')

        return self


    def add_tag(self, name, tag_class, *args, **kwargs):
        """Add a tag factory to the markup.

        name -- Name of the tag
        tag_class -- Class derived from BaseTag
        args -- Aditional parameters for the tag class

        """
        self.tags[name] = PostMarkup.TagFactory(tag_class, *args, **kwargs)


    def __call__(self, *args, **kwargs):
        return self.render_to_html(*args, **kwargs)


    def render_to_html(self,
                       post_markup,
                       encoding="ascii",
                       exclude_tags=None,
                       *args,
                       **kwargs):
        
        """Converts Post Markup to XHTML.

        post_markup -- String containing bbcode
        encoding -- Encoding of string, defaults to "ascii"

        """

        if not isinstance(post_markup, unicode):
            post_markup = unicode(post_markup, encoding, 'replace')        
            
        if exclude_tags is None:
            exclude_tags = []

        tag_data = {}
        post = []
        tag_stack = []
        break_stack = []
        enclosed = False

        def check_tag_stack(tag_name):
            """Check to see if a tag has been opened."""
            for tag in reversed(tag_stack):
                if tag_name == tag.name:
                    return True
            return False

        def redo_break_stack():
            """Re-opens tags that have been closed prematurely."""
            while break_stack:
                tag = copy(break_stack.pop())
                tag.raw = u""
                tag_stack.append(tag)
                post.append(tag.open(len(post)))

        for tag_type, tag_token in self.tokenize(post_markup):
            #print tag_type, tag_token
            raw_tag_token = tag_token
            if tag_type == PostMarkup.TOKEN_TEXT:
                redo_break_stack()
                post.append(StringToken(tag_token))
                continue
            elif tag_type == PostMarkup.TOKEN_TAG:
                tag_token = tag_token[1:-1].lstrip()
                if ' ' in tag_token:
                    tag_name, tag_attribs = tag_token.split(u' ', 1)
                    tag_attribs = tag_attribs.strip()
                else:
                    if '=' in tag_token:
                        tag_name, tag_attribs = tag_token.split(u'=', 1)
                        tag_attribs = tag_attribs.strip()
                    else:
                        tag_name = tag_token
                        tag_attribs = u""
            else:
                tag_token = tag_token[1:-1].lstrip()
                tag_name, tag_attribs = tag_token.split(u'=', 1)
                tag_attribs = tag_attribs.strip()[1:-1]

            tag_name = tag_name.strip().lower()

            end_tag = False
            if tag_name.startswith(u'/'):
                end_tag = True
                tag_name = tag_name[1:]
                
            if tag_name in exclude_tags:
                continue

            if not end_tag:
                if enclosed:
                    post.append(StringToken(raw_tag_token))
                    continue
                if tag_name not in self.tags:
                    continue
                tag = self.tags[tag_name]()
                tag.tag_data = tag_data
                enclosed = tag.enclosed
                tag.raw = raw_tag_token

                redo_break_stack()
                tag.params=tag_attribs
                tag_stack.append(tag)
                post.append(tag.open(len(post)))
                if tag.auto_close:
                    end_tag = True

            if end_tag:
                if not check_tag_stack(tag_name):
                    if enclosed:
                        post.append(StringToken(raw_tag_token))
                    continue
                enclosed = False
                while tag_stack[-1].name != tag_name:
                    tag = tag_stack.pop()
                    break_stack.append(tag)
                    if not enclosed:
                        post.append(tag.close(len(post), post))
                post.append(tag_stack.pop().close(len(post), post))

        if tag_stack:
            redo_break_stack()
            while tag_stack:
                post.append(tag_stack.pop().close(len(post), post))

        html = u"".join(unicode(p) for p in post)
        return html



def test():

    post_markup = create()

    tests = []
    print """<link rel="stylesheet" href="code.css" type="text/css" />\n"""

    tests.append('[')
    tests.append(':-[ Hello, [b]World[/b]')

    tests.append("[link=http://www.willmcgugan.com]My homepage[/link]")
    tests.append('[link="http://www.willmcgugan.com"]My homepage[/link]')
    tests.append("[link http://www.willmcgugan.com]My homepage[/link]")
    tests.append("[link]http://www.willmcgugan.com[/link]")

    tests.append(u"[b]Hello André[/b]")
    tests.append(u"[google]André[/google]")
    tests.append("[s]Strike through[/s]")
    tests.append("[b]bold [i]bold and italic[/b] italic[/i]")
    tests.append("[google]Will McGugan[/google]")
    tests.append("[wiki Will McGugan]Look up my name in Wikipedia[/wiki]")

    tests.append("[quote Will said...]BBCode is very cool[/quote]")

    tests.append("""[code]
# A proxy object that calls a callback when converted to a string
class TagStringify(object):
    def __init__(self, callback, raw):
        self.callback = callback
        self.raw = raw
        r[b]=3
    def __str__(self):
        return self.callback()
    def __repr__(self):
        return self.__str__()
[/code]""")


    tests.append(u"[img]http://upload.wikimedia.org/wikipedia/commons"\
                 "/6/61/Triops_longicaudatus.jpg[/img]")

    tests.append("[list][*]Apples[*]Oranges[*]Pears[/list]")
    tests.append("""[list=1]
    [*]Apples
    [*]Oranges
    are not the only fruit
    [*]Pears
[/list]""")
    tests.append("[list=a][*]Apples[*]Oranges[*]Pears[/list]")
    tests.append("[list=A][*]Apples[*]Oranges[*]Pears[/list]")

    long_test="""[b]Long test[/b]

New lines characters are converted to breaks."""\
"""Tags my be [b]ove[i]rl[/b]apped[/i].

[i]Open tags will be closed.
[b]Test[/b]"""

    tests.append(long_test)

    tests.append("[dict]Will[/dict]")

    tests.append("[code unknownlanguage]10 print 'In yr code'; 20 goto 10[/code]")
        
    tests.append("[url=http://www.google.com/coop/cse?cx=006850030468302103399%3Amqxv78bdfdo]CakePHP Google Groups[/url]")
    tests.append("[url=http://www.google.com/search?hl=en&safe=off&client=opera&rls=en&hs=pO1&q=python+bbcode&btnG=Search]Search for Python BBCode[/url]")
    #tests = []
    # Attempt to inject html in to unicode
    tests.append("[url=http://www.test.com/sfsdfsdf/ter?t=\"></a><h1>HACK</h1><a>\"]Test Hack[/url]")
        
    tests.append('Nested urls, i.e. [url][url]www.becontrary.com[/url][/url], are condensed in to a single tag.')    

    for test in tests:
        print u"<pre>%s</pre>"%str(test.encode("ascii", "xmlcharrefreplace"))
        print u"<p>%s</p>"%str(post_markup(test).encode("ascii", "xmlcharrefreplace"))
        print u"<hr/>"
        print


    print render_bbcode("[b]For the lazy, use the http://www.willmcgugan.com render_bbcode function.[/b]")
    

if __name__ == "__main__":

    test()
