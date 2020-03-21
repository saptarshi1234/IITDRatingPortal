from django import forms
from .models import Course_Rating


class ReviewPostForm(forms.ModelForm):
    class Meta:
        model = Course_Rating
        fields = ('comment', 'stars', 'course','postAnonymously')