from django.contrib.auth.models import User
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Professor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name) + '-' + str(self.age) + '-' + str(self.department)

    def get_absolute_url(self):
        return reverse('professors:detail',kwargs={'pk':self.pk})


class Prof_Rating(models.Model):
    comment = models.CharField(max_length=1000)
    stars = models.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    postAnonymously = models.BooleanField(default=False)

    def __str__(self):
        return str(self.comment) + '-' + str(self.stars)

    def get_absolute_url(self):
        return reverse('professors:detail',kwargs={'pk':self.professor.pk})


