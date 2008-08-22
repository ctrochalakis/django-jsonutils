import logging
import urllib
import urllib2
from urlparse import urljoin
import simplejson
log = logging.getLogger(__name__)

class BaseClient(object):
    "A command line client to interact with a web app through json"

    def __init__(self, baseURL, format='json', post_name='json',debug=False):
        if baseURL[-1] != '/':
            baseURL = baseURL +'/'
        self.baseURL = baseURL
        self.format = format
        self.post_name = post_name

        # Setup our logger
        logHandler = logging.StreamHandler()
        if debug:
            log.setLevel(logging.DEBUG)
            logHandler.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
            logHandler.setLevel(logging.INFO)

        format = logging.Formatter("%(message)s")
        logHandler.setFormatter(format)
        log.addHandler(logHandler)

    def _send_request(self, method, req_params):
        url = urljoin(self.baseURL, method + '/'+ '?format=%s' % self.format)

        log.debug("Requesting %s" % url)
        
        req = urllib2.Request(url)
        req.add_header('Accept', 'text/javascript')

        if req_params:
            post_data = { self.post_name : simplejson.dumps(req_params) }
            req.add_data(urllib.urlencode(post_data))

        response = urllib2.urlopen(req)
        json_response = response.read()
        data = simplejson.loads(json_response)
        return data
