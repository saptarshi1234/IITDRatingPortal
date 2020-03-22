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


def upvote(request, pk):
    rating = Course_Rating.objects.get(id=pk)
    rating.liked_by.add(request.user)
    if not rating.postAnonymously:
        rating.user.userprofile.respect_points += 1
    rating.user.save()
    return HttpResponseRedirect(reverse('courses:detail', kwargs={'pk': rating.course.pk}))
    # return redirect('professors:detail',kwargs={'pk':rating.professor.pk})


def downvote(request, pk):
    rating = Course_Rating.objects.get(id=pk)
    rating.liked_by.remove(request.user)
    if not rating.postAnonymously:
        rating.user.userprofile.respect_points -= 1
    rating.user.save()
    return HttpResponseRedirect(reverse('courses:detail', kwargs={'pk': rating.course.pk}))
    # return redirect('professors:detail',kwargs={'pk':rating.professor.pk})


def delete_rating(request, pk):
    review = Course_Rating.objects.get(id=pk)
    if not review.postAnonymously:
        review.user.userprofile.respect_points -= 1
    review.delete()
    review.user.save()
    warning = UserWarning.objects.create(user=review.user, message='U r being warned', time=datetime.now())
    return HttpResponseRedirect(reverse('courses:detail', kwargs={'pk': review.course.pk}))


def report_rating(request, pk):
    review = Course_Rating.objects.get(id=pk)
    review.reported = True
    review.last_reported_time = datetime.now()
    review.save()
    return HttpResponseRedirect(reverse('courses:detail', kwargs={'pk': review.course.pk}))
