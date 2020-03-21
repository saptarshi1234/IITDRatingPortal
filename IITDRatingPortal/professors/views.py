from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import ReviewPostForm
from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'professors/index.html'
    context_object_name = 'all_profs'

    def get_queryset(self):
        return Professor.objects.all()


class DetailView(generic.DetailView):
    model = Professor
    template_name = 'professors/details.html'
    context_object_name = 'prof'


class ProfRatingCreate(CreateView):
    model = Prof_Rating
    form_class = ReviewPostForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class ProfRatingDelete(DeleteView):
    model = Prof_Rating
    success_url = reverse_lazy('professors:index')
