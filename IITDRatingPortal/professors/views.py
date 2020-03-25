import _thread
import threading
import time

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import *
from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from users.models import *


class IndexView(generic.ListView):
    template_name = 'professors/index.html'
    context_object_name = 'all_profs'

    def get_queryset(self):
        return Professor.objects.all()


class DetailView(generic.DetailView):
    model = Professor
    template_name = 'professors/details.html'
    context_object_name = 'prof'


class ProfCreate(CreateView):
    model = Professor
    fields = ('name', 'age', 'department')


class ProfUpdate(UpdateView):
    model = Professor
    fields = ('name', 'age', 'department')


class ProfRatingCreate(CreateView):
    model = Prof_Rating
    form_class = ReviewPostForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.professor = Professor.objects.get(pk=self.kwargs.get('pk'))
        print(self.kwargs.get('pk'))
        print(obj.professor)
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class ProfRatingDelete(DeleteView):
    model = Prof_Rating
    success_url = reverse_lazy('professors:index')


def upvote(request, pk):
    rating = Prof_Rating.objects.get(id=pk)
    rating.liked_by.add(request.user)
    if not rating.postAnonymously:
        rating.user.userprofile.respect_points += 1
    rating.user.save()
    return HttpResponseRedirect(reverse('professors:detail', kwargs={'pk': rating.professor.pk}))
    # return redirect('professors:detail',kwargs={'pk':rating.professor.pk})


def downvote(request, pk):
    rating = Prof_Rating.objects.get(id=pk)
    rating.liked_by.remove(request.user)
    if not rating.postAnonymously:
        rating.user.userprofile.respect_points -= 1
    rating.user.save()
    return HttpResponseRedirect(reverse('professors:detail', kwargs={'pk': rating.professor.pk}))
    # return redirect('professors:detail',kwargs={'pk':rating.professor.pk})


def delete_rating(request, pk):
    review = Prof_Rating.objects.get(id=pk)
    # if not review.postAnonymously:
    #     review.user.userprofile.respect_points -= 1
    review.delete()
    review.user.save()
    warning_message = 'U r being warned for creating offensive post on professor ' + review.professor.name + '\nComment : ' + review.comment + '\n Such behaviour shall not be tolerated and u may be banned for further acts'
    warning = UserWarning.objects.create(user=review.user, message=warning_message, time=datetime.now())
    return HttpResponseRedirect(reverse('professors:detail', kwargs={'pk': review.professor.pk}))


def report_rating(request, pk):
    review = Prof_Rating.objects.get(id=pk)
    review.reported = True
    review.last_reported_time = datetime.now()
    review.save()
    # return render(request,'professors/detail',{})
    return HttpResponseRedirect(reverse('professors:detail', kwargs={'pk': review.professor.pk}))

