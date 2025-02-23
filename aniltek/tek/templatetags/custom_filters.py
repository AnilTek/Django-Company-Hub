from django import template

register = template.Library()

@register.filter
def to_field_name(value):
    """Boşlukları alt çizgi ile değiştir ve küçük harfe çevir."""
    return value.lower().replace(" ", "_")
