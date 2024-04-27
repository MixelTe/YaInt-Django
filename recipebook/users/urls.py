from django.contrib.auth import views
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.urls import path, reverse_lazy

from core.forms import add_styles_to_form
from users import views as u_views

app_name = "users"

urlpatterns = [
    path(
        "signup/",
        u_views.SignUpView.as_view(),
        name="signup",
    ),
    path(
        "profile/",
        u_views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "activate/<uidb64>/<token>",
        u_views.ActivateView.as_view(),
        name="activate",
    ),
    path(
        "activate/",
        u_views.ActivateDoneView.as_view(),
        name="activate_done",
    ),
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
            form_class=add_styles_to_form(AuthenticationForm),
        ),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:password_change_done"),
            form_class=add_styles_to_form(PasswordChangeForm),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
            form_class=add_styles_to_form(PasswordResetForm),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset/confirm/<uidb64>/<token>",
        views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
            form_class=add_styles_to_form(SetPasswordForm),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]


__all__ = []
