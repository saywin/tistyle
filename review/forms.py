from django import forms

from review.models import ReviewDB


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewDB
        fields = ["text", "grade"]
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Залиште коментар"}
            ),
            "grade": forms.Select(attrs={"class": "form-control"}),
        }
