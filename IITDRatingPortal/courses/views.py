from django.contrib.auth.decorators import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from professors.views import superuser_required, user_required
from .forms import *
from .models import *


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

@superuser_required()
class CourseCreate(CreateView):
    model = Course
    fields = ('name', 'department', 'profs_teaching')

@superuser_required()
class CourseUpdate(UpdateView):
    model = Course
    fields = ('name', 'department', 'profs_teaching')    # form_class = CourseCreateForm


@user_required()
class CourseRatingCreate(CreateView):
    model = Course_Rating
    form_class = ReviewPostForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.course=Course.objects.get(pk=self.kwargs.get('pk'))
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())



@login_required
def upvote(request, pk):
    print('obuvi')
    rating = Course_Rating.objects.get(id=pk)
    # print(rating.liked_by.all())
    if request.user in rating.liked_by.all():
        return HttpResponse('a user can upvote a post only once')
    rating.liked_by.add(request.user)
    if not rating.postAnonymously:
        rating.user.userprofile.respect_points += 1
    rating.user.save()
    rating.save()
    print(rating.get_absolute_url())
    return HttpResponseRedirect(rating.get_absolute_url())

@login_required
def downvote(request, pk):
    rating = Course_Rating.objects.get(id=pk)
    if request.user not in rating.liked_by.all():
        return HttpResponse('a user can only remove his upvotes not downvote')
    rating.liked_by.remove(request.user)
    if not rating.postAnonymously:
        rating.user.userprofile.respect_points -= 1
    rating.user.save()
    rating.save()
    return HttpResponseRedirect(rating.get_absolute_url())

@user_passes_test(lambda u: u.is_superuser)
def delete_rating(request, pk):
    review = Course_Rating.objects.get(id=pk)
    # if not review.postAnonymously:
    #     review.user.userprofile.respect_points -= 1
    review.delete()
    review.user.save()
    warning_message='U r being warned for creating offensive post on course '+ review.course.name + '\nComment : '+review.comment +'\n Such behaviour shall not be tolerated and u may be banned for further acts'
    warning = UserWarning.objects.create(user=review.user, message=warning_message, time=datetime.now())
    return HttpResponseRedirect(review.course.get_absolute_url())

@login_required
def report_rating(request, pk):
    rating = Course_Rating.objects.get(id=pk)
    rating.reported = True
    rating.last_reported_time = datetime.now()
    rating.save()
    return HttpResponseRedirect(rating.get_absolute_url())

@user_passes_test(lambda u:u.is_superuser)
def unmark_rating(request,pk):
    rating = Course_Rating.objects.get(id=pk)
    rating.reported = False
    rating.save()
    return HttpResponseRedirect(reverse('users:show_profile'))
