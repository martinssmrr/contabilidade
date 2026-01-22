
import os
import django
from django.urls import get_resolver, URLPattern, URLResolver

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestao360_project.settings")
django.setup()

def print_urls(resolver, prefix=''):
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            print_urls(pattern, prefix + str(pattern.pattern))
        elif isinstance(pattern, URLPattern):
            print(prefix + str(pattern.pattern))

print("Printing all registered URLs:")
print_urls(get_resolver())
