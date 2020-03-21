from django import forms
from .models import Prof_Rating


class ReviewPostForm(forms.ModelForm):
    class Meta:
        model = Prof_Rating
        fields = ('comment', 'stars', 'professor','postAnonymously')