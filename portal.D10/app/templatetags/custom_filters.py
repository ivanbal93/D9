from django import template


register = template.Library()

@register.filter()
def censor(value, word:str):
    if word in value:
        value = value.replace(word, '*'*len(word))
    return value