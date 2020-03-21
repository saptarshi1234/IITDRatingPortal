from django.shortcuts import render, get_object_or_404, redirect
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


def upvote(request, pk):
    rating = Prof_Rating.objects.get(id=pk)
    rating.liked_by.add(request.user)
    rating.user.userprofile.respect_points += 1
    rating.user.userprofile.save()
    return HttpResponseRedirect(reverse('professors:detail', kwargs={'pk': rating.professor.pk}))
    # return redirect('professors:detail',kwargs={'pk':rating.professor.pk})

def downvote(request, pk):
    rating = Prof_Rating.objects.get(id=pk)
    rating.liked_by.remove(request.user)
    rating.user.userprofile.respect_points -= 1
    rating.user.userprofile.save()
    return HttpResponseRedirect(reverse('professors:detail', kwargs={'pk': rating.professor.pk}))
    # return redirect('professors:detail',kwargs={'pk':rating.professor.pk})


def delete_rating(request, pk):
    review = Prof_Rating.objects.get(id=pk)
    review.user.userprofile.respect_points -= 1
    review.delete()
    review.user.userprofile.save()
    return HttpResponseRedirect(reverse('professors:detail', kwargs={'pk': review.professor.pk}))

