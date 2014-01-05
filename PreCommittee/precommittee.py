import os
import urllib
import json

from google.appengine.api import users

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

ITEMS_STUB = [{
        'id': '111',
        'image': '/files/Page_04.jpg',
        'type': 1,  # request
        'meta': {
            'date': 1386005728648,
            'tables': ['25-001', '26-039']
        }
    },{
        'id': '222',
        'image': '/files/Page_09.jpg',
        'type': 2,  # table
        'meta': {
            'tableNum' : '25-001',
            'transfers' : [{
                        'id' : '1000',
                        'articleId' : '250012',
                        'amount' : '10'
                    }, {
                        'id' : '1002',
                        'articleId' : '100030',
                        'amount' : '15'
                    }
                ]
            }
    },{
        'id': '333',
        'image': '/files/Page_26.jpg',
        'type': 2,  # table
        'meta' : {
            'tableNum' : '26-039',
            'transfers' : [{
                        'id' : '1001',
                        'articleId' : '033009',
                        'amount' : '20'
                    }
                ]
            }
    }]

ITEMS_STUB_NEW = [{
        'id': '111',    
        'image': '/files/Page_04.jpg',
        'type': None
    },{
        'id': '222',
        'image': '/files/Page_09.jpg',
        'type': None
    },{
        'id': '333',
        'image': '/files/Page_26.jpg',
        'type': None
    }]


class MainPage(webapp2.RequestHandler):

   def get(self):

        template_values = {};

        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))


class UploadFile(webapp2.RequestHandler):
    
    def post(self):

        myfile = self.request.get("file");

        # TODO: save file to storage

        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
            'success': 'true', 
            #'content': myfile
            'url': '/files/test1.pdf' # TODO: replace with saved file URL
        } 
        self.response.out.write(json.dumps(obj))


class Committee(webapp2.RequestHandler):
    
    def get(self):

        committeeId = self.request.get("id")

        committee = {
            'id': committeeId,
            'committeeDate': 1389218400000,
            'committee_items': ITEMS_STUB_NEW
        } # TODO: get this object from DB

        if committeeId is None:
           template_values = {}
            # TODO: create a page with a list of all requests
        else:
            template_values = {                
                'committee': committee
            }
            template_name = 'committee.html'

        template = JINJA_ENVIRONMENT.get_template(template_name)
        self.response.write(template.render(template_values))

    def post(self):
        
        comDate = self.request.get("committeeDateVal")
        fileUrl = self.request.get("requestFileUrl")

        # TODO: break pdf to images and save request and its pages to DB
        
        query_params = {'id': '123'}  # TODO:  replace with the created request's ID
        self.redirect('/committee?' + urllib.urlencode(query_params))


class Page(webapp2.RequestHandler):

    def post(self):

        arr = self.request.POST.dict_of_lists()

        # TODO: save post data to DB

        self.response.headers['Content-Type'] = 'application/json'   
        resp = {
            'success': 'true'
            # 'test': arr
        } 
        self.response.out.write(json.dumps(resp))



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/uploadFile', UploadFile),
    ('/committee', Committee),
    ('/page', Page)
], debug=True)