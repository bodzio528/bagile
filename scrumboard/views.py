from django.views import generic

from scrumboard.models import Item


class ItemListView(generic.ListView):
    template_name = 'scrumboard/items_list.html'
    context_object_name = 'all_items'

    def get_queryset(self):
        return Item.objects.all()


class ItemDetailView(generic.DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'scrumboard/item_details.html'
