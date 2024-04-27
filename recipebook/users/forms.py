from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.forms import BaseForm
from users import models


class SignUpForm(UserCreationForm, BaseForm):
    def clean(self) -> dict[str, Any]:
        email = self.cleaned_data[models.User.email.field.name]
        email = models.UserManager.normalize_email(email)
        self.cleaned_data[models.User.email.field.name] = email

        return self.cleaned_data

    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = [
            models.User.username.field.name,
            models.User.email.field.name,
        ]


class UserForm(forms.ModelForm, BaseForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields[models.User.trusted.field.name].disabled = True
        self.fields[models.User.email.field.name].disabled = True

    class Meta:
        model = models.User
        fields = [
            models.User.first_name.field.name,
            models.User.last_name.field.name,
            models.User.email.field.name,
            models.User.trusted.field.name,
            models.User.image.field.name,
        ]


__all__ = []
