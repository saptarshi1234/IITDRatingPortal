from django.contrib.auth.models import User
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone

class Professor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    department = models.CharField(max_length=100)
    #respect_points = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name) + '-' + str(self.age) + '-' + str(self.department)

    def get_absolute_url(self):
        return reverse('professors:detail',kwargs={'pk':self.pk})


class Prof_Rating(models.Model):
    datetime = models.DateTimeField(default=datetime.now)
    comment = models.CharField(max_length=1000)
    stars = models.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    postAnonymously = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User,related_name='all_liked_profrating')
    reported = models.BooleanField(default=False)
    last_reported_time = models.DateTimeField(default=now,blank=True)

    def __str__(self):
        return str(self.comment) + '-' + str(self.stars)

    def get_absolute_url(self):
        return reverse('professors:detail',kwargs={'pk':self.professor.pk})+'#'+ str(self.id)

    def get_class_name(self):
        return 'prof_rating'

