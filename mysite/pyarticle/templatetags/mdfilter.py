from django import template
from django.template.defaultfilters import stringfilter
import markdown
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs

register = template.Library()


@register.filter
@stringfilter
def markdown2html(value):
    md = markdown.Markdown(extensions=['tables', 'nl2br', 'fenced_code', 'pymdownx.tilde'], safe_mode='escape')

    html = md.convert(value)
    html = bleach.clean(html, markdown_tags, markdown_attrs)

    lines = html.split("\n")
    result = ""
    id = 0
    row = 0
    skip = False
    while row < len(lines):
        line = lines[row]
        if "<p><img alt=" in line:
            line = line.replace('<p>', '<p align="center">')
            result = result + "\n" + line

        if len(line) >= 11 and line[0:11] == "<pre><code>":
            skip = True
            result = result + "\n" + line
            row += 1
            continue

        if len(line) >= 13 and line[0:13] == '</code></pre>':
            skip = False
            result = result + "\n" + line
            row += 1
            continue

        if len(line) >= 4 and skip == False and line[0:4] == "<h1>":
            new_tag = '<h1 id="tag_{}">'.format(id)
            id += 1
            line = new_tag + line[4:]
            result = result + "\n" + line
        else:
            result = result + "\n" + line
        row += 1
    return result

