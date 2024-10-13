from django import template
from django.template.defaultfilters import stringfilter
import markdown2
import bleach

register = template.Library()

@register.filter
@stringfilter
def markdown2html(value):
    # markdown2 を使って Markdown を HTML に変換
    html = markdown2.markdown(value, extras=['tables', 'fenced-code-blocks', 'strike', 'break-on-newline'])

    # bleachで許可するタグと属性のリスト
    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre',
        'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'table', 'thead', 'tbody', 'tr', 'th',
        'td', 'del', 'iframe', 'img', 'br', 'div'
    ]
    allowed_attributes = {
        '*': ['class', 'style'],
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'width', 'height'],
        'iframe': ['src', 'width', 'height', 'allow', 'allowfullscreen', 'frameborder']
    }

    # bleachを使ってサニタイズ（iframeタグも許可）
    html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)

    # カスタマイズ処理
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
            row += 1
            continue

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
