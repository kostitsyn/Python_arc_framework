import sys
import re
sys.path.append('../')

# Front controllers
def set_key(request):
    request['secret_key'] = 'KEY'


def set_language(request):
    request['language'] = 'LANGUAGE'


def user_authorize(request):
    request['is_authorize'] = True


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        print(path)
        check_html = len(re.findall(r'html.*', path))
        if check_html:
            check_slash = len(re.findall(r'/$', path))
            if check_slash:
                result = re.match(r'^.+l', path)
                path = result.group(0)
            if path.count('html') >= 2:
                path = path.split('/')
                path = ['/', path[-1]]
                path = ''.join(path)
        else:
            check_slash = len(re.findall(r'/$', path))
            if not check_slash:
                path = path.split()
                path.append('/')
                path = ''.join(path)
        print(path)
        requests = {}
        for front_view in self.fronts:
            front_view(requests)
        if path in self.routes:
            view = self.routes[path]
            code, text_response = view(requests)
        else:
            code, text_response = '404 ERROR', 'Page not found!'
        start_response(code, [('Content-Type', 'text/html')])
        return [text_response.encode('utf-8')]

