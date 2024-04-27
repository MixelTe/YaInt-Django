from django import forms

from core.forms import BaseForm
from feedback.models import Comment, Rate


class RatingForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Rate
        fields = [
            model.value.field.name,
        ]


class DeleteRatingForm(BaseForm):
    delete_rating = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class CommentForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Comment
        fields = [
            model.text.field.name,
        ]


class DeleteCommentForm(BaseForm):
    delete_comment = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class CookedForm(BaseForm):
    add_cooked = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteCookedForm(BaseForm):
    delete_cooked = forms.BooleanField(widget=forms.HiddenInput, initial=True)


__all__ = []
