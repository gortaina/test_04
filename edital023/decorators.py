from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def _candidato_passes_test(test_func, error_message=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.cidadao):
                return view_func(request, *args, **kwargs)
            if error_message is not None:
                messages.add_message(request, messages.ERROR, error_message)
            return redirect('home')
        return _wrapped_view
    return decorator


def cidadao_is_authenticated(function=None):
    actual_decorator = _candidato_passes_test(lambda c: c.is_authenticated, f'Você ainda não se autenticou no sistema autenticado.')
    if function:
        return actual_decorator(function)
    return actual_decorator

def cidadao_is_anonymous(function=None):
    actual_decorator = _candidato_passes_test(lambda c: not c.is_authenticated, f'Você já está autenticado.')
    if function:
        return actual_decorator(function)
    return actual_decorator
