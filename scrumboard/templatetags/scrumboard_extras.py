from django import template

register = template.Library()


@register.inclusion_tag('scrumboard/extras/item_form.html')
def scrumboard_item_form(form):
    return {'form': form}


@register.inclusion_tag('scrumboard/extras/item_full.html')
def scrumboard_item_full(item):
    return {'item': item}


@register.inclusion_tag('scrumboard/extras/item_short.html')
def scrumboard_item_short(item):
    return {'item': item}


@register.inclusion_tag('scrumboard/extras/item_text_url.html')
def scrumboard_item_url(item, text=None):
    return {
        'item': item,
        'text': text or item.name
    }


@register.inclusion_tag('scrumboard/extras/sprint_text_url.html')
def scrumboard_sprint_url(sprint):
    return {'sprint': sprint}


@register.inclusion_tag('scrumboard/extras/sprint_active_select.html', takes_context=True)
def scrumboard_sprint_active_select(context):
    from django.forms import model_to_dict
    from scrumboard.models import Sprint

    active_sprints = [model_to_dict(sprint, fields=['id', 'name']) for sprint in Sprint.objects.all()]

    if 'current_sprint_pk' in context.request.session:
        current_sprint = Sprint.objects.get(pk=context.request.session['current_sprint_pk'])
    else:
        current_sprint = Sprint.get_current_sprint()

    return {'active_sprints': active_sprints, 'current_sprint': model_to_dict(current_sprint), 'current_url': context.request.get_full_path()}

