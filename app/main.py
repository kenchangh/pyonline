##########

import re
import sys
import json
import logging
from urllib import urlencode

import webapp2
from webapp2 import Route
from google.appengine.api import memcache

from StringIO import StringIO

from base_handler import BaseHandler

##########

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

##########

class FrontPage(BaseHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        pass


class Processor(BaseHandler):
    """
    Processes code in a sanbox environment.
    Sends the response back in plain text.

    Each user will need to access the API with a user_id, which is
    generated on the client's side. 
    EXAMPLE: http:/www.pyonline.appspot/<user_id>

    The code will be sent via a POST request in a url encoded manner.
    Then, accessed at the same url with a GET request.
    EXAMPLE:
    >> import urllib, urllib2
    >> Urlencode key-value pair, where key must be 'code'
    >> data = { 'code': "print 'hello world'" }
    >> data = urlencode(data)
    >> # Send POST request with extra data parameter in urlopen
    >> urlopen('http://www.pyonline.appspot/userid', data)
    >> result = urlopen('http://www.pyonline.appspot/userid')
    >> result.read()
    hello world
    """
    # To avoid changing local variables
    def sandbox(self, code):
        buffer = StringIO()
        sys.stdout = buffer
        exec code
        sys.stdout = sys.__stdout__
        result = buffer.getvalue()
        return result

    def valid_id(self, user_id):
        regex = re.compile(r'^[a-zA-Z0-9]{8}$')
        match = regex.match(user_id)
        if match:
            return True
        else:
            return False
    
    def get(self, **kw):
        user_id = kw['user_id']
        result = memcache.get(user_id)
        logging.info(result)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(result)

    def post(self, **kw):
        user_id = kw['user_id']
        if self.valid_id(user_id):
            code = self.request.get('code')
            try:
              result = self.sandbox(code)
            except Exception, error:
                result = 'ERROR: ' + str(error)
            logging.info(result)
            memcache.set(user_id, result)
            self.response.set_cookie('output', result)
        else:
            self.error(500)
            
##########

app = webapp2.WSGIApplication([
      ('/', FrontPage),
      Route('/process/<user_id>', handler = Processor)],
      config = config, debug = True)

if __name__ == '__main__':
    app.run()
    
