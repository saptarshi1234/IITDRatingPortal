from django.contrib.auth.decorators import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import *
from .models import *

def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper
def user_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return not self.request.user.is_anonymous

        return WrappedClass
    return wrapper

class IndexView(generic.ListView):
    template_name = 'professors/index.html'
    context_object_name = 'all_profs'

    def get_queryset(self):
        return Professor.objects.all()


class DetailView(generic.DetailView):
    model = Professor
    template_name = 'professors/details.html'
    context_object_name = 'prof'

@superuser_required()
class ProfCreate(CreateView):
    model = Professor
    fields = ('name', 'age', 'department')

@superuser_required()
class ProfUpdate(UpdateView):
    model = Professor
    fields = ('name', 'age', 'department')

@user_required()
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



@login_required
def upvote(request, pk):
    rating = Prof_Rating.objects.get(id=pk)
    if request.user in rating.liked_by.all():
        return HttpResponse('a user can upvote a post only once')
    rating.liked_by.add(request.user)
    if not rating.postAnonymously:
        rating.user.userprofile.respect_points += 1
    rating.user.save()
    rating.save()
    return HttpResponseRedirect(rating.get_absolute_url())
    # return redirect('professors:detail',kwargs={'pk':rating.professor.pk})

@login_required
def downvote(request, pk):
    rating = Prof_Rating.objects.get(id=pk)
    if request.user not in rating.liked_by.all():
        return HttpResponse('a user can only remove his upvotes not downvote')
    rating.liked_by.remove(request.user)
    if not rating.postAnonymously:
        rating.user.userprofile.respect_points -= 1
    rating.user.save()
    rating.save()
    return HttpResponseRedirect(rating.get_absolute_url())
    # return redirect('professors:detail',kwargs={'pk':rating.professor.pk})

@user_passes_test(lambda u:u.is_superuser)
def delete_rating(request, pk):
    review = Prof_Rating.objects.get(id=pk)
    # if not review.postAnonymously:
    #     review.user.userprofile.respect_points -= 1
    review.delete()
    review.user.save()
    warning_message = 'U r being warned for creating offensive post on professor ' + review.professor.name + '\nComment : ' + review.comment + '\n Such behaviour shall not be tolerated and u may be banned for further acts'
    warning = UserWarning.objects.create(user=review.user, message=warning_message, time=datetime.now())
    return HttpResponseRedirect(review.professor.get_absolute_url())

@login_required
def report_rating(request, pk):
    review = Prof_Rating.objects.get(id=pk)
    review.reported = True
    review.last_reported_time = datetime.now()
    review.save()
    return HttpResponseRedirect(review.get_absolute_url())

@user_passes_test(lambda u:u.is_superuser)
def unmark_rating(request,pk):
    review = Prof_Rating.objects.get(id=pk)
    review.reported = False
    review.save()
    return HttpResponseRedirect(reverse('users:show_profile'))
