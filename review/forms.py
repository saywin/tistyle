from django import forms

from review.models import ReviewDB


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewDB
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"placeholder": "Залиште коментар"})}
