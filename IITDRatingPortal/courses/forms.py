from django import forms
from .models import *


class ReviewPostForm(forms.ModelForm):
    class Meta:
        model = Course_Rating
        fields = ('comment', 'stars','postAnonymously')

