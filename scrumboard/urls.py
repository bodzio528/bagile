from django.conf.urls import url, include

from scrumboard.views import *

# in template: {% url 'scrumboard:detail' item.id %}
# in python: reverse('scrumboard:detail', ...)
app_name = 'scrumboard'

urlpatterns = [
    url(r'^$', ScrumboardView.as_view(), name='index'),
    url(r'^item/', include([
        url(r'^$', ItemListView.as_view(), name='item_list'),
        url(r'^create/$', ItemCreateView.as_view(), name='item_create'),
        url(r'^(?P<pk>[0-9]+)/', include([
            url(r'^details/$', ItemDetailView.as_view(), name='item_details'),
            url(r'^update/$', ItemUpdateView.as_view(), name='item_update'),
            url(r'^delete/$', ItemDeleteView.as_view(), name='item_delete'),
        ])),
    ])),
    url(r'^sprint/', include([
        url(r'^create/$', SprintCreateView.as_view(), name='sprint_create'),
        url(r'^planning/$', SprintPlanningView.as_view(), name='current_sprint_planning'),
        url(r'^(?P<pk>[0-9]+)/', include([
            url(r'^details/$', SprintDetailView.as_view(), name='sprint_details'),
            url(r'^update/$', SprintUpdateView.as_view(), name='sprint_update'),
            url(r'^delete/$', SprintDeleteView.as_view(), name='sprint_delete'),
            url(r'^planning/$', SprintPlanningView.as_view(), name='sprint_planning')
        ])),
    ])),
]
