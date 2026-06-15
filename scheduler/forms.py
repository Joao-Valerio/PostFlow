from django import forms

from .models import Post, ScheduledPost

INPUT_CLASS = "form-control input"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "content": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 5}),
        }


class ScheduledPostForm(forms.ModelForm):
    class Meta:
        model = ScheduledPost
        fields = ("post", "social_account", "scheduled_at")
        widgets = {
            "post": forms.Select(attrs={"class": INPUT_CLASS}),
            "social_account": forms.Select(attrs={"class": INPUT_CLASS}),
            "scheduled_at": forms.DateTimeInput(
                attrs={"class": INPUT_CLASS, "type": "datetime-local"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["scheduled_at"].input_formats = [
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
        ]
