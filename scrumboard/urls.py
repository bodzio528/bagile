from django.conf.urls import url

from . import views

# in template {% url 'scrumboard:detail' item.id %}
app_name = 'scrumboard'

urlpatterns = [
    url(r'^$', views.ItemListView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.ItemDetailView.as_view(), name='detail'),
]
