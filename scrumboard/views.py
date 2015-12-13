from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from scrumboard.models import Item


class ScrumboardView(ListView):
    """
    This View will combine current sprint scrumboard with data like charts, statistics.
    """
    model = Item
    template_name = 'scrumboard/scrumboard.html'
    context_object_name = 'all_items'


class ItemListView(ListView):
    """
    Subject to be removed.
    """
    model = Item
    context_object_name = 'all_items'


class ItemDetailView(DetailView):
    """
    Detailed information about the Item.
    """
    model = Item
    context_object_name = 'item'


class ItemCreateView(CreateView):
    """
    Create new Item instance in separate form.
    """
    model = Item
    fields = '__all__'


class ItemUpdateView(UpdateView):
    """
    Update Item instance in separate form.
    """
    model = Item
    fields = '__all__'

    def get_object(self, queryset=None):
        return Item.objects.get(pk=self.kwargs['pk'])


class ItemDeleteView(DeleteView):
    """
    Remove selected Item from application
    """
    model = Item
    success_url = reverse_lazy('scrumboard:index')

    def get_object(self, queryset=None):
        return Item.objects.get(pk=self.kwargs['pk'])
