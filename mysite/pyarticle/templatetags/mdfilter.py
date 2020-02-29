from django import template
from django.template.defaultfilters import stringfilter
import markdown

register = template.Library()


@register.filter
@stringfilter
def markdown2html(value):
    md = markdown.Markdown(extensions=['tables', 'nl2br', 'fenced_code'])
    html = md.convert(value)
    lines = html.split("\n")
    result = ""
    id = 0
    for line in lines:
        if len(line) > 4:
            if line[0:4] == "<h1>":
                new_tag = '<h1 id="tag_{}">'.format(id)
                id += 1
                line = new_tag + line[4:]
        result += line

    return result

