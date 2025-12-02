# ==================================
# GUNICORN CONFIGURATION
# ==================================

# Bind
bind = "0.0.0.0:8000"

# Workers
workers = 3
worker_class = "sync"
timeout = 120

# Forwarded headers - aceitar de qualquer IP
forwarded_allow_ips = "*"

# Configuração de proxy - forçar HTTPS scheme
secure_scheme_headers = {
    "X-FORWARDED-PROTO": "https"
}

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Preload app para melhor performance
preload_app = True
