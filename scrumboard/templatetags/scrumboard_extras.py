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
    data = [("2016-03-01", 54), ("2016-03-02", -3), ("2016-03-03", -5),  ("2016-03-04", -4), ("2016-03-05", -8),
            ("2016-03-09", -8), ("2016-03-10",  5), ("2016-03-06", -11), ("2016-03-12", -5), ("2016-03-13", -13)]
    extra_data = [("2016-03-03", 3), ("2016-03-04", 5), ("2016-03-09", -8)]

    from collections import defaultdict

    timetable = defaultdict(set)
    for item in data + extra_data:
        timetable[item[0]].add(item[1])
    # from scrumboard.models import Event
    # timetable = Event.get_sprint_timetable(sprint)

    from datetime import timedelta, date

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def iso_date(single_date):
        return single_date.strftime("%Y-%m-%d")

    today = date(2016, 3, 10)  # date.today()

    labels1 = [iso_date(single_date) for single_date in daterange(sprint.start_date, today)]  # TODO: if not single_date in sprint.excluded_days()
    labels2 = [iso_date(single_date) for single_date in daterange(today, sprint.end_date)]

    from itertools import accumulate
    dataset_burndown = list(accumulate([sum(timetable[l]) for l in labels1]))

    sprint_length = int((sprint.end_date - sprint.start_date).days)  # TODO: sprint.length() that takes free days into account
    dataset_prognosis = [sprint.capacity*(1.0 - (x + 1)/sprint_length) for x in range(sprint_length)]

    return {'sprint': sprint,
            'labels': labels1 + labels2,
            'dataset_burndown': dataset_burndown,
            'dataset_prognosis': dataset_prognosis}
