import os
from django import template

register = template.Library()


@register.filter(name='basename')
def basename(value):
    """Retorna o nome do arquivo (basename) a partir de um caminho ou FileField name."""
    try:
        return os.path.basename(str(value))
    except Exception:
        return value
