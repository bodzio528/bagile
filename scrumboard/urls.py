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
            url(r'^$', ItemDetailView.as_view(), name='item_details'),
            url(r'^update/$', ItemUpdateView.as_view(), name='item_update'),
            url(r'^delete/$', ItemDeleteView.as_view(), name='item_delete'),
        ])),
    ]))
]
