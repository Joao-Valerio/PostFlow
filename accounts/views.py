from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST

from .forms import (
    LoginForm,
    ProfileForm,
    SignupForm,
    StyledPasswordChangeForm,
    StyledPasswordResetForm,
    StyledSetPasswordForm,
)


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/email/password_reset_email.html"
    subject_template_name = "accounts/email/password_reset_subject.txt"
    form_class = StyledPasswordResetForm
    success_url = reverse_lazy("accounts:password_reset_done")


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = StyledSetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = StyledPasswordChangeForm
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Senha alterada com sucesso.")
        return response


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta criada com sucesso. Bem-vindo ao PostFlow!")
            return redirect("dashboard")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = StyledPasswordChangeForm(user=request.user)
    active_tab = request.GET.get("tab", "profile")

    if request.method == "POST":
        action = request.POST.get("action", "profile")

        if action == "profile":
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Perfil atualizado com sucesso.")
                return redirect("accounts:profile")
            active_tab = "profile"

        elif action == "password":
            password_form = StyledPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Senha alterada com sucesso.")
                return redirect(f"{reverse('accounts:profile')}?tab=security")
            active_tab = "security"

    return render(
        request,
        "accounts/profile.html",
        {
            "user_obj": request.user,
            "profile_form": profile_form,
            "password_form": password_form,
            "active_tab": active_tab,
        },
    )


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")
