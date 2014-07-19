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
from google.appengine.ext import db

from Entity import Page, Article
from translate import translate

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        lst = [1,2,3]
        dict = {"lst": lst}

        q = Page.all()
        q.order("-issueDate")

        for p in q.run():
            print p

        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(dict))

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

        # Find respective Page entity
        page_k = db.Key.from_path('Page', issue+page)
        page = db.get(page_k)
        if not page:
            newPage = Page(key_name=issue+page)
            newPage.issueDate = datetime.strptime(issue, '%Y%m%d')
            newPage.pageNumber = int(page)
            newPage.put()
            page = newPage

        # Find respective Article entity
        article_k = db.Key.from_path('Page', issue+page, 'Article', title)
        article = db.get(article_k)
        if not article:
            article = Article(parent=page, key_name=title)

        if article.englishWords:
            for i in range(len(finalEnglishWords)):
                currentWord = finalEnglishWords[i]
                if not currentWord in article.englishWords:
                    article.englishWords.append(currentWord)
                    article.chineseWords.append(chineseTranslation[i])
                    article.phonetics.append(phonetics[i])
        else:
            article.passageTitle = title
            article.englishWords = finalEnglishWords
            article.chineseWords = chineseTranslation
            article.phonetics = phonetics

        article.updateDate = datetime.now().date()
        article.put()

        print page
        print article

        self.redirect('/index')



appIndex = webapp2.WSGIApplication([
    ('/index', MainHandler)
], debug=True)

appAdd = webapp2.WSGIApplication([
    ('/add', addHandler)
], debug=True)