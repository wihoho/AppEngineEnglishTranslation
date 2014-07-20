__author__ = 'GongLi'

from google.appengine.ext import ndb

class Article(ndb.Model):

    issueDate = ndb.DateProperty()
    pageNumber = ndb.IntegerProperty()

    passageTitle = ndb.StringProperty()

    englishWords = ndb.StringProperty(repeated=True)
    phonetics = ndb.StringProperty(repeated=True)
    chineseWords = ndb.StringProperty(repeated=True)

    updateDate = ndb.DateTimeProperty(auto_now=True)








