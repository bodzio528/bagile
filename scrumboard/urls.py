from django.conf.urls import url, include

from . import views

# in template: {% url 'scrumboard:detail' item.id %}
# in python: reverse('scrumboard:detail', ...)
app_name = 'scrumboard'

urlpatterns = [
    url(r'^$', views.ScrumboardView.as_view(), name='index'),
    url(r'^item/', include([
        url(r'^$', views.ItemListView.as_view(), name='item_list'),
        url(r'^create/$', views.ItemCreateView.as_view(), name='item_create'),
        url(r'^(?P<pk>[0-9]+)/', include([
            url(r'^$', views.ItemDetailView.as_view(), name='item_details'),
            url(r'^update/$', views.ItemUpdateView.as_view(), name='item_update'),
            url(r'^delete/$', views.ItemDeleteView.as_view(), name='item_delete'),
        ])),
    ]))
]
