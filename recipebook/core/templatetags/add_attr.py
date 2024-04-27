from django import template
from django.forms import BoundField
from django.utils.safestring import SafeText

register = template.Library()


@register.filter(name="add_attr")
def add_attribute(field: BoundField, css: SafeText) -> SafeText:
    attrs = field.field.widget.attrs
    definition = css.split(",")

    for d in definition:
        if ":" not in d:
            attrs["class"] += f" {d}"
        else:
            key, val = d.split(":")
            attrs[key] += f"{val}"

    return field.as_widget(attrs=attrs)


__all__ = []
