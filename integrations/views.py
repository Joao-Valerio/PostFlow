from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import SocialAccount


PLATFORMS = SocialAccount.Platform.choices


@login_required
def account_list(request):
    org = request.user.organization
    accounts = org.social_accounts.all() if org else SocialAccount.objects.none()
    connected_platforms = set(accounts.values_list("platform", flat=True))
    return render(
        request,
        "integrations/account_list.html",
        {
            "accounts": accounts,
            "platforms": PLATFORMS,
            "connected_platforms": connected_platforms,
        },
    )


@login_required
def oauth_connect(request, platform):
    valid_platforms = dict(PLATFORMS)
    if platform not in valid_platforms:
        messages.error(request, "Plataforma inválida.")
        return redirect("integrations:account_list")

    return render(
        request,
        "integrations/oauth_mock.html",
        {"platform": platform, "platform_label": valid_platforms[platform]},
    )


@login_required
def oauth_callback(request, platform):
    org = request.user.organization
    if not org:
        messages.error(request, "Organização não encontrada.")
        return redirect("integrations:account_list")

    valid_platforms = dict(PLATFORMS)
    if platform not in valid_platforms:
        messages.error(request, "Plataforma inválida.")
        return redirect("integrations:account_list")

    code = request.GET.get("code")
    if not code:
        messages.error(request, "Autorização cancelada ou inválida.")
        return redirect("integrations:account_list")

    account_id = f"mock-{platform}-{org.id}"
    account, created = SocialAccount.objects.get_or_create(
        organization=org,
        platform=platform,
        account_id=account_id,
        defaults={
            "account_name": f"{valid_platforms[platform]} (Mock)",
            "connected_by": request.user,
        },
    )

    try:
        account.access_token = f"mock-access-{code}"
        account.refresh_token = f"mock-refresh-{code}"
        account.is_active = True
        account.connected_by = request.user
        account.save()
    except ValueError as exc:
        messages.error(request, str(exc))
        return redirect("integrations:account_list")

    if created:
        messages.success(request, f"Conta {valid_platforms[platform]} conectada com sucesso.")
    else:
        messages.success(request, f"Conta {valid_platforms[platform]} reconectada.")

    return redirect("integrations:account_list")


@login_required
@require_POST
def account_disconnect(request, account_id):
    org = request.user.organization
    account = get_object_or_404(SocialAccount, id=account_id, organization=org)
    platform_label = account.get_platform_display()
    account.is_active = False
    account.save(update_fields=["is_active", "updated_at"])
    messages.success(request, f"Conta {platform_label} desconectada.")
    return redirect("integrations:account_list")
