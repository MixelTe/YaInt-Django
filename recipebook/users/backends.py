from typing import Any

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext

from users.models import User


class AuthenticationBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> User | None:
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if username is None or password is None:
            return None

        user = None
        if "@" in username and "." in username:
            user = User.objects.by_mail(username)

        if not user:
            user = User.objects.by_username(username)

        if not user:
            User().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            user.attempts_count = 0
            user.save()
            return user

        on_login_failure(user, request)
        return None


def on_login_failure(user: User, request: HttpRequest | None) -> None:
    user.attempts_count += 1
    if user.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
        user.is_active = False
        user.attempts_count = 0
        user.deactivation_date = timezone.now()

        if request is None:
            user.save()
            return

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        use_https = request.is_secure()
        mail_context = {
            "username": user.username,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
        }
        send_mail(
            gettext("deactivation_email__subject"),
            render_to_string("users/deactivation_email.html", mail_context),
            None,
            [user.email],
            fail_silently=False,
        )

    user.save()


__all__ = []
