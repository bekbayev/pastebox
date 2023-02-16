from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from django import template
from django.utils.safestring import mark_safe

from ..models import Snippet

register = template.Library()


@register.filter(is_safe=True)
def highlight_code(snippet: Snippet) -> str:
    """Return a string with html that the syntax highlights."""
    syntax = snippet.syntax
    code = snippet.body
    lexer = get_lexer_by_name(syntax, encoding="utf-8", stripall=True)
    formatter = HtmlFormatter(linenos="table")
    return mark_safe(highlight(code, lexer, formatter))
