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
    
    def get(self, **kw):
        user_id = kw['user_id']
        result = memcache.get(user_id)
        logging.info(result)
        self.response.headers['Content-Type'] = 'application/json'
        result = {
            'success': result
        }
        self.response.out.write(json.dumps(result))

    def post(self, **kw):
        user_id = kw['user_id']
        pycode = self.request.get('pycode')
        buffer = StringIO()
        sys.sydout = buffer
        exec pycode
        sys.stdout = sys.__stdout__
        result = buffer.getvalue()
        logging.info(result)
        memcache.set(user_id, result)
            
##########

app = webapp2.WSGIApplication([
      Route('/<user_id>', handler = Processor)],
      config = config, debug = True)

if __name__ == '__main__':
    app.run()
    
