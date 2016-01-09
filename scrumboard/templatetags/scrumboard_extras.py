from django import template

register = template.Library()


@register.inclusion_tag('scrumboard/extras/item_form.html')
def fancy_item_form(form):
    return {'form': form}


@register.inclusion_tag('scrumboard/extras/item_full.html')
def fancy_item_detail(item):
    return {'item': item}


@register.inclusion_tag('scrumboard/extras/item_short.html')
def item_detail_short(item):
    return {'item': item}


@register.inclusion_tag('scrumboard/extras/item_text_url.html')
def item_url(item, text=None):
    return {
        'item': item,
        'text': text or item.name
    }


@register.inclusion_tag('scrumboard/extras/sprint_text_url.html')
def sprint_url(sprint):
    return {'sprint': sprint}
