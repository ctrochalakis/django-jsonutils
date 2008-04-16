from django.conf import settings
from django.utils import simplejson as json

class JSONMiddleware(object):
    """
    Checks if `format` GET parameter is set to json and sets request.json
    Also if something is POST'd with the name `json` it deserializes it
    and makes it accessible in request.JSON

    Settings:

    `FORMAT_STRING` : default 'format'
    `JSON_POST_NAME`: default 'json'

    Example use:
    
    url: http://example.com/foo/?format=<FORMAT_STRING>
    request.POST = {'JSON_POST_NAME': '<json data>'}
    """
    def process_request(self, request):
        format_string = getattr(settings, 'FORMAT_STRING', 'format')
        format = request.GET.get(format_string, None)
        if format != 'json':
            request.format = None
            return
        
        request.format = format
        
        post_name = getattr(settings, 'POST_NAME', 'json')
        if request.POST and request.POST.has_key(post_name):
            json_data = request.POST['json']
            request.JSON = json.loads(json_data)

