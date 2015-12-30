from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from extra_views import InlineFormSetView

from scrumboard.models import Item, Sprint


class ScrumboardView(TemplateView):
    """
    This View will combine current sprint scrumboard with data like charts, statistics.
    """
    template_name = 'scrumboard/scrumboard.html'

    def get_context_data(self, **kwargs):
        context = super(ScrumboardView, self).get_context_data(**kwargs)

        developers = User.objects.filter(groups__name='developers')

        current_sprint = Sprint.get_current_sprint()  # TODO: from session by default

        assigned_items_in_current_sprint = Item.objects.filter(
                sprint=current_sprint
        ).exclude(
                status__in=[Item.COMMITTED, Item.DONE]
        )

        def select_items_for_user(current_items, user):
            def split_by_status(items):
                return {
                    'WIP': items.filter(status=Item.WIP),
                    'RDY': items.filter(status=Item.PENDING_REVIEW),
                    'REV': items.filter(status=Item.REVIEW),
                    'FIX': items.filter(status=Item.FIX),
                    'EXT': items.filter(status=Item.EXTERNAL_REVIEW),
                    'BLK': items.filter(status=Item.BLOCKED)
                }
            return {
                'user': user,
                'status': split_by_status(current_items.filter(assignee=user))
            }

        assigned_items = [select_items_for_user(assigned_items_in_current_sprint, user) for user in developers]
        unassigned_items = {
            'COMMITTED': Item.objects.filter(status=Item.COMMITTED),
            'DONE': Item.objects.filter(status=Item.DONE)
        }

        context.update(
            sprint=current_sprint,
            assigned_items=assigned_items,
            unassigned_items=unassigned_items
        )

        return context


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
        return Item.objects.get(id=self.kwargs['pk'])


class ItemDeleteView(DeleteView):
    """
    Item delete
    @get:   display confirmation
    @post:  effectively delete
    """
    model = Item
    success_url = reverse_lazy('scrumboard:index')

    def get_object(self, queryset=None):
        return Item.objects.get(id=self.kwargs['pk'])


class SprintCreateView(CreateView):
    """
    Create Sprint as non admin user.
    """
    model = Sprint
    fields = '__all__'


class SprintUpdateView(UpdateView):
    """
    Update Sprint data.
    """
    model = Sprint
    fields = '__all__'

    def get_object(self, queryset=None):
        return Sprint.objects.get(id=self.kwargs['pk'])


class SprintDetailView(DetailView):
    """
    Detailed information about the Sprint.
    """
    model = Sprint
    fields = '__all__'

    def get_object(self, queryset=None):
        return Sprint.objects.get(id=self.kwargs['pk'])


class SprintDeleteView(DeleteView):
    """
    Sprint delete
    @get:   display confirmation
    @post:  effectively delete
    """
    model = Sprint
    success_url = reverse_lazy('scrumboard:index')

    def get_object(self, queryset=None):
        return Sprint.objects.get(id=self.kwargs['pk'])


class SprintPlanningView(InlineFormSetView):
    """
    SprintPlanning a form to add new items to existing sprint.

    Sprint is auto-detected from session or current time.
    """
    model = Sprint
    inline_model = Item
    # context_object_name = 'sprint'
    template_name = 'scrumboard/sprint_planning.html'

    def get_object(self):
        if 'pk' in self.kwargs:
            return Sprint.objects.get(id=self.kwargs['pk'])
        elif 'current_sprint' in self.request.session:
            return self.request.session['current_sprint']
        else:
            return Sprint.get_current_sprint()
