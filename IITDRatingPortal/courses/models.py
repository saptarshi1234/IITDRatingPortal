from django.contrib.auth.models import User
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name) + '-' + str(self.department)

    def get_absolute_url(self):
        return reverse('courses:detail',kwargs={'pk':self.pk})


class Course_Rating(models.Model):
    comment = models.CharField(max_length=1000)
    stars = models.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    postAnonymously = models.BooleanField(default=False)

    def __str__(self):
        return str(self.comment) + '-' + str(self.stars)

    def get_absolute_url(self):
        return reverse('courses:detail',kwargs={'pk':self.course.pk})

