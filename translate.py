__author__ = 'GongLi'

import urllib2
import urllib
import xml.etree.ElementTree as ET

def crawlYoudao(queryword):
    url = "http://dict.yodao.com/search?keyfrom=dict.python&q=" + queryword + "&xmlDetail=true&doctype=xml"
    return urllib2.urlopen(url).read();

def parseXML(xml):

    tree = ET.fromstring(xml)
    phonetic = tree.findall('phonetic-symbol')[0].text
    translation = tree.findall('custom-translation')[0].findall('translation')[0].findall('content')[0].text

    return phonetic, translation

def translate(word):
    return parseXML(crawlYoudao(word))

if __name__ == "__main__":

     print translate("hello")
