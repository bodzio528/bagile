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

    active_sprints = [model_to_dict(sprint, fields=['id', 'name']) for sprint in Sprint.get_active_sprints()]

    if 'current_sprint_pk' in context.request.session:
        current_sprint = Sprint.objects.get(pk=context.request.session['current_sprint_pk'])
    else:
        current_sprint = Sprint.get_current_sprint()

    return {'active_sprints': active_sprints,
            'current_sprint': model_to_dict(current_sprint),
            'current_url': context.request.get_full_path()}


@register.simple_tag
def style_background_color(color):
    from django.utils.safestring import mark_safe
    return mark_safe('style="background-color: {0}"'.format(color))


@register.inclusion_tag('scrumboard/extras/chart_burndown.html')
def scrumboard_chart_burndown(sprint):
    from scrumboard.models import Event
    timetable = Event.get_events_timetable(sprint)

    from datetime import timedelta, date

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def iso_date(single_date):
        return single_date.strftime("%Y-%m-%d")

    tomorrow = date.today() + timedelta(days=1)

    labels1 = [iso_date(single_date) for single_date in daterange(sprint.start_date, tomorrow)]  # TODO: if not single_date in sprint.excluded_days()
    labels2 = [iso_date(single_date) for single_date in daterange(tomorrow, sprint.end_date + timedelta(days=1))]

    from itertools import accumulate
    dataset_burndown = list(accumulate([sum(timetable[l]) for l in labels1]))

    sprint_length = int((sprint.end_date - sprint.start_date).days)  # TODO: sprint.length() that takes free days into account
    dataset_prognosis = [sprint.capacity*(1.0 - x/sprint_length) for x in range(sprint_length)] + [0]

    return {'sprint': sprint,
            'labels': labels1 + labels2,
            'dataset_burndown': dataset_burndown,
            'dataset_prognosis': dataset_prognosis}
