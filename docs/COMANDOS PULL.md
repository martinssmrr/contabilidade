comandos quando troca apenas html e imagens


# 1. Primeiro, vamos fazer o deploy das alterações nos templates
cd /root/vetorial
git pull origin master

# 2. Copiar os arquivos de media do container para o host (se existirem no container)
docker cp vetorial_web:/app/media/. /root/vetorial/media/

# 3. Ajustar permissões
chmod -R 755 /root/vetorial/media/

# 4. Verificar se os arquivos foram copiados
ls -la /root/vetorial/media/

# 5. Reiniciar o container web
docker-compose -f docker-compose.prod.yml restart web

# 6. Verificar se há imagens no container
docker-compose -f docker-compose.prod.yml exec web ls -la /app/media/

# 2. Coletar arquivos estáticos no container
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# 3. Copiar os arquivos estáticos do container para o host (onde o Nginx serve)
docker cp vetorial_web:/app/staticfiles/. /root/vetorial/staticfiles/

# 4. Ajustar permissões
chmod -R 755 /root/vetorial/staticfiles/

# 5. Verificar se o logo.png foi copiado
ls -la /root/vetorial/staticfiles/img/logo.png

# 6. Se necessário, reiniciar o Nginx
nginx -t && systemctl reload nginx