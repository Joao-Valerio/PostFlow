from .models import AuditLog


class AuditLogMiddleware:
    """Middleware para interceptar ações críticas do usuário."""

    TRACKED_PATHS = {
        "/accounts/login/": AuditLog.Action.LOGIN,
        "/accounts/logout/": AuditLog.Action.LOGOUT,
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self._maybe_log(request)
        return response

    def _maybe_log(self, request):
        action = self.TRACKED_PATHS.get(request.path)
        if not action or request.method != "POST":
            return

        user = request.user if request.user.is_authenticated else None
        organization = getattr(user, "organization", None) if user else None

        AuditLog.objects.create(
            user=user,
            organization=organization,
            action=action,
            resource_type="session",
            description=f"Ação registrada em {request.path}",
            ip_address=self._get_client_ip(request),
        )

    @staticmethod
    def _get_client_ip(request):
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded:
            return x_forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
