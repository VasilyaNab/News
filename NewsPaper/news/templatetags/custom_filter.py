import re
from django import template

register = template.Library()

@register.filter
def censor(text):
    if not isinstance(text, str):
        return text
    bad = ['помидорка', 'помидорки', 'ягодка']
    for word in bad:
        text = re.sub(r'(?i){}'.format(re.escape(word)), '*' * len(word), text)
    return text