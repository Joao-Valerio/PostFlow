import uuid

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.utils.text import slugify

from .models import CustomUser, Organization

INPUT_CLASS = "form-control input"


class SignupForm(UserCreationForm):
    organization_name = forms.CharField(
        label="Nome da organização",
        max_length=255,
        required=True,
        help_text="Será criada uma nova organização para sua conta.",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "autocomplete": "organization"}),
    )
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "autocomplete": "email"}),
    )
    first_name = forms.CharField(
        label="Nome",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "autocomplete": "given-name"}),
    )
    last_name = forms.CharField(
        label="Sobrenome",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "autocomplete": "family-name"}),
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "organization_name",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={"class": INPUT_CLASS, "autocomplete": "username"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": INPUT_CLASS, "autocomplete": "new-password"},
        )
        self.fields["password2"].widget.attrs.update(
            {"class": INPUT_CLASS, "autocomplete": "new-password"},
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.role = CustomUser.Role.ADMIN

        org_name = self.cleaned_data["organization_name"]
        base_slug = slugify(org_name) or "org"
        slug = base_slug
        while Organization.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

        organization = Organization.objects.create(name=org_name, slug=slug)
        user.organization = organization

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário ou e-mail",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "autocomplete": "current-password"}),
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "last_name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS}),
        }


class StyledPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "autocomplete": "email"}),
    )


class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": INPUT_CLASS})


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": INPUT_CLASS})
