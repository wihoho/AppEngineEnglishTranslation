#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from datetime import datetime
import webapp2
import jinja2
from google.appengine.ext import ndb

from Entity import Article
from translate import translate
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        lst = [1,2,3]
        dict = {"lst": lst}

        q = Article.query().order(-Article.issueDate).order(Article.pageNumber)
        dict = {}

        for p in q:
            keys = dict.keys()
            if p.issueDate not in keys:
                lst = []
                lst.append(p)
                dict[p.issueDate] = lst
            else:
                dict[p.issueDate].append(p)

        allDates = sorted(dict.keys(), reverse=True)
        result = {'issueDates': allDates, 'content': dict }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(result))

class addHandler(webapp2.RequestHandler):
    def post(self):

        issue = self.request.get('issue')
        page = self.request.get('page')
        title = self.request.get('title')

        rawWords= self.request.get('rawWords')
        words = rawWords.split('\n')
        englishWords = []
        for word in words:
            englishWords.append(word.strip(' \r'))

        phonetics = []
        chineseTranslation = []
        finalEnglishWords = []
        for word in englishWords:
            p, t = translate(word)
            if not p or not t:
                continue

            phonetics.append(p)
            chineseTranslation.append(t)
            finalEnglishWords.append(word)

        # Find relevant page
        issueDate = datetime.strptime(issue, '%Y%m%d')
        q = Article.query(ndb.AND(ndb.AND(Article.issueDate == issueDate, Article.pageNumber == int(page)), Article.passageTitle == title))
        if q.count() == 0:
            article = Article()
            article.issueDate = issueDate
            article.pageNumber = int(page)
            article.passageTitle = title
            article.englishWords = finalEnglishWords
            article.phonetics = phonetics
            article.chineseWords = chineseTranslation

            article.put()
        else:
            tempArticle = q.fetch()[0]
            for i in range(len(finalEnglishWords)):
                singleWorld = finalEnglishWords[i]
                if singleWorld not in tempArticle.englishWords:
                    tempArticle.englishWords.append(singleWorld)
                    tempArticle.phonetics.append(phonetics[i])
                    tempArticle.chineseWords.append(chineseTranslation[i])

            tempArticle.put()

        time.sleep(0.1)
        self.redirect('/index', permanent=True)

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('insert.html')
        self.response.write(template.render())



appIndex = webapp2.WSGIApplication([
    ('/index', MainHandler)
], debug=True)

appAdd = webapp2.WSGIApplication([
    ('/add', addHandler)
], debug=True)

appMain = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)