from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext
from django.views.generic import FormView, TemplateView, UpdateView, View

from users.forms import SignUpForm, UserForm
from users.models import User


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain
        use_https = self.request.is_secure()
        email = form.cleaned_data["email"]
        mail_context = {
            "username": form.cleaned_data["username"],
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
        }
        send_mail(
            gettext("signup__mail__subject"),
            render_to_string("users/signup_email.html", mail_context),
            None,
            [email],
            fail_silently=False,
        )
        messages.success(
            self.request,
            gettext("signup__success_message") % {"email": email},
        )
        return super().form_valid(form)


class ActivateView(View):
    def get(
        self,
        request: HttpRequest,
        uidb64: str,
        token: str,
    ) -> HttpResponse:
        user = get_user(uidb64)

        if user is None or not default_token_generator.check_token(
            user,
            token,
        ):
            messages.error(request, gettext("activate__error_message"))
            return redirect(reverse("users:activate_done"))

        if user.deactivation_date:
            if user.deactivation_date < timezone.now() - timedelta(
                days=7,
            ):
                messages.error(request, gettext("activate__old_message"))
                return redirect(reverse("users:activate_done"))
        elif user.date_joined < timezone.now() - timedelta(hours=12):
            messages.error(request, gettext("activate__old_message"))
            return redirect(reverse("users:activate_done"))

        user.is_active = True
        user.save()

        messages.success(request, gettext("activate__success_message"))
        return redirect(reverse("users:activate_done"))


class ActivateDoneView(TemplateView):
    template_name = "users/activate_done.html"


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = UserForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset: QuerySet | None = None) -> User:
        return self.request.user

    def form_valid(self, form: UserForm) -> HttpResponse:
        messages.success(self.request, gettext("profile__success_message"))
        return super().form_valid(form)


def get_user(uidb64: str) -> User | None:
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        return User.objects.get(pk=uid)
    except Exception:
        return None


__all__ = []
