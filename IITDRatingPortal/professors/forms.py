from django import forms
from .models import *


class ReviewPostForm(forms.ModelForm):
    class Meta:
        model = Prof_Rating
        fields = ('comment', 'stars','postAnonymously')
