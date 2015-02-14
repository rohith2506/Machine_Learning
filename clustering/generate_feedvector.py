import feedparser
import math
import re

feedlist = []
def gen_word_cnt(url):
    feedlist.append(url)
    d = feedparser.parse(url)
    wc = {}
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word] = wc[word] + 1

    print url
    try:
        return d.feed.title,wc
    except AttributeError:
        return "nofeed",wc

def getwords(html):
    txt = re.compile(r'<[^>]+>').sub('',html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word!=' ']

apcount = {}
wordcounts = {}
for feedurl in file('feedlist.txt'):
    title,wc = gen_word_cnt(feedurl)
    wordcounts[title] = wc
    for word,count in wc.items():
        apcount.setdefault(word,0)
        if count > 1:
            apcount[word] = apcount[word] + 1

wordlist = []
for w,bc in apcount.items():
    print w,bc
    frac = float(bc)/len(feedlist)
    wordlist.append(w)

#print wordlist

out = file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')

for blog,wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')
