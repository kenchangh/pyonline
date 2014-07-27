##########

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
    
    def get(self, **kw):
        user_id = kw['user_id']
        result = memcache.get(user_id)
        logging.info(result)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(result)

    def post(self, **kw):
        user_id = kw['user_id']
        code = self.request.get('code')
        try:
          result = self.sandbox(code)
        except Exception, error:
          result = str(error)
        logging.info(result)
        memcache.set(user_id, result)
            
##########

app = webapp2.WSGIApplication([
      Route('/<user_id>', handler = Processor)],
      config = config, debug = True)

if __name__ == '__main__':
    app.run()
    
