from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, TaskList

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        first_task_id = TaskList.objects.filter(user=self.request.user)[0].id
        return reverse_lazy('task-list', args=[first_task_id])


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class ToDoList(LoginRequiredMixin, ListView):
    model = TaskList
    context_object_name = 'task_lists'
    template_name = 'base/task_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_lists"] = TaskList.objects.filter(user=self.request.user)
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task_lists'] = context['task_lists'].filter(title__startswith=search_input)
            
        context['search_input'] = search_input
        return context


class ToDoListdetail(LoginRequiredMixin, DetailView):
    model = TaskList
    context_object_name = 'task_list'
    template_name = 'base/task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_lists"] = TaskList.objects.filter(user=self.request.user)
        context['tasks'] = Task.objects.filter(task_list=context['task_list'].id)
        context['task_count'] = context['tasks'].filter(complete=False).count()
        context['current_list'] = self.object.id
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task_lists'] = context['task_lists'].filter(title__startswith=search_input)
            
        context['search_input'] = search_input
        return context


class ToDoListCreate(LoginRequiredMixin, CreateView):
    model = TaskList
    fields = ['title']
    template_name = 'base/task_form.html'

    def get_success_url(self):
        return reverse_lazy('task-list', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_lists"] = TaskList.objects.filter(user=self.request.user)
        context['header'] = 'Task list create'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ToDoListCreate, self).form_valid(form)


class ToDoListUpdate(LoginRequiredMixin, UpdateView):
    model = TaskList
    fields = ['title']
    template_name = 'base/task_form.html'

    def get_success_url(self):
        return reverse_lazy('task-list', args=[self.object.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_lists"] = TaskList.objects.filter(user=self.request.user)
        context['header'] = 'Edit task list'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ToDoListUpdate, self).form_valid(form)  


class ToDoListDelete(LoginRequiredMixin, DeleteView):
    model = TaskList
    template_name = 'base/task_confirm_delete.html'
    context_object_name = 'task'

    def get_success_url(self):
        first_task_id = TaskList.objects.filter(user=self.request.user)[0].id
        return reverse_lazy('task-list', args=[first_task_id])


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = ['title', 'description', 'complete']

    def get_success_url(self):
        return reverse_lazy('task-list', args=[self.object.task_list.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_lists"] = TaskList.objects.filter(user=self.request.user)
        context['header'] = 'Task create'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task_list = TaskList.objects.get(id=self.kwargs['task_list_id'])
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']

    def get_success_url(self):
        return reverse_lazy('task-list', args=[self.object.task_list.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_lists"] = TaskList.objects.filter(user=self.request.user)
        context['header'] = 'Edit task'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdate, self).form_valid(form)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'

    def get_success_url(self):
        return reverse_lazy('task-list', args=[self.object.task_list.id])