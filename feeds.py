from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import urllib
import os
import cgi

#cfeed info
consumer_key = '3MVG98XJQQAccJQcNdyHKdTAAktiZJU3MEJAH3gCfQqOl9xoAc_TUky1UMRDzxLvxgRp9GOCxQFmxYKDtvwZF'
consumer_secret    ='1542233998658503107'
redirect_uri = 'https://feedtest0.appspot.com/callback'



class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'json_ajax.html')
        self.response.out.write(template.render(path, template_values))
        
class OutputJSON(webapp.RequestHandler):
    def get(self):
        title = self.request.get('title').encode('UTF-8')
        link = self.request.get('link').encode('UTF-8')
        res = '{"title":"%s", "link":"%s"}' % (title, link)
        self.response.out.write(cgi.escape(unicode(res, 'UTF-8')))

class Block(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'json_block.html')
        self.response.out.write(template.render(path, template_values))
        
class Demo(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'demo.html')
        self.response.out.write(template.render(path, template_values))
                    
class NextPage(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('NextPage!')

class SignIn(webapp.RequestHandler):
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
            
class CallBack(webapp.RequestHandler):
    def get(self):
        pass

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/OutputJSON',OutputJSON),
                                      ('/block', Block),
                                      ('/demo', Demo),
                                      ('/next', NextPage),
                                      ('/signin', SignIn),
                                      ('/callback', CallBack)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
