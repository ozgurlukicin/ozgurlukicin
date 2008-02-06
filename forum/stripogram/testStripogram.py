# Copyright (c) 2001 Chris Withers
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: testStripogram.py,v 1.20 2003/01/07 11:03:56 fresh Exp $

# we need to import ourselves, so add the folder above
# into the module search path
import sys
sys.path.insert(0,'..')

from unittest import makeSuite, TestCase, main, TestSuite

from stripogram import html2safehtml, html2text

valid_tags=['b', 'a', 'i', 'br', 'p','ul','li']
valid_tags2=['b','i','br']

def test(function,input,expected):
    output=''
    output = apply(function,input)
    assert output==expected, "\nInput   : '%s'\nExpected: '%s'\n     Got: '%s'\n" % (input[0],expected,output)

class stripogramTests(TestCase):

    def test_html2text1(self):
        "test \n becomes a space"
        test(html2text,('See also:\n<a href="">this</a>\nfor',),'See also: this for')

    def test_html2text2(self):
        "test spaces are left intact when tags are removed"
	test(html2text,('<b>andre</b> camargo',),'andre camargo')

    def test_html2text3(self):
        "test multiple spaces in HTML become single spaces in text"
	test(html2text,('<p><font><b>andre</b></font> camargo</p> <i>strip-o-gram</i> <u>is</u>  great.',),'\n\nandre camargo strip-o-gram is great.')

    def test_html2text4(self):
        "test for enable image tag"
	test(html2text, ('<img src="ImImage.png">',), '\n\nImage: ImImage.png')

    def test_html2text5(self):
        "test for disable image tag"
	test(html2text, ('there aren\'t anything <img src="ImImage.png"> between us.', ['img']), 'there aren\'t anything between us.')

    def test_html2text6(self):
        "test for html ordered lists"
	test(html2text, ('<ol><li>one</li><li>two</li><li>three</li></ol>',), '    \n\n    1 - one\n\n    \n\n    2 - two\n\n    \n\n    3 - three\n\n    \n\n')

    def test_html2text7(self):
        "test for case of ignored tags"
	test(html2text, ('there aren\'t anything <img src="ImImage.png"> between us.', ['iMg']), 'there aren\'t anything between us.')

    def test_html2text8(self):
        "test for indent width"
	test(html2text, ('<ol><li>one</li><li>two</li><li>three</li></ol>',(),2), '  \n\n  1 - one\n\n  \n\n  2 - two\n\n  \n\n  3 - three\n\n  \n\n')
    
    def test_html2text9(self):
        "test for page width"
	test(html2text, ('one two three four',(),4,10), 'one two\nthree four')
        
    def test_html2safehtml1(self):
        "test correct HTML is left alone 1"
        test(html2safehtml,('<b>x<br>y</b>z<p>a',),'<b>x<br>y</b>z<p>a')

    def test_html2safehtml2(self):
        "test correct HTML is left alone 2"
        test(html2safehtml,('<b>x<br>y<i>z</b>a</i>b<p>',),'<b>x<br>y<i>za</i>b<p></b>')

    def test_html2safehtml3(self):
        "test overlapping tags are closed in the correct order 1"
        test(html2safehtml,('<b><p>x</p>y<p>z</p>a</b>',),'<b><p>x</p>y<p>z</p>a</b>')
        
    def test_html2safehtml4(self):
        "test overlapping tags are closed in the correct order 2"
        test(html2safehtml,('<p>x<i>y</p>z</i>a<p>b</p>',),'<p>x<i>yz</i>a<p>b</p>')
        
    def test_html2safehtml5(self):
        "test optionally closed tags that are correct are left alone"
        test(html2safehtml,('<ul><li>x<li>y<li>z</ul>',valid_tags),'<ul><li>x<li>y<li>z</ul>')
        
    def test_html2safehtml6(self):
        "test that XML-ish unclosed tags are handled sensibly"
        test(html2safehtml,('Roses <b>are</B> red,<br/>violets <i>are</i> blue',valid_tags2),
                            'Roses <b>are</b> red,<br>violets <i>are</i> blue')
        
    def test_html2safehtml7(self):
        "check that unfinished start tags at the end of input are ignored"
        test(html2safehtml,('Roses <b>are</B> red,<br/QUACK',valid_tags2),
                            'Roses <b>are</b> red,')
        
    def test_html2safehtml8(self):
        "check that unfinished end tags at the end of input are ignored"
        test(html2safehtml,('Roses <b>are</B> red,<br/</blink>QUACK<//blink> violets <i>are</i> blue',valid_tags2),
                            'Roses <b>are</b> red,QUACK violets <i>are</i> blue')
        
    def test_html2safehtml9(self):
        "test for bug reported by J M Cerqueira Esteves <jmce@artenumerica.com>"
        test(html2safehtml,('Roses <b>are</B> red,QUACK<//blink',valid_tags2),
                            'Roses <b>are</b> red,QUACK')
        
    def test_html2safehtml10(self):
        "test for non-bug reported by on Squishdot's Bug Tracker"
        test(html2safehtml,('a<form>b<input name="test" type="text">c</form>d',valid_tags),'abcd')
        
    def test_html2safehtml11(self):
        "test that entity refs are handled nicely"
        test(html2safehtml,('&lt;squishdot@yahoo.com&gt;',),'&lt;squishdot@yahoo.com&gt;')

    def test_html2safehtml12(self):
        "test that ampersands aren't buggered about with"
        test(html2safehtml,('one & two & three &three; &blagh ;',),'one &amp; two &amp; three &amp;three; &amp;blagh ;')
        
    def test_html2safehtml13(self):
        "test short attribute names"
        test(html2safehtml,('<b x="xyz">',),'<b x="xyz"></b>')

    def test_html2safehtml14(self):
        "test short attribute values"
        test(html2safehtml,('<a href="x">test</a>',),'<a href="x">test</a>')

    def test_html2safehtml15(self):
        "test empty attribute values"
        test(html2safehtml,('<a href="">test</a>',),'<a href="">test</a>')

    def test_html2safehtml16(self):
        "test image tag"
        test(html2safehtml,('<img src="fish.jpg"><img src="monkey.gif"/>',['img']),
                            '<img src="fish.jpg"><img src="monkey.gif">')

    def test_html2safehtml17(self):
        "test tags that aren't closed"
        test(html2safehtml,('<br><wbr><hr><input><isindex><base><meta><img>',
                            ['br','wbr','hr','input','isindex','base','meta','img']),
                            '<br><wbr><hr><input><isindex><base><meta><img>')

    def test_html2safehtml18(self):
        "test cross scripting vulnerability"
        test(html2safehtml,('<input type="submit" onClick="javascript:alert(\'Die\')">',['input']),
                            '<input type="submit">')
        
    def test_html2safehtml19(self):
        "test strict cross scripting vulnerability to handle browser defaults"
        test(html2safehtml,('<input type="submit" onClick="alert(\'Die\')">',['input']),
                            '<input type="submit">')

    def test_html2safehtml20(self):
        "test captalised tags"
        test(html2safehtml,('<INPUT TyPe="submit" onClick="alert(\'Die\')">',['input']),
                            '<input type="submit">')

    def test_html2safehtml21(self):
        "test captalised valid_tags"
        test(html2safehtml,('<INPUT TyPe="submit" onClick="alert(\'Die\')"><fOnt></font>',['INPUT','fOnt']),
                            '<input type="submit"><font></font>')

    def test_html2safehtml21(self):
        "test attributes without values"
        test(html2safehtml,('<input type=radio name="digest" value="0" CHECKED>',['input']),
                            '<input type="radio" name="digest" value="0" checked>')    

try:
    import Testing
    import Zope
    try:
        Zope.startup()
    except AttributeError:
        pass
    from Products.PythonScripts.PythonScript import PythonScript 
except ImportError:
    class ZopeTests(TestCase):
        pass
else:
    class ZopeTests(TestCase):

        def _testScript(self,txt):
            theScript = PythonScript('test')
            theScript.ZBindings_edit({})
            theScript.write(txt)
            theScript._makeFunction()
            return theScript()
            
        def test_ScriptPython_html2safehtml(self):
            self.assertEqual(
                self._testScript("from Products.stripogram import html2safehtml\nreturn html2safehtml('<i>hello</i>')"),
                '<i>hello</i>'
                )
                                 
            
        def test_ScriptPython_html2text(self):
            self.assertEqual(
                self._testScript("from Products.stripogram import html2text\nreturn html2text('<i>hello</i>')"),
                'hello'
                )
        def test_SomethingBad(self):
            # test we can't import something nasty
            try:
                self._testScript("from Products.stripogram import HTML2Text")
            except:
                pass
            else:
                self.fail("managed to import HTML2TExt")

def test_suite():
    return TestSuite((
        makeSuite( stripogramTests ),
        makeSuite( ZopeTests ),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')
                                
