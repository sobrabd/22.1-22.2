from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Category, Dog
from django.urls import reverse_lazy, reverse
from .forms import DogForm, ParentForm


class IndexView(TemplateView):
    template_name = 'dogs/index.html'
    extra_context = {
        'title': 'Питомник - Добро пожаловать',
    }

    def get_context_data(self, **kwargs: Any):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]
        return context_data


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Питомник - Наши породы'
    }


class DogListView(ListView):
    model = Dog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['object_list'] = Dog.objects.filter(category_id=category_item.pk)
        context_data['title'] = f'Все собаки породы {category_item.name}'

        return context_data


class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy('dogs:categories')


class DogUpdateView(UpdateView):
    model = Dog
    fields = ('name', 'category')

    def get_success_url(self):
        return reverse('dogs:category_dogs', args=[self.object.category.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            formset = ParentForm(self.request.POST)
        else:
            formset = ParentForm(initial={"dog": self.object.pk, "category": self.object.category.id})

        context_data['parent_form'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        parent_form = context_data['parent_form']
        self.object = form.save()
        if parent_form.is_valid():
            parent_form.product = self.object
            parent_form.save()

        return super().form_valid(form)


class DogDeleteView(DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:categories')
