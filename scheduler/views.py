import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django.utils.dateparse import parse_datetime

from .models import Post, ScheduledPost

logger = logging.getLogger(__name__)


def _store_uploaded_media(files):
    media_items = []
    for uploaded in files:
        if not uploaded:
            continue
        saved_path = default_storage.save(
            f"post_media/{uploaded.name}",
            uploaded,
        )
        media_items.append(
            {
                "name": uploaded.name,
                "url": default_storage.url(saved_path),
                "size": uploaded.size,
                "content_type": uploaded.content_type or "",
            }
        )
    return media_items


def _save_post_media(post, form, files):
    uploaded_media = _store_uploaded_media(files)
    existing_media = list(post.media or [])
    remove_urls = set(form.data.getlist("remove_media_urls"))
    kept_media = [item for item in existing_media if item.get("url") not in remove_urls]
    post.media = kept_media + uploaded_media
    post.save(update_fields=["media", "updated_at"])


def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/landing.html")


@login_required
def dashboard(request):
    org = request.user.organization
    stats = {
        "total": 0,
        "scheduled": 0,
        "published": 0,
        "failed": 0,
    }
    chart_labels = []
    chart_data = []
    if org:
        qs = ScheduledPost.objects.filter(post__organization=org)
        stats["total"] = qs.count()
        stats["scheduled"] = qs.filter(status=ScheduledPost.Status.PENDING).count()
        stats["published"] = qs.filter(status=ScheduledPost.Status.PUBLISHED).count()
        stats["failed"] = qs.filter(status=ScheduledPost.Status.FAILED).count()

        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        monthly = (
            qs.filter(created_at__gte=six_months_ago)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        for row in monthly:
            if row["month"]:
                chart_labels.append(row["month"].strftime("%b %Y"))
                chart_data.append(row["count"])

    return render(
        request,
        "core/dashboard.html",
        {
            "stats": stats,
            "chart_labels": json.dumps(chart_labels),
            "chart_data": json.dumps(chart_data),
        },
    )


@login_required
def post_list(request):
    org = request.user.organization
    posts = Post.objects.filter(organization=org) if org else Post.objects.none()
    return render(request, "scheduler/post_list.html", {"posts": posts})


@login_required
def post_create(request):
    org = request.user.organization
    if not org:
        messages.warning(request, "Você precisa pertencer a uma organização para criar posts.")
        return redirect("dashboard")

    from .forms import PostForm

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.organization = org
            post.author = request.user
            post.save()
            _save_post_media(post, form, request.FILES.getlist("media_files"))
            messages.success(request, "Post salvo como rascunho.")
            return redirect("scheduler:post_list")
    else:
        form = PostForm()

    return render(request, "scheduler/post_form.html", {"form": form, "is_edit": False})


@login_required
def post_edit(request, post_id):
    org = request.user.organization
    post = get_object_or_404(Post, id=post_id, organization=org)

    from .forms import PostForm

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            _save_post_media(post, form, request.FILES.getlist("media_files"))
            messages.success(request, "Post atualizado com sucesso.")
            return redirect("scheduler:post_list")
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "scheduler/post_form.html",
        {"form": form, "post": post, "is_edit": True},
    )


@login_required
@require_POST
def post_delete(request, post_id):
    org = request.user.organization
    post = get_object_or_404(Post, id=post_id, organization=org)
    post.delete()
    messages.success(request, "Post excluído com sucesso.")
    return redirect("scheduler:post_list")


@login_required
def post_schedule(request, post_id):
    org = request.user.organization
    post = get_object_or_404(Post, id=post_id, organization=org)

    from .forms import ScheduledPostForm

    accounts = org.social_accounts.filter(is_active=True) if org else []
    if not accounts.exists():
        messages.warning(
            request,
            "Conecte pelo menos uma rede social antes de agendar.",
        )
        return redirect("integrations:account_list")

    if request.method == "POST":
        form = ScheduledPostForm(request.POST)
        form.fields["post"].queryset = Post.objects.filter(organization=org)
        form.fields["social_account"].queryset = accounts
        if form.is_valid():
            schedule = form.save()
            post.status = Post.Status.SCHEDULED
            post.save(update_fields=["status", "updated_at"])
            messages.success(request, "Publicação agendada com sucesso.")
            return redirect("scheduler:calendar")
    else:
        form = ScheduledPostForm(initial={"post": post})
        form.fields["post"].queryset = Post.objects.filter(organization=org)
        form.fields["social_account"].queryset = accounts

    return render(
        request,
        "scheduler/schedule_form.html",
        {"form": form, "post": post},
    )


@login_required
def calendar(request):
    return render(request, "scheduler/calendar.html")


@login_required
@require_GET
def calendar_events(request):
    org = request.user.organization
    if not org:
        return JsonResponse([], safe=False)

    events = []
    schedules = ScheduledPost.objects.filter(post__organization=org).select_related(
        "post",
        "social_account",
    )
    for schedule in schedules:
        platform = schedule.social_account.platform
        events.append(
            {
                "id": str(schedule.id),
                "title": schedule.post.title or schedule.post.content[:40],
                "start": schedule.scheduled_at.isoformat(),
                "classNames": [f"platform-{platform}"],
                "extendedProps": {
                    "status": schedule.status,
                    "platform": platform,
                },
            },
        )
    return JsonResponse(events, safe=False)


@login_required
@require_POST
def calendar_reschedule(request, schedule_id):
    org = request.user.organization
    schedule = get_object_or_404(
        ScheduledPost,
        id=schedule_id,
        post__organization=org,
    )

    try:
        data = json.loads(request.body)
        new_start = data.get("start")
        if not new_start:
            return JsonResponse({"error": "Data inválida."}, status=400)

        parsed = parse_datetime(new_start)
        if not parsed:
            return JsonResponse({"error": "Formato de data inválido."}, status=400)
        schedule.scheduled_at = (
            timezone.make_aware(parsed) if timezone.is_naive(parsed) else parsed
        )
        schedule.save(update_fields=["scheduled_at", "updated_at"])
        return JsonResponse({"ok": True, "id": str(schedule.id)})
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return JsonResponse({"error": str(exc)}, status=400)


@login_required
@require_POST
def schedule_cancel(request, schedule_id):
    org = request.user.organization
    schedule = get_object_or_404(
        ScheduledPost,
        id=schedule_id,
        post__organization=org,
    )
    schedule.status = ScheduledPost.Status.CANCELLED
    schedule.save(update_fields=["status", "updated_at"])

    if not schedule.post.schedules.filter(
        status=ScheduledPost.Status.PENDING,
    ).exists():
        schedule.post.status = Post.Status.DRAFT
        schedule.post.save(update_fields=["status", "updated_at"])

    messages.success(request, "Agendamento cancelado.")
    return redirect("scheduler:history")


@login_required
def history(request):
    org = request.user.organization
    status_filter = request.GET.get("status", "")
    schedules = (
        ScheduledPost.objects.filter(post__organization=org)
        .select_related("post", "social_account")
        .order_by("-scheduled_at")
        if org
        else ScheduledPost.objects.none()
    )

    if status_filter:
        schedules = schedules.filter(status=status_filter)

    paginator = Paginator(schedules, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    query_parts = []
    if status_filter:
        query_parts.append(f"status={status_filter}")
    query_string = "&".join(query_parts)

    return render(
        request,
        "scheduler/history.html",
        {
            "page_obj": page_obj,
            "schedules": page_obj.object_list,
            "status_filter": status_filter,
            "query": query_string,
            "status_choices": ScheduledPost.Status.choices,
        },
    )


def publish_due_posts():
    """Tarefa periódica do Django Q2 — publica posts com horário vencido."""
    now = timezone.now()
    due = ScheduledPost.objects.filter(
        status=ScheduledPost.Status.PENDING,
        scheduled_at__lte=now,
    ).select_related("post", "social_account")

    for schedule in due:
        try:
            schedule.status = ScheduledPost.Status.PUBLISHING
            schedule.save(update_fields=["status", "updated_at"])
            logger.info("Publicação pendente para agendamento %s", schedule.id)
        except Exception as exc:
            schedule.status = ScheduledPost.Status.FAILED
            schedule.error_message = str(exc)
            schedule.retry_count += 1
            schedule.save(
                update_fields=["status", "error_message", "retry_count", "updated_at"],
            )
