from jinja2 import Template


def render(template_name, **kwargs):
    """
    Создать шаблонизатор для HTML страниц, используя jinja.
    :param template_name:
    :param kwargs:
    :return:
    """
    with open(f'templates/{template_name}', encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)

