from django.shortcuts import render
from professors.models import Professor
from courses.models import Course
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    return render(request, 'root/home.html', {})


def search(request):
    query = str(request.GET['query']).lower()
    user_match = []
    prof_match = []
    course_match = []

    for prof in Professor.objects.all():
        if prof.name.lower().__contains__(query):
            prof_match.append(prof)

    for course in Course.objects.all():
        if course.name.lower().__contains__(query):
            course_match.append(course)

    for user in User.objects.all():
        if user.username.lower().__contains__(query):
            user_match.append(user)

    return render(request, 'root/search.html', {'prof_match': prof_match, 'course_match': course_match, 'user_match': user_match})
