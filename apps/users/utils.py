from django.conf import settings


def validate_file_upload(f):
    """Valida um arquivo de upload para movimentações financeiras.

    Retorna (True, None) quando válido, ou (False, mensagem_de_erro).
    Regras:
    - extensão permitida por `MOVIMENTACAO_ALLOWED_EXTENSIONS`
    - tamanho menor que `MOVIMENTACAO_MAX_UPLOAD_SIZE`
    """
    if not f:
        return True, None

    # extensão
    name = getattr(f, 'name', '')
    if '.' in name:
        ext = name.rsplit('.', 1)[1].lower()
    else:
        ext = ''

    allowed = getattr(settings, 'MOVIMENTACAO_ALLOWED_EXTENSIONS', ['pdf', 'png', 'jpg', 'jpeg'])
    if ext not in allowed:
        return False, f'Extensão .{ext} não permitida. Tipos permitidos: {", ".join(allowed)}.'

    max_size = getattr(settings, 'MOVIMENTACAO_MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
    size = getattr(f, 'size', None)
    if size is not None and size > max_size:
        return False, f'O arquivo excede o limite de {max_size // (1024*1024)} MB.'

    return True, None
