# -*- coding: utf-8 -*-
#from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app
import webapp2
from google.appengine.ext.webapp import template
import urllib
import urllib2
import os
import cgi
import json

#cfeed info
consumer_key = '3MVG98XJQQAccJQcNdyHKdTAAktiZJU3MEJAH3gCfQqOl9xoAc_TUky1UMRDzxLvxgRp9GOCxQFmxYKDtvwZF'
consumer_secret    ='1542233998658503107'
redirect_uri = 'https://feedtest0.appspot.com/callback'

#GAE
#initialpage = 'http://feedtest0.appspot.com/tile'
#local
initialpage = 'http://localhost:8081/tile'



class JsonAjax(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'json_ajax.html')
        self.response.out.write(template.render(path, template_values))
        
class OutputJSON(webapp2.RequestHandler):
    def get(self):
        title = self.request.get('title').encode('UTF-8')
        link = self.request.get('link').encode('UTF-8')
        res = '{"title":"%s", "link":"%s"}' % (title, link)
        self.response.out.write(cgi.escape(unicode(res, 'UTF-8')))
        
class Demo(webapp2.RequestHandler):
    def get(self):
        template_values = {'name' : 'yosuke'}
        path = os.path.join(os.path.dirname(__file__), 'demo.html')
        self.response.out.write(template.render(path, template_values))

class Tile(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id').encode('UTF-8')
        instance_url = self.request.get('instance_url').encode('UTF-8')
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('tile id:%s,instance_url:%s' % (id,instance_url))
        
        #template_values = {'name' : 'tile demo'}
        #path = os.path.join(os.path.dirname(__file__), 'tile.html')
        #self.response.out.write(template.render(path, template_values))
                    
class NextPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('NextPage!')

class SignIn(webapp2.RequestHandler):
    def get(self):
        auth_url = 'https://login.salesforce.com/services/oauth2/authorize'
        params = {
            'response_type' : 'code',
            'client_id' : consumer_key,
            'redirect_uri': redirect_uri,
        }
        params = urllib.urlencode(params)    
        auth_url = auth_url + '?' + params
        self.redirect(auth_url)
            
class CallBack(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('code').encode('UTF-8')
        auth_url = 'https://login.salesforce.com/services/oauth2/token'
        params = {
            'code' : code,
            'grant_type' : 'authorization_code',
            'client_id' : consumer_key,
            'client_secret' : consumer_secret,
            'redirect_uri': redirect_uri,
        }
        params = urllib.urlencode(params).encode()
        request = urllib2.Request(auth_url)
        request.add_data(params)
        response = urllib2.urlopen(request)
        res = response.read()
        
        data = json.loads(res.decode())
        
        params = {
            'id' : data['id'],
            'instance_url' : data['instance_url'],
            'refresh_token': data['refresh_token'],
            'signature' : data['signature'],
            'access_token' :data['access_token'],
        }
        
        params = urllib.urlencode(params)
        redirect = initialpage + '?' + params                
        self.redirect(redirect) 

        

        
        
app = webapp2.WSGIApplication([('/', SignIn),
                                      ('/ajaxtest',JsonAjax),
                                      ('/OutputJSON',OutputJSON),
                                      ('/demo', Demo),
                                      ('/tile', Tile),
                                      ('/next', NextPage),
                                      ('/signin', SignIn),
                                      ('/callback', CallBack)], debug=True)

'''
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
'''