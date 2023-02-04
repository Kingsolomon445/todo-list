from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, DeleteView, TemplateView

from .forms import TaskManagerForm
from api.models import Task


class TaskCreateView(FormView):
    template_name = 'add_task.html'
    form_class = TaskManagerForm
    success_url = reverse_lazy('manager:tasks')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('completed')
        return form

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TaskView(ListView):
    template_name = 'index.html'
    model = Task
    context_object_name = 'tasks'
    ordering = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "index"
        return context




class SingleTaskView(FormView, DetailView):
    template_name = 'task.html'
    context_object_name = 'task'
    model = Task
    success_url = reverse_lazy('manager:tasks')
    form_class = TaskManagerForm

    # Adds the form instance to the context repopulating the form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    #   Retrieves the instance using the get_object method and sets it as the instance in the form kwargs.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

class ApiDocView(TemplateView):
    template_name = 'api_doc.html'

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('manager:tasks')