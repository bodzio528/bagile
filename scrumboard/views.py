from django.core.urlresolvers import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from scrumboard.models import Item


#homepage
class ScrumboardView(ListView):
    model = Item
    template_name = 'scrumboard/scrumboard.html'
    context_object_name = 'all_items'


class ItemListView(ListView):
    model = Item
    context_object_name = 'all_items'


class ItemDetailView(DetailView):
    model = Item
    context_object_name = 'item'


class ItemCreateView(CreateView):
    model = Item
    fields = '__all__'


class ItemUpdateView(UpdateView):
    model = Item
    fields = '__all__'

    def get_object(self, queryset=None):
        return Item.objects.get(pk=self.kwargs['pk'])


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('scrumboard:index')

    def get_object(self, queryset=None):
        return Item.objects.get(pk=self.kwargs['pk'])
