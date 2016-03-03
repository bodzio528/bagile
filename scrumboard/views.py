from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from django.views.generic import TemplateView, View
from django.views.generic.base import ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from extra_views import InlineFormSetView

from scrumboard.models import Item, Sprint


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


class SessionCurrentSprintMixin(object):
    def get_current_sprint(self):
        if 'pk' in self.kwargs:
            return Sprint.objects.get(id=self.kwargs['pk'])
        elif 'current_sprint_pk' in self.request.session:
            return Sprint.objects.get(id=self.request.session['current_sprint_pk'])
        else:
            return Sprint.get_current_sprint()


class ScrumboardView(SessionCurrentSprintMixin, TemplateView):
    """
    This View will combine current sprint scrumboard with data like charts, statistics.
    """
    template_name = 'scrumboard/scrumboard.html'

    def get_context_data(self, **kwargs):
        context = super(ScrumboardView, self).get_context_data(**kwargs)

        developers = User.objects.filter(groups__name='developers')

        current_sprint = self.get_current_sprint()

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

        unassigned_items_in_current_sprint = Item.objects.filter(sprint=current_sprint)
        unassigned_items = {
            'COMMITTED': unassigned_items_in_current_sprint.filter(status=Item.COMMITTED),
            'DONE': unassigned_items_in_current_sprint.filter(status=Item.DONE)
        }

        context.update(
            sprint=current_sprint,
            assigned_items=assigned_items,
            unassigned_items=unassigned_items,
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


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    Create new Item instance in separate form.
    """
    model = Item
    fields = '__all__'


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update Item instance in separate form.
    """
    model = Item
    fields = '__all__'

    def get_object(self, queryset=None):
        return Item.objects.get(id=self.kwargs['pk'])


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    Item delete
    @get:   display confirmation
    @post:  effectively delete
    """
    model = Item
    success_url = reverse_lazy('scrumboard:index')

    def get_object(self, queryset=None):
        return Item.objects.get(id=self.kwargs['pk'])


class SprintCreateView(LoginRequiredMixin, CreateView):
    """
    Create Sprint as non admin user.
    """
    model = Sprint
    fields = '__all__'


class SprintUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update Sprint data.
    """
    model = Sprint
    fields = '__all__'

    def get_object(self, queryset=None):
        return Sprint.objects.get(id=self.kwargs['pk'])


class SprintDetailView(LoginRequiredMixin, DetailView):
    """
    Detailed information about the Sprint.
    """
    model = Sprint
    fields = '__all__'

    def get_object(self, queryset=None):
        return Sprint.objects.get(id=self.kwargs['pk'])


class SprintDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sprint delete
    @get:   display confirmation
    @post:  effectively delete
    """
    model = Sprint
    success_url = reverse_lazy('scrumboard:index')

    def get_object(self, queryset=None):
        return Sprint.objects.get(id=self.kwargs['pk'])


class SprintPlanningView(LoginRequiredMixin, InlineFormSetView):
    """
    SprintPlanning a form to add new items to existing sprint.

    Sprint is auto-detected from session or current time.
    """
    model = Sprint
    inline_model = Item
    context_object_name = 'sprint'
    template_name = 'scrumboard/sprint_planning.html'

    extra = 0
    max_num = 20
    can_delete = True
    can_order = False

    def get_context_data(self, **kwargs):
        context = super(SprintPlanningView, self).get_context_data(**kwargs)

        estimate_total = 0

        items = Item.objects.filter(sprint=self.get_object())

        for item in items:
            estimate_total += item.estimate_review + item.estimate_work

        context.update(estimate_total=estimate_total)

        return context

    def get_object(self):
        if 'pk' in self.kwargs:
            return Sprint.objects.get(id=self.kwargs['pk'])
        elif 'current_sprint_pk' in self.request.session:
            return Sprint.objects.get(id=self.request.session['current_sprint_pk'])
        else:
            return Sprint.get_current_sprint()


class SprintCurrentView(LoginRequiredMixin, View):
    def get(self, request):
        current_sprint = Sprint.get_current_sprint()

        if 'current_sprint_pk' in request.session:
            session_sprint = Sprint.objects.get(pk=request.session['current_sprint_pk'])
            if session_sprint in Sprint.get_active_sprints():
                current_sprint = session_sprint
            else:
                request.session['current_sprint_pk'] = current_sprint.pk

        from django.http import JsonResponse
        return JsonResponse({'current_sprint': model_to_dict(current_sprint)})

    def post(self, request):
        if 'current_sprint_pk' in request.POST:
            current_sprint = Sprint.objects.get(pk=request.POST['current_sprint_pk'])
            request.session['current_sprint_pk'] = current_sprint.pk
            if 'next' in request.POST:
                from django.shortcuts import redirect
                return redirect(request.POST['next'])
        raise Http404


class SprintActiveView(View):
    def get(self, request):
        from django.http import JsonResponse
        active_sprints = [model_to_dict(sprint, fields=['id', 'name']) for sprint in Sprint.get_active_sprints()]
        return JsonResponse(active_sprints, safe=False)


class SprintBurndownChartView(SessionCurrentSprintMixin, TemplateView):
    template_name = 'scrumboard/sprint_burndown_chart.html'

    def get_context_data(self, **kwargs):
        context = super(SprintBurndownChartView, self).get_context_data(**kwargs)
        context.update(sprint=self.get_current_sprint())
        return context
