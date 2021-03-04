from .templates import render


class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template_name(self):
        return self.template_name

    def render_template_with_context(self, request):
        template_name = self.get_template_name()
        context_data = self.get_context_data()
        return '200 OK', render(template_name, **request, **context_data)

    def __call__(self, request):
        if request['method'] == 'POST':
            print(f'Получено сообщение: {request["data"]}')
        return self.render_template_with_context(request)


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    def get_request_data(self, request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context(request)
        else:
            return super().__call__(request)
