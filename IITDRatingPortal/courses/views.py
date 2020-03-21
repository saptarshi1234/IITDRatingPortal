from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import ReviewPostForm
from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'courses/index.html'
    context_object_name = 'all_courses'

    def get_queryset(self):
        return Course.objects.all()


class DetailView(generic.DetailView):
    model = Course
    template_name = 'courses/details.html'
    context_object_name = 'course'


class CourseRatingCreate(CreateView):
    model = Course_Rating
    form_class = ReviewPostForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class CourseRatingDelete(DeleteView):
    model = Course_Rating
    success_url = reverse_lazy('courses:index')
