from django.conf import settings


def certidoes_alert(request):
    """Context processor que indica se o usuário logado possui alguma certidão com status 'Indisponível'.

    Retorna: {'has_certidao_indisponivel': bool}
    """
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {}

    try:
        from .models import CertidaoNegativa
        has = CertidaoNegativa.objects.filter(cliente=user, status=CertidaoNegativa.STATUS_INDISPONIVEL).exists()
        return {'has_certidao_indisponivel': has}
    except Exception:
        # Em caso de erro (migrations não aplicadas etc.), não quebrar o template
        return {'has_certidao_indisponivel': False}
