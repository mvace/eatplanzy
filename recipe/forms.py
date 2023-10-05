from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Type your comment...",
                "size": "30",
                "maxlength": "255",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["text"]
