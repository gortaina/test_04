from django.contrib.auth.middleware import MiddlewareMixin
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.utils.functional import SimpleLazyObject
from edital023.models import Cidadao, CidadaoAnonimo


def get_cidadao(request):
    cidadao = Cidadao.objects.filter(pk=request.session.get('cidadao_pk',  0)).first()
    return cidadao if cidadao is not None else CidadaoAnonimo()

def simple_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        return response
    return middleware

class CidadaoMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.cidadao = SimpleLazyObject(lambda: get_cidadao(request))
