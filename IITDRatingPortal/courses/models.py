from django.contrib.auth.models import User
from django.db import models
from users.models import *

from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from datetime import datetime
from django.utils.timezone import now

from professors.models import Professor


class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    profs_teaching = models.ManyToManyField(Professor,related_name='all_courses_taught')

    def __str__(self):
        return str(self.name) + '-' + str(self.department)

    def get_absolute_url(self):
        return reverse('courses:detail',kwargs={'pk':self.pk})


class Course_Rating(Rating):
    datetime = models.DateTimeField(default=datetime.now)
    comment = models.CharField(max_length=1000)
    stars = models.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    postAnonymously = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User, related_name='all_liked_courserating')
    reported = models.BooleanField(default=False)
    last_reported_time = models.DateTimeField(default=now,blank=True)

    def __str__(self):
        return str(self.comment) + '-' + str(self.stars)

    def get_absolute_url(self):
        return reverse('courses:detail',kwargs={'pk':self.course.pk})+'#'+ str(self.id)

    def get_class_name(self):
        return 'course_rating'
