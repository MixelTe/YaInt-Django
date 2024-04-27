from typing import Any, Type, TypeVar

from django import forms


class BaseForm(forms.Form):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if isinstance(field.field.widget, forms.CheckboxInput):
                field.field.widget.attrs["class"] = "form-check-input"
            else:
                field.field.widget.attrs["class"] = "form-control"


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFiIeField(forms.FileField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(
        self,
        data: tuple | list | Any,
        initial: forms.FileField | None = None,
    ) -> tuple | list:
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return [single_file_clean(data, initial)]


TForm = TypeVar("TForm", bound=forms.BaseForm)


def add_styles_to_form(form: Type[TForm]) -> Type[TForm]:
    class StyledForm(BaseForm, form):
        pass

    return StyledForm


__all__ = []
