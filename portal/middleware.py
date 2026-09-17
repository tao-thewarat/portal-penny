from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.shortcuts import redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme


class RedirectAuthenticatedFromLoginMiddleware:
    login_view_names = frozenset({"discord_login"})

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (
            not request.user.is_authenticated
            or request.resolver_match.view_name not in self.login_view_names
            or request.GET.get("process") == "connect"
            or not SocialAccount.objects.filter(
                user=request.user, provider="discord"
            ).exists()
        ):
            return None

        next_url = request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
