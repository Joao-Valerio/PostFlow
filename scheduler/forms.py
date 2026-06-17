from django import forms

from .models import Post, ScheduledPost

INPUT_CLASS = "form-control input"
PLATFORM_CHOICES = (
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("linkedin", "LinkedIn"),
    ("tiktok", "TikTok"),
)
PLATFORM_LIMITS = {
    "facebook": 63206,
    "instagram": 2200,
    "linkedin": 3000,
    "tiktok": 2200,
}


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PostForm(forms.ModelForm):
    target_platforms = forms.MultipleChoiceField(
        choices=PLATFORM_CHOICES,
        required=False,
        initial=[choice[0] for choice in PLATFORM_CHOICES],
        label="Plataformas de destino",
    )
    media_files = forms.FileField(
        required=False,
        widget=MultiFileInput(
            attrs={
                "class": INPUT_CLASS,
                "multiple": True,
                "accept": "image/*,video/*",
            },
        ),
        label="Mídias",
    )

    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "content": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update({"maxlength": PLATFORM_LIMITS["facebook"]})


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
