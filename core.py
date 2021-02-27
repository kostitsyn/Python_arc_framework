import sys

import urllib

from wsgiref.util import setup_testing_defaults
sys.path.append('../')
# from views import main_view

# Front controllers
def set_key(request):
    request['secret_key'] = 'KEY'


def set_language(request):
    request['language'] = 'LANGUAGE'


def user_authorize(request):
    request['is_authorize'] = True


class Application:
    """Класс создающий объект для запуска сервера."""
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        # print(f'Словарь урлов: {self.routes}')
        setup_testing_defaults(environ)
        path = environ['PATH_INFO']
        # print(environ)
        requests = {}

        request_type = environ['REQUEST_METHOD']
        # print(f'Тип запроса: {request_type}')
        requests['method'] = request_type

        # Если тип запроса POST
        if request_type == 'POST':
            data = self.get_post_data(environ)
            requests['data'] = data
            # print(f'Полученные данные: {data}')

        # Если тип запроса GET c параметрами
        if environ["QUERY_STRING"]:
            data = self.get_data(environ)
            requests['data'] = data
            # print(f'Полученные данные: {data}')

        if not path.endswith('/'):
            path = path + '/'

        for front_view in self.fronts:
            front_view(requests)
        if path in self.routes:
            view = self.routes[path]
            code, text_response = view(requests)
        else:
            code, text_response = '404 ERROR', 'Page not found!'
        start_response(code, [('Content-Type', 'text/html')])
        return [text_response.encode('utf-8')]


    def get_post_data(self, environ: dict) -> dict:
        """
        Получить параметры POST запроса в виде словаря, где ключ - название
        параметра, значение - соответствующее этому ключу значение.
        :param environ:
        :return:
        """
        contnent_length_data = environ['CONTENT_LENGTH']
        content_length = int(contnent_length_data) if contnent_length_data\
            else 0
        string_bytes = environ['wsgi.input'].read(content_length) if\
            content_length else b''
        query_string = string_bytes.decode('utf-8')
        data = self.parse_string(query_string)
        return data

    def get_data(self, environ: dict) -> dict:
        """
        Получить параметры GET запроса в виде словаря, где ключ - название
        параметра, значение - соответствующее этому ключу значение.
        :param environ:
        :return:
        """
        query_string = environ['QUERY_STRING']
        data = self.parse_string(query_string)
        return data

    def parse_string(self, string: str) -> dict:
        """
        Преобразовать строку с параметрами в словарь.
        :param string:
        :return:
        """
        data = urllib.parse.parse_qs(string, encoding='utf-8')
        data = {key: value[0] for key, value in data.items()}
        return data


class DebugApplication(Application):
    def __init__(self, routes, fronts):
        self.application = Application(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, environ, start_response):
        print('/\/\/\/\/\/\/\/\/\/\/\/\/\Режим ОТЛАДКИ/\/\/\/\/\/\/\/\/\/\/\/\/\\')
        print(f'Тип запроса: {environ["REQUEST_METHOD"]}\nЕго параметры: {environ}')
        return super().__call__(environ, start_response)


class FakeApplication(Application):
    def __call__(self, environ, start_response):
        code, text_response = '200 OK', '<h1>Hello from Fake</h1>'
        start_response(code, [('Content-Type', 'text-html')])
        return [text_response.encode('utf-8')]



