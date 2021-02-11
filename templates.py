from jinja2 import Template


def render(template_name, **kwargs):
    with open(f'templates/{template_name}', encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)

