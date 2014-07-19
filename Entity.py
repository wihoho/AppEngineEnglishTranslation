__author__ = 'GongLi'

from google.appengine.ext import db

class Page(db.Model):

    issueDate = db.DateProperty()
    pageNumber = db.IntegerProperty()

class Article(db.Model):

    passageTitle = db.StringProperty()

    englishWords = db.JsonProperty()
    phonetics = db.JsonProperty()
    chineseWords = db.JsonProperty()

    updateDate = db.DateTimeProperty()








