from django import template

register = template.Library()


@register.inclusion_tag('scrumboard/item/form_snippet.html')
def fancy_item_form(form):
    return {'form': form}


@register.inclusion_tag('scrumboard/item/detail_snippet.html')
def fancy_item_detail(item):
    return {'item': item}
