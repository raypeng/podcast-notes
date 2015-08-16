import re
import sys
import cgi
import codecs

HEADER = '''
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link rel="stylesheet" href="http://ihome.ust.hk/~rpeng/markdown.css" type="text/css" />

'''

def f_link(s):
    ''' [link](url "title") -> <a href="url" title="title">link</a>'''
    def replace_link(tup):
        if tup == None:
            return ""
        title = tup[2].strip()
        text = tup[0]
        url = tup[1]
        if title != None:
            title = title[1:-1]
            return u'<a href="{0}" title="{1}">{2}</a>'.format(url, title, text)
        else:
            return u'<a href="{0}>{1}</a>'.format(url, text)

    link_tups = re.findall(r"\[(.*?)\]\((\S+?)(\s*\".*\")?\)", s)
    for tup in link_tups:
        original = u'[{0}]({1}{2})'.format(*tup)
        s = s.replace(original, replace_link(tup))
    return s

def f_heading(s):
    ''' # -> <h1>...</h1> ### -> <h3>...</h3>'''
    match = re.match(r"^\s*(#+)\s*(.+)\s*$", s)
    if match == None:
        return s
    hashes, heading = match.group(1, 2)
    num = len(hashes)
    return u"<h{0}>{1}</h{0}>".format(num, heading)

def f_hr(s):
    ''' --- (>=3 dashes) -> <hr>'''
    match = re.match(r"^\s*([-=]+)\s*$", s)
    if match == None:
        return s
    num = len(match.group(1))
    if num >= 3:
        return "<hr>"
    else:
        return s

def f_bold(s):
    ''' **text** | __text__ -> <b>text</b>'''
    matches = re.findall(r"([\*_]{2}.*?[\*_]{2})", s)
    for match in matches:
        replaced = u"<b>{}</b>".format(match[2:-2])
        s = s.replace(match, replaced)
    return s

def f_italic(s):
    ''' *text* | _text_ -> <i>text</i>'''
    matches = re.findall(r"([\*_].*?[\*_])", s)
    for match in matches:
        replaced = u"<i>{}</i>".format(match[1:-1])
        s = s.replace(match, replaced)
    return s

def f_blockquote(s):
    ''' > -> <blockquote>...</blockquote>
        >> -> <blockquote><blockquote>...</blockquote></blockquote>'''
    match = re.match(r"^(>+)\s*(.*)", s)
    if match == None:
        return s
    num = len(match.group(1))
    s = match.group(2)
    for _ in range(num):
        s = "<blockquote>" + s + "</blockquote>"
    return s

def f_replace(s):
    s = s.strip()
    s = f_blockquote(s)
    # s = cgi.escape(s)
    s = f_heading(s)
    s = f_link(s)
    s = f_hr(s)
    s = f_bold(s)
    s = f_italic(s)
    return s

if len(sys.argv) < 2:
    print "please specify a markdown document"
    infile = sys.argv[1]
    outfile = infile + ".html"
else:
    infile = sys.argv[1]
    try:
        outfile = sys.argv[2]
    except:
        outfile = infile + ".html"

with codecs.open(infile, "r", encoding="utf8") as f:
    mdtext = f.readlines()

mdtext = map(f_replace, mdtext)


with codecs.open(outfile, "w", encoding="utf8") as f:
    f.write(HEADER)
    f.write("\n".join(mdtext))
print "file written to", outfile

